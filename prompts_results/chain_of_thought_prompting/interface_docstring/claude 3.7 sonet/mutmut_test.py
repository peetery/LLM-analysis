import unittest
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
#         if not isinstance(tax_rate, (int, float)):
#             raise TypeError("Tax rate must be a number")
#         if not isinstance(free_shipping_threshold, (int, float)):
#             raise TypeError("Free shipping threshold must be a number")
#         if not isinstance(shipping_cost, (int, float)):
#             raise TypeError("Shipping cost must be a number")
#
#         if tax_rate < 0.0 or tax_rate > 1.0:
#             raise ValueError("Tax rate must be between 0.0 and 1.0")
#         if free_shipping_threshold < 0:
#             raise ValueError("Free shipping threshold must be non-negative")
#         if shipping_cost < 0:
#             raise ValueError("Shipping cost must be non-negative")
#
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = free_shipping_threshold
#         self.shipping_cost = shipping_cost
#         self.items = []
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string")
#         if not isinstance(price, (int, float)):
#             raise TypeError("Item price must be a number")
#         if not isinstance(quantity, int):
#             raise TypeError("Item quantity must be an integer")
#
#         if not name:
#             raise ValueError("Item name cannot be empty")
#         if price <= 0:
#             raise ValueError("Item price must be positive")
#         if quantity < 1:
#             raise ValueError("Item quantity must be at least 1")
#
#         # Check if item with same name but different price exists
#         for item in self.items:
#             if item["name"] == name and item["price"] != price:
#                 raise ValueError(f"Item '{name}' already exists with a different price")
#
#         # Check if item with same name and price exists
#         for item in self.items:
#             if item["name"] == name and item["price"] == price:
#                 item["quantity"] += quantity
#                 return
#
#         # Add new item
#         self.items.append({"name": name, "price": price, "quantity": quantity})
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string")
#
#         for i, item in enumerate(self.items):
#             if item["name"] == name:
#                 self.items.pop(i)
#                 return
#
#         raise ValueError(f"Item '{name}' not found in order")
#
#     def get_subtotal(self) -> float:
#         if not self.items:
#             raise ValueError("Order is empty")
#
#         subtotal = 0.0
#         for item in self.items:
#             subtotal += item["price"] * item["quantity"]
#         return subtotal
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (int, float)):
#             raise TypeError("Subtotal must be a number")
#         if not isinstance(discount, (int, float)):
#             raise TypeError("Discount must be a number")
#
#         if subtotal < 0:
#             raise ValueError("Subtotal cannot be negative")
#         if discount < 0.0 or discount > 1.0:
#             raise ValueError("Discount must be between 0.0 and 1.0")
#
#         return subtotal * (1 - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (int, float)):
#             raise TypeError("Discounted subtotal must be a number")
#
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (int, float)):
#             raise TypeError("Amount must be a number")
#
#         if amount < 0:
#             raise ValueError("Amount cannot be negative")
#
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if not isinstance(discount, (int, float)):
#             raise TypeError("Discount must be a number")
#
#         if discount < 0.0 or discount > 1.0:
#             raise ValueError("Discount must be between 0.0 and 1.0")
#
#         subtotal = self.get_subtotal()  # Will raise ValueError if order is empty
#         discounted_subtotal = self.apply_discount(subtotal, discount)
#         shipping = self.calculate_shipping(discounted_subtotal)
#         tax = self.calculate_tax(discounted_subtotal + shipping)
#
#         return discounted_subtotal + shipping + tax
#
#     def total_items(self) -> int:
#         total = 0
#         for item in self.items:
#             total += item["quantity"]
#         return total
#
#     def clear_order(self):
#         self.items = []
#
#     def list_items(self) -> List[str]:
#         return [item["name"] for item in self.items]
#
#     def is_empty(self) -> bool:
#         return len(self.items) == 0


