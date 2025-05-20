import unittest
from typing import TypedDict, List
from unittest.mock import patch, MagicMock
from order_calculator import OrderCalculator


# class Item(TypedDict):
#     name: str
#     price: float
#     quantity: int
#
#
# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         pass
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         pass
#
#     def remove_item(self, name: str):
#         pass
#
#     def get_subtotal(self) -> float:
#         pass
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         pass
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         pass
#
#     def calculate_tax(self, amount: float) -> float:
#         pass
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         pass
#
#     def total_items(self) -> int:
#         pass
#
#     def clear_order(self):
#         pass
#
#     def list_items(self) -> List[str]:
#         pass
#
#     def is_empty(self) -> bool:
#         pass


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()
        self.calculator_custom = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)

    def test_init_default_values(self):
        self.assertEqual(self.calculator._tax_rate, 0.23)
        self.assertEqual(self.calculator._free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator._shipping_cost, 10.0)
        self.assertEqual(self.calculator._items, {})

    def test_init_custom_values(self):
        self.assertEqual(self.calculator_custom._tax_rate, 0.1)
        self.assertEqual(self.calculator_custom._free_shipping_threshold, 200.0)
        self.assertEqual(self.calculator_custom._shipping_cost, 15.0)

    def test_add_item_new(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(self.calculator._items["Apple"], {"price": 1.5, "quantity": 3})

    def test_add_item_existing(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.add_item("Apple", 1.5, 2)
        self.assertEqual(self.calculator._items["Apple"], {"price": 1.5, "quantity": 5})

    def test_add_item_different_price(self):
        self.calculator.add_item("Apple", 1.5, 3)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0, 2)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", -1.5)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.5, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.5, -2)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 1.5)

    def test_remove_item_existing(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.remove_item("Apple")
        self.assertNotIn("Apple", self.calculator._items)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("Apple")

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.add_item("Banana", 2.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 8.5)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_percentage(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 100.0), 0.0)

    def test_apply_discount_over_full(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 110.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(90.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_custom_threshold(self):
        self.assertEqual(self.calculator_custom.calculate_shipping(150.0), 15.0)
        self.assertEqual(self.calculator_custom.calculate_shipping(200.0), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_custom_rate(self):
        self.assertEqual(self.calculator_custom.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_empty_no_discount(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_with_items_no_discount(self):
        self.calculator.add_item("Apple", 50.0, 1)
        self.assertEqual(self.calculator.calculate_total(), 71.5)  # 50 + 10 shipping + 11.5 tax

    def test_calculate_total_free_shipping_no_discount(self):
        self.calculator.add_item("Apple", 100.0, 1)
        self.assertEqual(self.calculator.calculate_total(), 123.0)  # 100 + 0 shipping + 23 tax

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Apple", 100.0, 1)
        self.assertEqual(self.calculator.calculate_total(20.0), 98.4)  # 80 + 0 shipping + 18.4 tax

    def test_calculate_total_with_discount_below_threshold(self):
        self.calculator.add_item("Apple", 100.0, 1)
        self.assertEqual(self.calculator.calculate_total(50.0), 71.5)  # 50 + 10 shipping + 11.5 tax

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.add_item("Banana", 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.add_item("Banana", 2.0, 2)
        self.calculator.clear_order()
        self.assertEqual(self.calculator._items, {})

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(self.calculator.list_items(), ["Apple: 3 x $1.5"])

    def test_list_items_multiple(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.calculator.add_item("Banana", 2.0, 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Apple: 3 x $1.5", items)
        self.assertIn("Banana: 2 x $2.0", items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertFalse(self.calculator.is_empty())

    def test_integration_full_order_flow(self):
        self.calculator.add_item("Apple", 40.0, 2)
        self.calculator.add_item("Banana", 30.0, 1)

        self.assertEqual(self.calculator.get_subtotal(), 110.0)
        self.assertEqual(self.calculator.total_items(), 3)

        total = self.calculator.calculate_total(10.0)
        expected = 99.0 + 99.0 * 0.23  # 99 (after discount) + tax
        self.assertAlmostEqual(total, expected, places=2)

        self.calculator.remove_item("Apple")
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()