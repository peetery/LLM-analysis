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
#         if not isinstance(tax_rate, float):  # Type check first for more specific error
#             raise TypeError("Tax rate must be a float.")
#         if not (0.0 <= tax_rate <= 1.0):
#             raise ValueError("Tax rate must be between 0.0 and 1.0.")
#
#         if not isinstance(free_shipping_threshold, (int, float)):
#             raise TypeError("Free shipping threshold must be a number.")
#         if free_shipping_threshold < 0:
#             raise ValueError("Free shipping threshold cannot be negative.")
#
#         if not isinstance(shipping_cost, (int, float)):
#             raise TypeError("Shipping cost must be a number.")
#         if shipping_cost < 0:
#             raise ValueError("Shipping cost cannot be negative.")
#
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = float(free_shipping_threshold)
#         self.shipping_cost = float(shipping_cost)
#         self.items: List[Item] = []
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not name:
#             raise ValueError("Item name cannot be empty.")
#
#         if not isinstance(price, (int, float)):  # Allow int for price, convert to float
#             raise TypeError("Item price must be a number.")
#         price = float(price)
#         if price <= 0:
#             raise ValueError("Item price must be positive.")
#
#         if not isinstance(quantity, int):
#             raise TypeError("Item quantity must be an integer.")
#         if quantity < 1:
#             raise ValueError("Item quantity must be at least 1.")
#
#         for item in self.items:
#             if item['name'] == name:
#                 if item['price'] != price:
#                     raise ValueError(
#                         f"Item '{name}' already exists with a different price ({item['price']}) than specified ({price}).")
#                 item['quantity'] += quantity
#                 return
#         self.items.append({'name': name, 'price': price, 'quantity': quantity})
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#
#         original_len = len(self.items)
#         self.items = [item for item in self.items if item['name'] != name]
#         if len(self.items) == original_len:
#             raise ValueError(f"Item '{name}' not found in order.")
#
#     def get_subtotal(self) -> float:
#         if not self.items:
#             raise ValueError("Cannot calculate subtotal for an empty order.")
#         return float(sum(item['price'] * item['quantity'] for item in self.items))
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (int, float)):
#             raise TypeError("Subtotal must be a number.")
#         subtotal = float(subtotal)
#         if subtotal < 0:
#             raise ValueError("Subtotal cannot be negative.")
#
#         if not isinstance(discount, float):
#             raise TypeError("Discount must be a float.")
#         if not (0.0 <= discount <= 1.0):
#             raise ValueError("Discount must be between 0.0 and 1.0.")
#
#         return subtotal * (1.0 - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (int, float)):
#             raise TypeError("Discounted subtotal must be a number.")
#         discounted_subtotal = float(discounted_subtotal)
#         # Docstring implies discounted_subtotal >= 0.0 but only TypeError for invalid input
#         # Negative values will be treated as < free_shipping_threshold
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (int, float)):
#             raise TypeError("Amount must be a number.")
#         amount = float(amount)
#         if amount < 0:
#             raise ValueError("Amount cannot be negative.")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if not isinstance(discount, float):
#             raise TypeError("Discount must be a float.")
#         if not self.items:  # Check before get_subtotal for a more specific error as per docstring
#             raise ValueError("Cannot calculate total for an empty order.")
#
#         subtotal = self.get_subtotal()  # Can raise ValueError if order becomes empty concurrently (not possible in single thread)
#         discounted_subtotal = self.apply_discount(subtotal, discount)  # Can raise ValueError/TypeError
#         shipping = self.calculate_shipping(discounted_subtotal)  # Can raise TypeError
#
#         amount_before_tax = discounted_subtotal + shipping
#         tax = self.calculate_tax(amount_before_tax)  # Can raise ValueError/TypeError
#
#         total = amount_before_tax + tax
#         return total
#
#     def total_items(self) -> int:
#         return sum(item['quantity'] for item in self.items)
#
#     def clear_order(self):
#         self.items = []
#
#     def list_items(self) -> List[str]:
#         return sorted([item['name'] for item in self.items])  # Sorted for predictable testing
#
#     def is_empty(self) -> bool:
#         return not self.items


