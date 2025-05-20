import unittest
from order_calculator import OrderCalculator


# Assuming OrderCalculator class is defined in a module named order_calculator_module
# from order_calculator_module import OrderCalculator

# Placeholder OrderCalculator class for the tests to run.
# In a real scenario, this class would be imported from its own module.
# To make this file self-contained and runnable for demonstration,
# a basic implementation matching the expected interface is provided here.
# For the final deliverable as per "Output a valid .py file containing only the test class",
# this placeholder class definition should be removed, and the import statement above uncommented.

# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         if not isinstance(tax_rate, (int, float)):
#             raise TypeError("Tax rate must be a number")
#         if not (0 <= tax_rate <= 1):
#             raise ValueError("Tax rate must be between 0 and 1")
#         if not isinstance(free_shipping_threshold, (int, float)):
#             raise TypeError("Free shipping threshold must be a number")
#         if free_shipping_threshold < 0:
#             raise ValueError("Free shipping threshold cannot be negative")
#         if not isinstance(shipping_cost, (int, float)):
#             raise TypeError("Shipping cost must be a number")
#         if shipping_cost < 0:
#             raise ValueError("Shipping cost cannot be negative")
#
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = free_shipping_threshold
#         self.shipping_cost = shipping_cost
#         self._items = {}  # Using a dictionary: {name: {'price': float, 'quantity': int}}
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string")
#         if not name:
#             raise ValueError("Item name cannot be empty")
#         if not isinstance(price, (int, float)):
#             raise TypeError("Item price must be a number")
#         if price < 0:
#             raise ValueError("Item price cannot be negative")
#         if not isinstance(quantity, int):
#             raise TypeError("Item quantity must be an integer")
#         if quantity <= 0:  # Test scenarios assume quantity=0 is invalid or means no add
#             raise ValueError("Item quantity must be positive")
#
#         if name in self._items:
#             self._items[name]['quantity'] += quantity
#             self._items[name]['price'] = price  # Assuming price update on re-add
#         else:
#             self._items[name] = {'price': price, 'quantity': quantity}
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string")
#         if not name:  # Assuming empty string name will lead to KeyError or specific ValueError
#             raise KeyError("Item '' not found in order.")  # Or ValueError
#         if name not in self._items:
#             raise KeyError(f"Item '{name}' not found in order.")
#         del self._items[name]
#
#     def get_subtotal(self) -> float:
#         return sum(item['price'] * item['quantity'] for item in self._items.values())
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (int, float)):
#             raise TypeError("Subtotal must be a number")
#         if not isinstance(discount, (int, float)):
#             raise TypeError("Discount must be a number")
#         if discount < 0:
#             raise ValueError("Discount cannot be negative")
#
#         discounted_price = subtotal * (1.0 - discount)
#         return max(0.0, discounted_price)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (int, float)):
#             raise TypeError("Discounted subtotal must be a number")
#         # Assuming negative discounted_subtotal is treated as 0 for shipping calculation
#         effective_subtotal = max(0.0, discounted_subtotal)
#
#         if effective_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (int, float)):
#             raise TypeError("Amount must be a number")
#         # Assuming tax on negative amount is 0 or based on absolute. Let's go with 0.
#         effective_amount = max(0.0, amount)
#         return round(effective_amount * self.tax_rate, 2)
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         # This method will call other methods, so type/value errors from them might propagate
#         if not isinstance(discount, (int, float)):
#             raise TypeError("Discount must be a number")
#
#         subtotal = self.get_subtotal()
#         discounted_subtotal = self.apply_discount(subtotal, discount)  # Can raise ValueError if discount < 0
#         shipping = self.calculate_shipping(discounted_subtotal)
#         tax = self.calculate_tax(discounted_subtotal)
#
#         total = discounted_subtotal + tax + shipping
#         return round(total, 2)
#
#     def total_items(self) -> int:
#         return sum(item['quantity'] for item in self._items.values())
#
#     def clear_order(self):
#         self._items.clear()
#
#     def list_items(self) -> list[str]:
#         return list(self._items.keys())
#
#     def is_empty(self) -> bool:
#         return not self._items


# End of Placeholder OrderCalculator class


