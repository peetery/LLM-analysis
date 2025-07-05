import unittest
from typing import TypedDict, List

class Item(TypedDict):
    name: str
    price: float
    quantity: int

class OrderCalculator:
    def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        pass

    def add_item(self, name: str, price: float, quantity: int = 1):
        pass

    def remove_item(self, name: str):
        pass

    def get_subtotal(self) -> float:
        pass

    def apply_discount(self, subtotal: float, discount: float) -> float:
        pass

    def calculate_shipping(self, discounted_subtotal: float) -> float:
        pass

    def calculate_tax(self, amount: float) -> float:
        pass

    def calculate_total(self, discount: float = 0.0) -> float:
        pass

    def total_items(self) -> int:
        pass

    def clear_order(self):
        pass

    def list_items(self) -> List[str]:
        pass

    def is_empty(self) -> bool:
        pass


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()
        self.calculator_custom = OrderCalculator(tax_rate=0.10, free_shipping_threshold=200.0, shipping_cost=15.0)

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.10, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calculator.tax_rate, 0.10)
        self.assertEqual(calculator.free_shipping_threshold, 200.0)
        self.assertEqual(calculator.shipping_cost, 15.0)

    def test_add_item_single(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn("Test Item", self.calculator.list_items())

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item("Test Item", 10.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", -10.0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 0.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 10.0, 0)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 10.0)

    def test_add_item_invalid_name_none(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(None, 10.0)

    def test_add_multiple_items(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertIn("Item 1", self.calculator.list_items())
        self.assertIn("Item 2", self.calculator.list_items())

    def test_remove_item_existing(self):
        self.calculator.add_item("Test Item", 10.0)
        self.calculator.remove_item("Test Item")
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertNotIn("Test Item", self.calculator.list_items())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("Nonexistent Item")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

    def test_get_subtotal_multiple_quantity(self):
        self.calculator.add_item("Test Item", 10.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_percentage(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.1), 90.0)

    def test_apply_discount_percentage_greater_than_one(self):
        subtotal = 100.0
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(subtotal, 1.1)

    def test_apply_discount_negative(self):
        subtotal = 100.0
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(subtotal, -0.1)

    def test_calculate_shipping_below_threshold(self):
        discounted_subtotal = 50.0
        self.assertEqual(self.calculator.calculate_shipping(discounted_subtotal), 10.0)

    def test_calculate_shipping_at_threshold(self):
        discounted_subtotal = 100.0
        self.assertEqual(self.calculator.calculate_shipping(discounted_subtotal), 0.0)

    def test_calculate_shipping_above_threshold(self):
        discounted_subtotal = 150.0
        self.assertEqual(self.calculator.calculate_shipping(discounted_subtotal), 0.0)

    def test_calculate_shipping_custom_threshold(self):
        discounted_subtotal = 150.0
        self.assertEqual(self.calculator_custom.calculate_shipping(discounted_subtotal), 15.0)
        
        discounted_subtotal = 200.0
        self.assertEqual(self.calculator_custom.calculate_shipping(discounted_subtotal), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-50.0)

    def test_calculate_tax_zero(self):
        amount = 0.0
        self.assertEqual(self.calculator.calculate_tax(amount), 0.0)

    def test_calculate_tax_positive(self):
        amount = 100.0
        self.assertEqual(self.calculator.calculate_tax(amount), 23.0)

    def test_calculate_tax_custom_rate(self):
        amount = 100.0
        self.assertEqual(self.calculator_custom.calculate_tax(amount), 10.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item("Item 1", 50.0)
        self.assertEqual(self.calculator.calculate_total(), 73.5)  # 50 + 10 shipping + 23% tax on 60

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item 1", 100.0)
        self.assertEqual(self.calculator.calculate_total(0.1), 110.7)  # 100 - 10 discount + 0 shipping + 23% tax on 90

    def test_calculate_total_empty_order(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item("Item 1", 200.0)
        self.assertEqual(self.calculator.calculate_total(), 246.0)  # 200 + 0 shipping + 23% tax on 200

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_multiple_items(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_total_items_multiple_quantity(self):
        self.calculator.add_item("Test Item", 10.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_clear_order(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(len(self.calculator.list_items()), 0)

    def test_list_items_empty(self):
        self.assertEqual(len(self.calculator.list_items()), 0)

    def test_list_items_single(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertEqual(len(self.calculator.list_items()), 1)
        self.assertIn("Test Item", self.calculator.list_items())

    def test_list_items_multiple(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Item 1", items)
        self.assertIn("Item 2", items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item("Test Item", 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == "__main__":
    unittest.main()