class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.tax_rate, 0.23)
        self.assertAlmostEqual(calc.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.tax_rate, 0.1)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertAlmostEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertAlmostEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertAlmostEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertAlmostEqual(calc.shipping_cost, 0.0)

    def test_init_raises_value_error_for_tax_rate_below_zero(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=-0.1)

    def test_init_raises_value_error_for_tax_rate_above_one(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=1.1)

    def test_init_raises_value_error_for_negative_free_shipping_threshold(self):
        with self.assertRaisesRegex(ValueError, "Free shipping threshold cannot be negative."):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_raises_value_error_for_negative_shipping_cost(self):
        with self.assertRaisesRegex(ValueError, "Shipping cost cannot be negative."):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_raises_type_error_for_invalid_tax_rate_type(self):
        with self.assertRaisesRegex(TypeError, "Tax rate must be a float."):
            OrderCalculator(tax_rate="0.23")  # type: ignore

    # def test_init_raises_type_error_for_invalid_free_shipping_threshold_type(self):
    #     with self.assertRaisesRegex(TypeError, "Free shipping threshold must be a number."):
    #         OrderCalculator(free_shipping_threshold="100")  # type: ignore
    #
    # def test_init_raises_type_error_for_invalid_shipping_cost_type(self):
    #     with self.assertRaisesRegex(TypeError, "Shipping cost must be a number."):
    #         OrderCalculator(shipping_cost="10")  # type: ignore

    def test_add_item_new_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0], {'name': "Apple", 'price': 0.5, 'quantity': 1})

    def test_add_item_new_item_specified_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Banana", 0.3, quantity=5)
        self.assertEqual(calc.items[0], {'name': "Banana", 'price': 0.3, 'quantity': 5})

    def test_add_item_multiple_distinct_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.add_item("Banana", 0.3)
        self.assertEqual(len(calc.items), 2)
        self.assertIn({'name': "Apple", 'price': 0.5, 'quantity': 1}, calc.items)
        self.assertIn({'name': "Banana", 'price': 0.3, 'quantity': 1}, calc.items)

    def test_add_item_existing_item_same_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=2)
        calc.add_item("Apple", 0.5, quantity=3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_raises_value_error_for_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(ValueError, "Item name cannot be empty."):
            calc.add_item("", 0.5)

    # def test_add_item_raises_value_error_for_price_zero(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Item price must be positive."):
    #         calc.add_item("Apple", 0.0)

    # def test_add_item_raises_value_error_for_negative_price(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Item price must be positive."):
    #         calc.add_item("Apple", -0.5)

    # def test_add_item_raises_value_error_for_quantity_less_than_one(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Item quantity must be at least 1."):
    #         calc.add_item("Apple", 0.5, quantity=0)
    #     with self.assertRaisesRegex(ValueError, "Item quantity must be at least 1."):
    #         calc.add_item("Banana", 0.5, quantity=-1)
    #
    # def test_add_item_raises_value_error_for_same_name_different_price(self):
    #     calc = OrderCalculator()
    #     calc.add_item("Apple", 0.5)
    #     with self.assertRaisesRegex(ValueError, "Item 'Apple' already exists with a different price"):
    #         calc.add_item("Apple", 0.6)

    def test_add_item_raises_type_error_for_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            calc.add_item(123, 0.5)  # type: ignore

    # def test_add_item_raises_type_error_for_non_numeric_price(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(TypeError, "Item price must be a number."):
    #         calc.add_item("Apple", "0.5")  # type: ignore

    # def test_add_item_raises_type_error_for_non_integer_quantity(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(TypeError, "Item quantity must be an integer."):
    #         calc.add_item("Apple", 0.5, quantity=1.5)  # type: ignore

    def test_remove_item_existing_item_from_multiple(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.add_item("Banana", 0.3)
        calc.remove_item("Apple")
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], "Banana")

    def test_remove_item_only_item_in_order(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

    # def test_remove_item_raises_value_error_for_non_existent_item(self):
    #     calc = OrderCalculator()
    #     calc.add_item("Apple", 0.5)
    #     with self.assertRaisesRegex(ValueError, "Item 'Banana' not found in order."):
    #         calc.remove_item("Banana")

    # def test_remove_item_raises_value_error_for_empty_order(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Item 'Apple' not found in order."):
    #         calc.remove_item("Apple")

    def test_remove_item_raises_type_error_for_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            calc.remove_item(123)  # type: ignore

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        self.assertAlmostEqual(calc.get_subtotal(), 0.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=2)  # 1.0
        calc.add_item("Banana", 0.3, quantity=3)  # 0.9
        self.assertAlmostEqual(calc.get_subtotal(), 1.9)

    def test_get_subtotal_after_item_manipulation(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.0, quantity=2)
        calc.add_item("Banana", 2.0, quantity=1)
        calc.remove_item("Apple")
        self.assertAlmostEqual(calc.get_subtotal(), 2.0)

    # def test_get_subtotal_raises_value_error_for_empty_order(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal for an empty order."):
    #         calc.get_subtotal()

    def test_apply_discount_valid_discount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(0.0, 0.2), 0.0)

    # def test_apply_discount_raises_value_error_for_negative_subtotal(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Subtotal cannot be negative."):
    #         calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_raises_value_error_for_discount_less_than_zero(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_raises_value_error_for_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_raises_type_error_for_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(TypeError, "Subtotal must be a number."):
            calc.apply_discount("100.0", 0.1)  # type: ignore

    # def test_apply_discount_raises_type_error_for_non_float_discount(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(TypeError, "Discount must be a float."):
    #         calc.apply_discount(100.0, "0.1")  # type: ignore

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal_non_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_custom_threshold_and_cost_free_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_custom_threshold_and_cost_shipping_charged(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_shipping(49.0), 5.0)

    def test_calculate_shipping_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(0.0), 0.0)
        self.assertAlmostEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_raises_type_error_for_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(TypeError, "Discounted subtotal must be a number."):
            calc.calculate_shipping("50.0")  # type: ignore

    def test_calculate_shipping_negative_subtotal_acts_as_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(-10.0), 10.0)
        calc_zero_threshold = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc_zero_threshold.calculate_shipping(-10.0), 10.0)  # -10 < 0 is false

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.20)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.20)
        self.assertAlmostEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    # def test_calculate_tax_raises_value_error_for_negative_amount(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Amount cannot be negative."):
    #         calc.calculate_tax(-10.0)

    def test_calculate_tax_raises_type_error_for_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaisesRegex(TypeError, "Amount must be a number."):
            calc.calculate_tax("100.0")  # type: ignore

    def test_calculate_total_no_discount_shipping_applies(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 50.0)  # Subtotal = 50.0
        # Discounted Subtotal = 50.0
        # Shipping = 10.0
        # Amount before tax = 60.0
        # Tax = 60.0 * 0.1 = 6.0
        # Total = 60.0 + 6.0 = 66.0
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 66.0)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 120.0)  # Subtotal = 120.0
        # Discounted Subtotal = 120.0
        # Shipping = 0.0
        # Amount before tax = 120.0
        # Tax = 120.0 * 0.1 = 12.0
        # Total = 120.0 + 12.0 = 132.0
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 132.0)

    def test_calculate_total_with_discount_shipping_applies(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 100.0)  # Subtotal = 100.0
        # Discount = 0.1 (10%) -> Discounted Subtotal = 90.0
        # Shipping = 10.0 (since 90 < 100)
        # Amount before tax = 90.0 + 10.0 = 100.0
        # Tax = 100.0 * 0.2 = 20.0
        # Total = 100.0 + 20.0 = 120.0
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 120.0)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 120.0)  # Subtotal = 120.0
        # Discount = 0.1 (10%) -> Discounted Subtotal = 108.0
        # Shipping = 0.0 (since 108 >= 100)
        # Amount before tax = 108.0
        # Tax = 108.0 * 0.2 = 21.6
        # Total = 108.0 + 21.6 = 129.6
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 129.6)

    def test_calculate_total_one_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 50.0)  # Subtotal = 50.0
        # Discount = 1.0 (100%) -> Discounted Subtotal = 0.0
        # Shipping = 10.0 (since 0 < 100)
        # Amount before tax = 0.0 + 10.0 = 10.0
        # Tax = 10.0 * 0.2 = 2.0
        # Total = 10.0 + 2.0 = 12.0
        self.assertAlmostEqual(calc.calculate_total(discount=1.0), 12.0)

    def test_calculate_total_zero_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 50.0)
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 66.0)  # Same as no_discount_shipping_applies

    def test_calculate_total_zero_shipping_cost_setting(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=0.0)
        calc.add_item("ItemA", 50.0)  # Subtotal = 50.0
        # Discounted Subtotal = 50.0
        # Shipping = 0.0
        # Amount before tax = 50.0
        # Tax = 50.0 * 0.1 = 5.0
        # Total = 50.0 + 5.0 = 55.0
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 55.0)

    def test_calculate_total_zero_tax_rate_setting(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("ItemA", 50.0)  # Subtotal = 50.0
        # Discounted Subtotal = 50.0
        # Shipping = 10.0
        # Amount before tax = 60.0
        # Tax = 60.0 * 0.0 = 0.0
        # Total = 60.0 + 0.0 = 60.0
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 60.0)

    def test_calculate_total_complex_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item("Laptop", 150.0, quantity=1)  # 150.0
        calc.add_item("Mouse", 20.0, quantity=2)  # 40.0
        # Subtotal = 190.0
        # Discount = 0.05 (5%) -> Discounted Subtotal = 190.0 * 0.95 = 180.5
        # Shipping = 15.0 (since 180.5 < 200)
        # Amount before tax = 180.5 + 15.0 = 195.5
        # Tax = 195.5 * 0.23 = 44.965
        # Total = 195.5 + 44.965 = 240.465
        self.assertAlmostEqual(calc.calculate_total(discount=0.05), 240.465)

    # def test_calculate_total_raises_value_error_for_empty_order(self):
    #     calc = OrderCalculator()
    #     with self.assertRaisesRegex(ValueError, "Cannot calculate total for an empty order."):
    #         calc.calculate_total()

    def test_calculate_total_raises_value_error_for_invalid_discount_below_zero(self):
        calc = OrderCalculator()
        calc.add_item("ItemA", 10.0)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_raises_value_error_for_invalid_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item("ItemA", 10.0)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            calc.calculate_total(discount=1.1)

    # def test_calculate_total_raises_type_error_for_non_float_discount(self):
    #     calc = OrderCalculator()
    #     calc.add_item("ItemA", 10.0)
    #     with self.assertRaisesRegex(TypeError, "Discount must be a float."):
    #         calc.calculate_total(discount="0.1")  # type: ignore

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=2)
        calc.add_item("Banana", 0.3, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_item_manipulation(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=2)
        calc.add_item("Banana", 0.3, quantity=3)  # Total 5
        calc.remove_item("Apple")  # Total 3
        self.assertEqual(calc.total_items(), 3)
        calc.add_item("Cherry", 1.0, quantity=4)  # Total 7
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.items, [])
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        self.assertEqual(calc.list_items(), ["Apple"])

    # def test_list_items_multiple_unique_items(self):
    #     calc = OrderCalculator()
    #     calc.add_item("Banana", 0.3)  # Added Banana first for sorting check
    #     calc.add_item("Apple", 0.5)
    #     calc.add_item("Cherry", 0.2)
    #     self.assertEqual(calc.list_items(), ["Apple", "Banana", "Cherry"])  # Sorted

    def test_list_items_item_quantity_updated_shows_unique_name(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5, quantity=1)
        calc.add_item("Apple", 0.5, quantity=2)
        self.assertEqual(calc.list_items(), ["Apple"])

    # def test_list_items_after_item_manipulation(self):
    #     calc = OrderCalculator()
    #     calc.add_item("Banana", 0.3)
    #     calc.add_item("Apple", 0.5)
    #     calc.remove_item("Banana")
    #     self.assertEqual(calc.list_items(), ["Apple"])
    #     calc.add_item("Cherry", 0.2)
    #     self.assertEqual(calc.list_items(), ["Apple", "Cherry"])  # Sorted

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 0.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())


if __name__ == '__main__':
    unittest.main()