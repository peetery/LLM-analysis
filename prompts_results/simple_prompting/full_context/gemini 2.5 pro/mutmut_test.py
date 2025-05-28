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
#         if not isinstance(tax_rate, (float, int)):
#             raise TypeError("Tax rate must be a float or int.")
#         if not isinstance(free_shipping_threshold, (float, int)):
#             raise TypeError("Free shipping threshold must be a float or int.")
#         if not isinstance(shipping_cost, (float, int)):
#             raise TypeError("Shipping cost must be a float or int.")
#         if not 0.0 <= tax_rate <= 1.0:
#             raise ValueError("Tax rate must be between 0.0 and 1.0.")
#         if free_shipping_threshold < 0.0:
#             raise ValueError("Free shipping threshold cannot be negative.")
#         if shipping_cost < 0.0:
#             raise ValueError("Shipping cost cannot be negative.")
#
#         self.items: List[Item] = []
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = free_shipping_threshold
#         self.shipping_cost = shipping_cost
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not isinstance(price, (float, int)):
#             raise TypeError("Price must be a number.")
#         if not isinstance(quantity, int):
#             raise TypeError("Quantity must be an integer.")
#         if not name:
#             raise ValueError("Item name cannot be empty.")
#         if quantity < 1:
#             raise ValueError("Quantity must be at least 1.")
#         if price <= 0:
#             raise ValueError("Price must be greater than 0.")
#
#         for item in self.items:
#             if item["name"] == name:
#                 if item["price"] != price:
#                     raise ValueError("Item with the same name but different price already exists.")
#                 item["quantity"] += quantity
#                 return
#
#         self.items.append({
#             "name": name,
#             "price": price,
#             "quantity": quantity
#         })
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not any(item["name"] == name for item in self.items):
#             raise ValueError(f"Item with name '{name}' does not exist in the order.")
#
#         self.items = [item for item in self.items if item["name"] != name]
#
#     def get_subtotal(self) -> float:
#         if not self.items:
#             raise ValueError("Cannot calculate subtotal on empty order.")
#         return sum(item["price"] * item["quantity"] for item in self.items)
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (float, int)):
#             raise TypeError("Subtotal must be a number.")
#         if not isinstance(discount, (float, int)):
#             raise TypeError("Discount must be a number.")
#         if not 0.0 <= discount <= 1.0:
#             raise ValueError("Discount must be between 0.0 and 1.0.")
#         if subtotal < 0.0:
#             raise ValueError("Cannot apply discount on negative subtotal.")
#         return subtotal * (1 - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (float, int)):
#             raise TypeError("Discounted subtotal must be a number.")
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (float, int)):
#             raise TypeError("Amount must be a number.")
#         if amount < 0.0:
#             raise ValueError("Cannot calculate tax on negative amount.")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if not isinstance(discount, (float, int)):
#             raise TypeError("Discount must be a number.")
#
#         subtotal = self.get_subtotal()
#         if subtotal < 0.0:  # Should not happen with current add_item logic
#             raise ValueError("Cannot calculate total on negative subtotal.")
#         discounted_subtotal = self.apply_discount(subtotal, discount)
#         shipping_cost = self.calculate_shipping(discounted_subtotal)
#         tax = self.calculate_tax(discounted_subtotal + shipping_cost)
#         return discounted_subtotal + shipping_cost + tax
#
#     def total_items(self) -> int:
#         return sum(item["quantity"] for item in self.items)
#
#     def clear_order(self):
#         self.items = []
#
#     def list_items(self) -> List[str]:
#         return list(set(item["name"] for item in self.items))
#
#     def is_empty(self) -> bool:
#         return len(self.items) == 0