class TestOrderCalculator(unittest.TestCase):
    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "item1")
        self.assertEqual(calc.items[0]["price"], 10.0)
        self.assertEqual(calc.items[0]["quantity"], 1)

    def test_add_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        self.assertEqual(len(calc.items), 2)
        self.assertEqual(calc.items[0]["name"], "item1")
        self.assertEqual(calc.items[1]["name"], "item2")

    def test_add_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 5)
        self.assertEqual(calc.items[0]["quantity"], 5)

    def test_add_same_item_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 2)
        calc.add_item("item1", 10.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["quantity"], 5)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        self.assertEqual(calc.items[0]["quantity"], 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item1", 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item1", -10.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item1", 10.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item1", 10.0, -1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        with self.assertRaises(ValueError):
            calc.add_item("item1", 20.0)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("item1", "10.0")

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("item1", 10.0, 1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        calc.remove_item("item1")
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "item2")

    def test_remove_and_readd_item(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.remove_item("item1")
        calc.add_item("item1", 10.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "item1")

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("item1")

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 2)
        calc.add_item("item2", 20.0, 3)
        self.assertEqual(calc.get_subtotal(), 10.0 * 2 + 20.0 * 3)

    def test_get_subtotal_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)
        calc.add_item("item2", 20.0)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 5)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_after_removing_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        calc.remove_item("item1")
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.5), 50.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(0.0, 0.5), 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.5)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.5)

    def test_apply_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100.0", 0.5)

    def test_apply_discount_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.5")

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("100.0")

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("100.0")

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 50.0)
        # Subtotal: 50.0, Shipping: 10.0, Tax: (50+10)*0.2 = 12.0
        self.assertEqual(calc.calculate_total(), 72.0)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 100.0)
        # Subtotal: 100.0, Discount: 100*0.1=10, Discounted: 90.0, Shipping: 10.0, Tax: (90+10)*0.2 = 20.0
        self.assertEqual(calc.calculate_total(0.1), 120.0)

    def test_calculate_total_below_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 50.0)
        # Subtotal: 50.0, Shipping: 10.0, Tax: (50+10)*0.2 = 12.0
        self.assertEqual(calc.calculate_total(), 72.0)

    def test_calculate_total_above_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 120.0)
        # Subtotal: 120.0, Shipping: 0.0, Tax: 120*0.2 = 24.0
        self.assertEqual(calc.calculate_total(), 144.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_zero_discount(self):
        calc = OrderCalculator(tax_rate=0.2)
        calc.add_item("item1", 100.0)
        self.assertEqual(calc.calculate_total(0.0), calc.calculate_total())

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 50.0)
        # Subtotal: 50.0, Discount: 50*1.0=50, Discounted: 0.0, Shipping: 10.0, Tax: (0+10)*0.2 = 2.0
        self.assertEqual(calc.calculate_total(1.0), 12.0)

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item("item1", 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_calculate_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item("item1", 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total("0.1")

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 2)
        calc.add_item("item2", 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        self.assertEqual(set(calc.list_items()), {"item1", "item2"})

    def test_list_items_duplicate_names(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item1", 10.0, 2)
        self.assertEqual(calc.list_items(), ["item1"])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_with_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.remove_item("item1")
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_full_order_calculation(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("item1", 50.0, 2)
        calc.add_item("item2", 25.0, 1)

        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 125.0)

        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 112.5)

        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 0.0)

        tax = calc.calculate_tax(discounted + shipping)
        self.assertEqual(tax, 22.5)

        total = calc.calculate_total(0.1)
        self.assertEqual(total, 135.0)

    # def test_integration_add_remove_calculate(self):
    #     calc = OrderCalculator(tax_rate=0.2)
    #     calc.add_item("item1", 50.0)
    #     calc.add_item("item2", 30.0)
    #     calc.remove_item("item1")
    #     self.assertEqual(calc.calculate_total(), 36.0)  # 30 + (30 * 0.2)

    def test_integration_add_clear_verify_empty(self):
        calc = OrderCalculator()
        calc.add_item("item1", 10.0)
        calc.add_item("item2", 20.0)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())


if __name__ == "__main__":
    unittest.main()