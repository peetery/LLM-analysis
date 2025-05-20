import unittest
from unittest.mock import patch, MagicMock
from typing import TypedDict, List
from order_calculator import OrderCalculator


# class Item(TypedDict):
#     name: str
#     price: float
#     quantity: int
#
#
# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = free_shipping_threshold
#         self.shipping_cost = shipping_cost
#         self.items = {}
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not name or price < 0 or quantity < 0:
#             raise ValueError("Invalid item parameters")
#         if name in self.items:
#             self.items[name]["quantity"] += quantity
#         else:
#             self.items[name] = {"price": price, "quantity": quantity}
#
#     def remove_item(self, name: str):
#         if not name:
#             raise ValueError("Item name cannot be empty")
#         if name in self.items:
#             del self.items[name]
#
#     def get_subtotal(self) -> float:
#         subtotal = 0.0
#         for item_data in self.items.values():
#             subtotal += item_data["price"] * item_data["quantity"]
#         return subtotal
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if discount < 0:
#             raise ValueError("Discount cannot be negative")
#         return max(0, subtotal - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if discounted_subtotal < 0:
#             raise ValueError("Subtotal cannot be negative")
#         return 0.0 if discounted_subtotal >= self.free_shipping_threshold else self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if amount < 0:
#             raise ValueError("Amount cannot be negative")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if discount < 0:
#             raise ValueError("Discount cannot be negative")
#         subtotal = self.get_subtotal()
#         discounted_subtotal = self.apply_discount(subtotal, discount)
#         shipping = self.calculate_shipping(discounted_subtotal)
#         return discounted_subtotal + shipping + self.calculate_tax(discounted_subtotal + shipping)
#
#     def total_items(self) -> int:
#         return sum(item_data["quantity"] for item_data in self.items.values())
#
#     def clear_order(self):
#         self.items = {}
#
#     def list_items(self) -> List[str]:
#         return list(self.items.keys())
#
#     def is_empty(self) -> bool:
#         return len(self.items) == 0


class TestOrderCalculator(unittest.TestCase):
    def test_default_initialization(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 200.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_initialization_with_invalid_tax_rate(self):
        calculator = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calculator.tax_rate, -0.1)

        calculator = OrderCalculator(tax_rate=1.5)
        self.assertEqual(calculator.tax_rate, 1.5)

    def test_initialization_with_negative_shipping_cost(self):
        calculator = OrderCalculator(shipping_cost=-5.0)
        self.assertEqual(calculator.shipping_cost, -5.0)

    def test_initialization_with_negative_free_shipping_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=-50.0)
        self.assertEqual(calculator.free_shipping_threshold, -50.0)

    def test_add_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items["Item1"]["price"], 10.0)
        self.assertEqual(calculator.items["Item1"]["quantity"], 1)

    def test_add_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertEqual(len(calculator.items), 2)
        self.assertEqual(calculator.items["Item1"]["price"], 10.0)
        self.assertEqual(calculator.items["Item2"]["price"], 20.0)

    def test_add_item_with_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 5)
        self.assertEqual(calculator.items["Item1"]["quantity"], 5)

    def test_add_duplicate_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 2)
        calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(calculator.items["Item1"]["quantity"], 5)

    def test_add_item_with_zero_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 0)
        self.assertEqual(calculator.items["Item1"]["quantity"], 0)

    def test_add_item_with_negative_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", 10.0, -1)

    def test_add_item_with_zero_price(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 0.0)
        self.assertEqual(calculator.items["Item1"]["price"], 0.0)

    def test_add_item_with_negative_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", -10.0)

    def test_add_item_with_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("", 10.0)

    def test_add_item_with_none_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(None, 10.0)

    def test_add_item_with_invalid_price_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Item1", "invalid")

    def test_add_item_with_invalid_quantity_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Item1", 10.0, "invalid")

    def test_remove_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.remove_item("Item1")
        self.assertEqual(len(calculator.items), 0)

    def test_remove_nonexistent_item(self):
        calculator = OrderCalculator()
        calculator.remove_item("NonExistentItem")
        self.assertEqual(len(calculator.items), 0)

    def test_remove_item_with_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item("")

    def test_remove_item_with_none_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(None)

    def test_remove_item_case_sensitivity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.remove_item("item1")
        self.assertEqual(len(calculator.items), 1)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertEqual(calculator.get_subtotal(), 30.0)

    def test_get_subtotal_with_quantities(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 2)
        calculator.add_item("Item2", 20.0, 3)
        self.assertEqual(calculator.get_subtotal(), 10.0 * 2 + 20.0 * 3)

    def test_apply_discount_zero(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_partial(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calculator.apply_discount(subtotal, 30.0), 70.0)

    def test_apply_discount_full(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calculator.apply_discount(subtotal, 100.0), 0.0)

    def test_apply_discount_greater_than_subtotal(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calculator.apply_discount(subtotal, 150.0), 0.0)

    def test_apply_discount_negative(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        with self.assertRaises(ValueError):
            calculator.apply_discount(subtotal, -10.0)

    def test_apply_discount_invalid_type(self):
        calculator = OrderCalculator()
        subtotal = 100.0
        with self.assertRaises(TypeError):
            calculator.apply_discount(subtotal, "invalid")

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(90.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_shipping(-10.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_positive_amount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_tax_with_custom_rate(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calculator.calculate_tax(100.0), 10.0)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_total(), 12.3)  # 0 (subtotal) + 10 (shipping) + 0.23*10 (tax) = 12.3

    def test_calculate_total_without_discount(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 50.0)
        # 50 (subtotal) + 10 (shipping) + 0.23*(50+10) = 73.8
        self.assertEqual(calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 100.0)
        # 100 (subtotal) - 20 (discount) = 80
        # 80 + 0 (free shipping) + 0.23*80 = 98.4
        self.assertEqual(calculator.calculate_total(20.0), 98.4)

    def test_calculate_total_with_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 150.0)
        # 150 (subtotal) + 0 (shipping) + 0.23*150 = 184.5
        self.assertEqual(calculator.calculate_total(), 184.5)

    def test_calculate_total_without_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 80.0)
        # 80 (subtotal) + 10 (shipping) + 0.23*(80+10) = 110.7
        self.assertEqual(calculator.calculate_total(), 110.7)

    def test_calculate_total_discount_greater_than_subtotal(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 50.0)
        # 50 (subtotal) - 100 (discount) = 0
        # 0 + 10 (shipping) + 0.23*10 = 12.3
        self.assertEqual(calculator.calculate_total(100.0), 12.3)

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_total_items_single_item_no_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.total_items(), 1)

    def test_total_items_single_item_with_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 5)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 2)
        calculator.add_item("Item2", 20.0, 3)
        calculator.add_item("Item3", 30.0, 1)
        self.assertEqual(calculator.total_items(), 6)

    def test_clear_order_empty(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertEqual(len(calculator.items), 0)

    def test_clear_order_with_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        calculator.clear_order()
        self.assertEqual(len(calculator.items), 0)

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.list_items(), [])

    def test_list_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.list_items(), ["Item1"])

    def test_list_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertCountEqual(calculator.list_items(), ["Item1", "Item2"])

    def test_is_empty_new_order(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_with_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertFalse(calculator.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.remove_item("Item1")
        self.assertTrue(calculator.is_empty())

    def test_is_empty_after_clear(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())


if __name__ == "__main__":
    unittest.main()