class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertEqual(calculator.items, [])

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_tax_rate_edge_cases(self):
        calculator_zero = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calculator_zero.tax_rate, 0.0)
        calculator_one = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calculator_one.tax_rate, 1.0)

    def test_init_free_shipping_threshold_edge_case(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calculator.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_edge_case(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calculator.shipping_cost, 0.0)

    def test_init_invalid_tax_rate_too_low(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaisesRegex(ValueError, "Free shipping threshold cannot be negative."):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaisesRegex(ValueError, "Shipping cost cannot be negative."):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaisesRegex(TypeError, "Tax rate must be a float or int."):
            OrderCalculator(tax_rate="0.23")

    def test_init_type_error_free_shipping_threshold(self):
        with self.assertRaisesRegex(TypeError, "Free shipping threshold must be a float or int."):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_type_error_shipping_cost(self):
        with self.assertRaisesRegex(TypeError, "Shipping cost must be a float or int."):
            OrderCalculator(shipping_cost="10")

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_add_item_new(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "apple")
        self.assertEqual(self.calculator.items[0]["price"], 1.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 2)

    def test_add_item_existing_increases_quantity(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.add_item("apple", 1.0, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 5)

    def test_add_item_default_quantity(self):
        self.calculator.add_item("banana", 0.5)
        self.assertEqual(self.calculator.items[0]["quantity"], 1)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaisesRegex(ValueError, "Item name cannot be empty."):
            self.calculator.add_item("", 1.0, 1)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaisesRegex(ValueError, "Price must be greater than 0."):
            self.calculator.add_item("apple", 0.0, 1)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaisesRegex(ValueError, "Price must be greater than 0."):
            self.calculator.add_item("apple", -1.0, 1)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be at least 1."):
            self.calculator.add_item("apple", 1.0, 0)

    def test_add_item_invalid_quantity_negative(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be at least 1."):
            self.calculator.add_item("apple", 1.0, -1)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item("apple", 1.0, 1)
        with self.assertRaisesRegex(ValueError, "Item with the same name but different price already exists."):
            self.calculator.add_item("apple", 1.5, 1)

    def test_add_item_type_error_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            self.calculator.add_item(123, 1.0, 1)

    def test_add_item_type_error_price(self):
        with self.assertRaisesRegex(TypeError, "Price must be a number."):
            self.calculator.add_item("apple", "1.0", 1)

    def test_add_item_type_error_quantity(self):
        with self.assertRaisesRegex(TypeError, "Quantity must be an integer."):
            self.calculator.add_item("apple", 1.0, "1")

    def test_remove_item_existing(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.add_item("banana", 0.5, 1)
        self.calculator.remove_item("apple")
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "banana")

    def test_remove_item_non_existing(self):
        self.calculator.add_item("apple", 1.0, 1)
        with self.assertRaisesRegex(ValueError, "Item with name 'banana' does not exist in the order."):
            self.calculator.remove_item("banana")

    def test_remove_item_type_error_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item("apple", 1.5, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("apple", 1.5, 2)  # 3.0
        self.calculator.add_item("banana", 0.5, 3)  # 1.5
        self.assertAlmostEqual(self.calculator.get_subtotal(), 4.5)

    def test_get_subtotal_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal on empty order."):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_zero_subtotal(self):
        self.assertAlmostEqual(self.calculator.apply_discount(0.0, 0.1), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaisesRegex(ValueError, "Cannot apply discount on negative subtotal."):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_too_low(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_too_high(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaisesRegex(TypeError, "Subtotal must be a number."):
            self.calculator.apply_discount("100.0", 0.1)

    def test_apply_discount_type_error_discount(self):
        with self.assertRaisesRegex(TypeError, "Discount must be a number."):
            self.calculator.apply_discount(100.0, "0.1")

    def test_calculate_shipping_below_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_threshold(self):
        self.calculator.free_shipping_threshold = 0.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_type_error_subtotal(self):
        with self.assertRaisesRegex(TypeError, "Discounted subtotal must be a number."):
            self.calculator.calculate_shipping("50.0")

    def test_calculate_tax_positive_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        self.calculator.tax_rate = 0.0
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 0.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate tax on negative amount."):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error_amount(self):
        with self.assertRaisesRegex(TypeError, "Amount must be a number."):
            self.calculator.calculate_tax("100.0")

    def test_calculate_total_no_discount_shipping_applies(self):
        # Subtotal = 50*0.5 = 25. Discounted = 25. Shipping = 10. Tax = (25+10)*0.23 = 35*0.23 = 8.05. Total = 25+10+8.05 = 43.05
        self.calculator.add_item("item1", 0.5, 50)  # Subtotal 25
        self.calculator.free_shipping_threshold = 30.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 43.05)

    def test_calculate_total_no_discount_free_shipping(self):
        # Subtotal = 120. Discounted = 120. Shipping = 0. Tax = 120*0.23 = 27.6. Total = 120+0+27.6 = 147.6
        self.calculator.add_item("item1", 1.0, 120)  # Subtotal 120
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 147.6)

    def test_calculate_total_with_discount_shipping_applies(self):
        # Subtotal = 80. Discounted = 80 * 0.9 = 72. Shipping = 10. Tax = (72+10)*0.23 = 82*0.23 = 18.86. Total = 72+10+18.86 = 100.86
        self.calculator.add_item("item1", 1.0, 80)  # Subtotal 80
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.1), 100.86)

    def test_calculate_total_with_discount_free_shipping(self):
        # Subtotal = 150. Discounted = 150 * 0.8 = 120. Shipping = 0. Tax = 120*0.23 = 27.6. Total = 120+0+27.6 = 147.6
        self.calculator.add_item("item1", 1.0, 150)  # Subtotal 150
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.2), 147.6)

    def test_calculate_total_zero_tax_rate(self):
        # Subtotal = 50. Discounted = 50. Shipping = 10. Tax = 0. Total = 50+10+0 = 60
        self.calculator.add_item("item1", 1.0, 50)
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.0
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 60.0)

    def test_calculate_total_full_discount(self):
        # Subtotal = 50. Discounted = 0. Shipping = 10 (threshold on discounted_subtotal). Tax = (0+10)*0.23 = 2.3. Total = 0+10+2.3 = 12.3
        self.calculator.add_item("item1", 1.0, 50)
        self.calculator.free_shipping_threshold = 1.0  # Ensure shipping applies if discounted_subtotal is 0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(1.0), 12.3)

    def test_calculate_total_full_discount_free_shipping(self):
        # Subtotal = 50. Discounted = 0. Shipping = 0 (threshold is 0). Tax = (0+0)*0.23 = 0. Total = 0+0+0 = 0
        self.calculator.add_item("item1", 1.0, 50)
        self.calculator.free_shipping_threshold = 0.0
        self.calculator.shipping_cost = 10.0
        self.calculator.tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(1.0), 0.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal on empty order."):
            self.calculator.calculate_total(0.1)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item("item1", 1.0, 10)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.calculate_total(1.1)

    def test_calculate_total_type_error_discount(self):
        self.calculator.add_item("item1", 1.0, 10)
        with self.assertRaisesRegex(TypeError, "Discount must be a number."):
            self.calculator.calculate_total("0.1")

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item_multiple_quantity(self):
        self.calculator.add_item("apple", 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.add_item("banana", 0.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_non_empty(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order_already_empty(self):
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single_item(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.assertEqual(self.calculator.list_items(), ["apple"])

    def test_list_items_multiple_items(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.add_item("banana", 0.5, 1)
        self.calculator.add_item("cherry", 2.0, 3)
        # Order might not be guaranteed due to set conversion, so check presence and length
        item_list = self.calculator.list_items()
        self.assertEqual(len(item_list), 3)
        self.assertIn("apple", item_list)
        self.assertIn("banana", item_list)
        self.assertIn("cherry", item_list)

    def test_list_items_duplicate_add_same_item(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.calculator.add_item("apple", 1.0, 3)  # Increases quantity, not a new item type
        self.assertEqual(self.calculator.list_items(), ["apple"])

    def test_is_empty_new_order(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_with_items(self):
        self.calculator.add_item("apple", 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calculator.add_item("apple", 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_removing_last_item(self):
        self.calculator.add_item("apple", 1.0, 1)
        self.calculator.remove_item("apple")
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)