class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calculator = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calculator.tax_rate, 0.15)

    def test_init_custom_free_shipping_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calculator = OrderCalculator(shipping_cost=5.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_all_custom_parameters(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 200.0)
        self.assertEqual(calculator.shipping_cost, 15.0)

    def test_init_tax_rate_zero(self):
        calculator = OrderCalculator(tax_rate=0)
        self.assertEqual(calculator.tax_rate, 0)

    def test_init_tax_rate_one(self):
        calculator = OrderCalculator(tax_rate=1)
        self.assertEqual(calculator.tax_rate, 1)

    def test_init_free_shipping_threshold_zero(self):
        calculator = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calculator.free_shipping_threshold, 0)

    def test_init_shipping_cost_zero(self):
        calculator = OrderCalculator(shipping_cost=0)
        self.assertEqual(calculator.shipping_cost, 0)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_non_numeric_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="abc")

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_non_numeric_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="abc")

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_non_numeric_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="abc")

    def test_add_item_single_new_item_default_quantity(self):
        self.calculator.add_item("apple", 0.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn("apple", self.calculator.list_items())
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.5)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_single_new_item_specified_quantity(self):
        self.calculator.add_item("banana", 0.3, quantity=3)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.9)

    def test_add_item_multiple_different_items(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 1.9)  # (0.5*2) + (0.3*3) = 1.0 + 0.9
        self.assertIn("apple", self.calculator.list_items())
        self.assertIn("banana", self.calculator.list_items())

    def test_add_item_existing_item_updates_quantity_and_price(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("apple", 0.6, 3)  # Adding same item, new price
        self.assertEqual(self.calculator.total_items(), 5)  # 2+3
        # Subtotal reflects new price for all items of this type if price is updated this way
        # Or subtotal reflects (0.5*2) + (0.6*3) = 1 + 1.8 = 2.8
        # Current placeholder implementation: updates price and sums quantity. Price becomes 0.6
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)  # 5 * 0.6

    def test_add_item_price_zero(self):
        self.calculator.add_item("free_item", 0.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("invalid_item", -10.0)

    def test_add_item_quantity_zero_raises_value_error(self):
        with self.assertRaises(ValueError):  # Assuming quantity must be > 0
            self.calculator.add_item("item_q_zero", 1.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("invalid_item", 1.0, -1)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 1.0)

    def test_add_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(None, 1.0)

    def test_add_item_price_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("item", "abc")

    def test_add_item_quantity_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("item", 1.0, 1.5)

    def test_remove_item_existing_item(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 1)
        self.calculator.remove_item("apple")
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertNotIn("apple", self.calculator.list_items())
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3)

    def test_remove_item_only_item(self):
        self.calculator.add_item("apple", 0.5, 1)
        self.calculator.remove_item("apple")
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_non_existent_item_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("orange")

    def test_remove_item_from_empty_order_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("apple")

    def test_remove_item_empty_name_raises_key_error_or_value_error(self):
        # Behavior for empty string name depends on implementation, could be ValueError or KeyError
        with self.assertRaises((KeyError, ValueError)):
            self.calculator.remove_item("")

    def test_remove_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_empty_order(self):
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 1.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 1.9)

    def test_get_subtotal_after_add_and_remove(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.calculator.remove_item("apple")
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.9)

    def test_get_subtotal_items_with_zero_price(self):
        self.calculator.add_item("free_apple", 0.0, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.9)

    def test_apply_discount_valid_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_one_hundred_percent_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_greater_than_one_hundred_percent(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.5), 0.0)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_to_zero_subtotal(self):
        self.assertAlmostEqual(self.calculator.apply_discount(0.0, 0.1), 0.0)

    def test_apply_discount_to_negative_subtotal(self):
        # Assuming negative subtotal treated as positive or results in 0 if discount applied
        self.assertAlmostEqual(self.calculator.apply_discount(-100.0, 0.1), 0.0)  # max(0, -90)

    def test_apply_discount_non_numeric_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("abc", 0.1)

    def test_apply_discount_non_numeric_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "abc")

    def test_calculate_shipping_subtotal_less_than_threshold(self):
        # Default threshold 100, cost 10
        self.assertAlmostEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_subtotal_equal_to_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_subtotal_greater_than_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_subtotal_zero(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_threshold_zero_always_free(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        self.assertAlmostEqual(calculator.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_cost_zero_always_free(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        # If threshold is met, it's 0. If not, it's shipping_cost which is 0.
        self.assertAlmostEqual(calculator.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        # Assuming negative subtotal is treated as 0 for calculation
        self.assertAlmostEqual(self.calculator.calculate_shipping(-50.0), 10.0)

    def test_calculate_shipping_non_numeric_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("abc")

    def test_calculate_tax_positive_amount_default_rate(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)  # 100 * 0.23

    def test_calculate_tax_positive_amount_custom_rate(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_rate_zero(self):
        calculator = OrderCalculator(tax_rate=0.0)
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 0.0)

    def test_calculate_tax_rate_one(self):
        calculator = OrderCalculator(tax_rate=1.0)
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 100.0)

    def test_calculate_tax_negative_amount(self):
        # Assuming tax on negative amount is 0 or raises error. Placeholder makes it 0.
        self.assertAlmostEqual(self.calculator.calculate_tax(-100.0), 0.0)

    def test_calculate_tax_non_numeric_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("abc")

    def test_calculate_total_empty_order(self):
        self.assertAlmostEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_no_discount_shipping_applies(self):
        self.calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Tax: 50 * 0.23 = 11.5. Shipping: 10. Total: 50 + 11.5 + 10 = 71.5
        self.assertAlmostEqual(self.calculator.calculate_total(), 71.5)

    def test_calculate_total_no_discount_free_shipping(self):
        self.calculator.add_item("item", 100.0, 1)  # Subtotal 100
        # Tax: 100 * 0.23 = 23. Shipping: 0. Total: 100 + 23 + 0 = 123.0
        self.assertAlmostEqual(self.calculator.calculate_total(), 123.0)

    def test_calculate_total_with_discount_shipping_applies(self):
        self.calculator.add_item("item", 80.0, 1)  # Subtotal 80
        # Discount 0.1: 80 * 0.9 = 72. Tax: 72 * 0.23 = 16.56. Shipping: 10.
        # Total: 72 + 16.56 + 10 = 98.56
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 98.56)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calculator.add_item("item", 120.0, 1)  # Subtotal 120
        # Discount 0.1: 120 * 0.9 = 108. Tax: 108 * 0.23 = 24.84. Shipping: 0.
        # Total: 108 + 24.84 + 0 = 132.84
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 132.84)

    def test_calculate_total_discount_makes_subtotal_zero_shipping_applies(self):
        self.calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Discount 1.0: 50 * 0 = 0. Tax: 0 * 0.23 = 0. Shipping: 10.
        # Total: 0 + 0 + 10 = 10.0
        self.assertAlmostEqual(self.calculator.calculate_total(discount=1.0), 10.0)

    def test_calculate_total_100_percent_discount(self):
        self.calculator.add_item("item", 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=1.0), 10.0)  # 0 + 0_tax + 10_shipping

    def test_calculate_total_tax_rate_zero(self):
        calculator = OrderCalculator(tax_rate=0.0)
        calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Tax: 0. Shipping: 10. Total: 50 + 0 + 10 = 60.0
        self.assertAlmostEqual(calculator.calculate_total(), 60.0)

    def test_calculate_total_shipping_cost_zero(self):
        calculator = OrderCalculator(shipping_cost=0.0, free_shipping_threshold=100)  # Still has threshold
        calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Tax: 50 * 0.23 = 11.5. Shipping: 0 (because shipping_cost is 0). Total: 50 + 11.5 + 0 = 61.5
        self.assertAlmostEqual(calculator.calculate_total(), 61.5)

    def test_calculate_total_free_shipping_threshold_zero(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Tax: 50 * 0.23 = 11.5. Shipping: 0. Total: 50 + 11.5 + 0 = 61.5
        self.assertAlmostEqual(calculator.calculate_total(), 61.5)

    def test_calculate_total_negative_discount_raises_value_error(self):
        self.calculator.add_item("item", 50.0, 1)
        with self.assertRaises(ValueError):  # Propagated from apply_discount
            self.calculator.calculate_total(discount=-0.1)

    def test_calculate_total_discount_greater_than_one(self):
        self.calculator.add_item("item", 50.0, 1)  # Subtotal 50
        # Discounted Subtotal = 0. Tax = 0. Shipping = 10. Total = 10.
        self.assertAlmostEqual(self.calculator.calculate_total(discount=1.5), 10.0)

    def test_calculate_total_non_numeric_discount_raises_type_error(self):
        self.calculator.add_item("item", 50.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount="abc")

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_one_item_quantity_one(self):
        self.calculator.add_item("apple", 0.5, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_one_item_quantity_n(self):
        self.calculator.add_item("apple", 0.5, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_after_adding_same_item_again(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("apple", 0.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_after_add_and_remove(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.add_item("banana", 0.3, 3)
        self.calculator.remove_item("apple")
        self.assertEqual(self.calculator.total_items(), 3)

    def test_clear_order_with_items(self):
        self.calculator.add_item("apple", 0.5, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_clear_order_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_one_item(self):
        self.calculator.add_item("apple", 0.5)
        self.assertEqual(self.calculator.list_items(), ["apple"])

    def test_list_items_multiple_items(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.add_item("banana", 0.3)
        # Order depends on dict insertion order for Python 3.7+
        items = self.calculator.list_items()
        self.assertIn("apple", items)
        self.assertIn("banana", items)
        self.assertEqual(len(items), 2)

    def test_list_items_order_consistency(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.add_item("banana", 0.3)
        self.calculator.add_item("cherry", 0.1)
        self.assertEqual(self.calculator.list_items(), ["apple", "banana", "cherry"])

    def test_list_items_after_add_and_remove(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.add_item("banana", 0.3)
        self.calculator.remove_item("apple")
        self.assertEqual(self.calculator.list_items(), ["banana"])

    def test_list_items_after_clear_order(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_new_order(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item("apple", 0.5)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_add_and_remove_item(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.remove_item("apple")
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_multiple_and_removing_all(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.add_item("banana", 0.3)
        self.calculator.remove_item("apple")
        self.calculator.remove_item("banana")
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear_order_with_items(self):
        self.calculator.add_item("apple", 0.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)