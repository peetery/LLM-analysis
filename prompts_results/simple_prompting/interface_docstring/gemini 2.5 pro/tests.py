import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator

# class Item(TypedDict):
#     name: str
#     price: float
#     quantity: int
#
# # Minimal OrderCalculator implementation for tests to run
# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         if not isinstance(tax_rate, (int, float)):
#              raise TypeError("tax_rate must be a number.")
#         if not (0.0 <= tax_rate <= 1.0):
#             raise ValueError("tax_rate must be between 0.0 and 1.0.")
#         if not isinstance(free_shipping_threshold, (int, float)):
#              raise TypeError("free_shipping_threshold must be a number.")
#         if free_shipping_threshold < 0:
#             raise ValueError("free_shipping_threshold cannot be negative.")
#         if not isinstance(shipping_cost, (int, float)):
#              raise TypeError("shipping_cost must be a number.")
#         if shipping_cost < 0:
#             raise ValueError("shipping_cost cannot be negative.")
#
#         self.tax_rate = float(tax_rate)
#         self.free_shipping_threshold = float(free_shipping_threshold)
#         self.shipping_cost = float(shipping_cost)
#         self._items: List[Item] = []
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not name:
#             raise ValueError("Item name cannot be empty.")
#         if not isinstance(price, (int, float)):
#             raise TypeError("Item price must be a number.")
#         if price <= 0:
#             raise ValueError("Item price must be positive.")
#         if not isinstance(quantity, int):
#              raise TypeError("Item quantity must be an integer.")
#         if quantity < 1:
#             raise ValueError("Item quantity must be at least 1.")
#
#         existing_item = next((item for item in self._items if item['name'] == name), None)
#
#         if existing_item:
#             if existing_item['price'] != price:
#                 raise ValueError(f"Item '{name}' already exists with a different price ({existing_item['price']} vs {price}).")
#             existing_item['quantity'] += quantity
#         else:
#             self._items.append({'name': name, 'price': float(price), 'quantity': quantity})
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         initial_len = len(self._items)
#         self._items = [item for item in self._items if item['name'] != name]
#         if len(self._items) == initial_len:
#              raise ValueError(f"Item '{name}' not found in the order.")
#
#     def get_subtotal(self) -> float:
#         if not self._items:
#              raise ValueError("Cannot calculate subtotal for an empty order.")
#         return sum(item['price'] * item['quantity'] for item in self._items)
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (int, float)):
#             raise TypeError("Subtotal must be a number.")
#         if subtotal < 0:
#             raise ValueError("Subtotal cannot be negative.")
#         if not isinstance(discount, (int, float)):
#              raise TypeError("Discount must be a number.")
#         if not (0.0 <= discount <= 1.0):
#             raise ValueError("Discount must be between 0.0 and 1.0.")
#         return subtotal * (1.0 - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (int, float)):
#              raise TypeError("Discounted subtotal must be a number.")
#         # Docstring doesn't explicitly require non-negative, but implies it.
#         # We'll rely on apply_discount validation.
#         # if discounted_subtotal < 0:
#         #    raise ValueError("Discounted subtotal cannot be negative.")
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         else:
#             return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (int, float)):
#              raise TypeError("Amount must be a number.")
#         if amount < 0:
#              raise ValueError("Amount cannot be negative.")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if not self._items:
#             raise ValueError("Cannot calculate total for an empty order.")
#         if not isinstance(discount, (int, float)):
#             raise TypeError("Discount must be a number.")
#         if not (0.0 <= discount <= 1.0):
#              raise ValueError("Discount must be between 0.0 and 1.0.")
#
#         subtotal = self.get_subtotal()
#         if subtotal < 0: # Should not happen if add_item works correctly
#              raise ValueError("Subtotal cannot be negative.")
#
#         discounted_subtotal = self.apply_discount(subtotal, discount)
#         shipping = self.calculate_shipping(discounted_subtotal)
#         amount_before_tax = discounted_subtotal + shipping
#         tax = self.calculate_tax(amount_before_tax)
#         total = amount_before_tax + tax
#         return total
#
#     def total_items(self) -> int:
#         return sum(item['quantity'] for item in self._items)
#
#     def clear_order(self):
#         self._items = []
#
#     def list_items(self) -> List[str]:
#         return [item['name'] for item in self._items]
#
#     def is_empty(self) -> bool:
#         return not self._items

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()
        self.item1 = {"name": "Apple", "price": 1.5, "quantity": 2}
        self.item2 = {"name": "Banana", "price": 0.75, "quantity": 4}
        self.item3 = {"name": "Orange", "price": 2.0, "quantity": 1}

    # --- __init__ tests ---

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator._items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)
        self.assertEqual(calc._items, [])

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaisesRegex(ValueError, "tax_rate must be between 0.0 and 1.0"):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaisesRegex(ValueError, "tax_rate must be between 0.0 and 1.0"):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_negative(self):
        with self.assertRaisesRegex(ValueError, "free_shipping_threshold cannot be negative"):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaisesRegex(ValueError, "shipping_cost cannot be negative"):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaisesRegex(TypeError, "tax_rate must be a number"):
            OrderCalculator(tax_rate="0.2")

    def test_init_invalid_type_free_shipping_threshold(self):
        with self.assertRaisesRegex(TypeError, "free_shipping_threshold must be a number"):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaisesRegex(TypeError, "shipping_cost must be a number"):
            OrderCalculator(shipping_cost="10")

    # --- add_item tests ---

    def test_add_item_new(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.assertEqual(len(self.calculator._items), 1)
        self.assertEqual(self.calculator._items[0], {"name": "Apple", "price": 1.5, "quantity": 2})

    def test_add_item_default_quantity(self):
        self.calculator.add_item("Banana", 0.75)
        self.assertEqual(len(self.calculator._items), 1)
        self.assertEqual(self.calculator._items[0], {"name": "Banana", "price": 0.75, "quantity": 1})

    def test_add_item_existing_increases_quantity(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(len(self.calculator._items), 1)
        self.assertEqual(self.calculator._items[0]['quantity'], 5)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaisesRegex(ValueError, "Item name cannot be empty"):
            self.calculator.add_item("", 1.0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaisesRegex(ValueError, "Item price must be positive"):
            self.calculator.add_item("Apple", 0)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaisesRegex(ValueError, "Item price must be positive"):
            self.calculator.add_item("Apple", -1.0)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaisesRegex(ValueError, "Item quantity must be at least 1"):
            self.calculator.add_item("Apple", 1.0, 0)

    def test_add_item_invalid_quantity_negative(self):
        with self.assertRaisesRegex(ValueError, "Item quantity must be at least 1"):
            self.calculator.add_item("Apple", 1.0, -1)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item("Apple", 1.5)
        with self.assertRaisesRegex(ValueError, "already exists with a different price"):
            self.calculator.add_item("Apple", 2.0)

    def test_add_item_invalid_type_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string"):
            self.calculator.add_item(123, 1.0) # type: ignore

    def test_add_item_invalid_type_price(self):
        with self.assertRaisesRegex(TypeError, "Item price must be a number"):
            self.calculator.add_item("Apple", "1.5") # type: ignore

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaisesRegex(TypeError, "Item quantity must be an integer"):
            self.calculator.add_item("Apple", 1.0, 1.5) # type: ignore

    # --- remove_item tests ---

    def test_remove_item_existing(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item(**self.item2)
        self.calculator.remove_item("Apple")
        self.assertEqual(len(self.calculator._items), 1)
        self.assertEqual(self.calculator._items[0]['name'], "Banana")

    def test_remove_item_non_existent(self):
        self.calculator.add_item(**self.item1)
        with self.assertRaisesRegex(ValueError, "Item 'Orange' not found"):
            self.calculator.remove_item("Orange")

    def test_remove_item_from_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Item 'Apple' not found"):
            self.calculator.remove_item("Apple")

    def test_remove_item_invalid_type_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string"):
            self.calculator.remove_item(123) # type: ignore

    # --- get_subtotal tests ---

    def test_get_subtotal_one_item(self):
        self.calculator.add_item(**self.item1) # name="Apple", price=1.5, quantity=2
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item(**self.item1) # 1.5 * 2 = 3.0
        self.calculator.add_item(**self.item2) # 0.75 * 4 = 3.0
        self.assertAlmostEqual(self.calculator.get_subtotal(), 6.0)

    def test_get_subtotal_after_removal(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item(**self.item2)
        self.calculator.remove_item("Apple")
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0) # Only Banana left

    def test_get_subtotal_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal for an empty order"):
            self.calculator.get_subtotal()

    # --- apply_discount tests ---

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)
        self.assertAlmostEqual(self.calculator.apply_discount(50.0, 0.25), 37.5)

    def test_apply_discount_zero_percent(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_hundred_percent(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaisesRegex(ValueError, "Subtotal cannot be negative"):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_negative(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0"):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_above_one(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0"):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_type_subtotal(self):
        with self.assertRaisesRegex(TypeError, "Subtotal must be a number"):
            self.calculator.apply_discount("100", 0.1) # type: ignore

    def test_apply_discount_invalid_type_discount(self):
        with self.assertRaisesRegex(TypeError, "Discount must be a number"):
            self.calculator.apply_discount(100.0, "0.1") # type: ignore

    # --- calculate_shipping tests ---

    def test_calculate_shipping_below_threshold(self):
        # Default threshold = 100.0, cost = 10.0
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
         self.assertEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_custom_calculator(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)
        self.assertEqual(calc.calculate_shipping(50.00), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaisesRegex(TypeError, "Discounted subtotal must be a number"):
            self.calculator.calculate_shipping("100") # type: ignore

    # Although not explicitly in docstring, negative subtotal after discount is unlikely
    # but let's test the negative case if the method supports it internally
    # def test_calculate_shipping_negative_subtotal(self):
    #     # Behavior depends on implementation, assuming it defaults to standard cost
    #     self.assertEqual(self.calculator.calculate_shipping(-10.0), 10.0)


    # --- calculate_tax tests ---

    def test_calculate_tax_positive_amount(self):
        # Default tax_rate = 0.23
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaisesRegex(ValueError, "Amount cannot be negative"):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type_amount(self):
        with self.assertRaisesRegex(TypeError, "Amount must be a number"):
            self.calculator.calculate_tax("100") # type: ignore

    # --- calculate_total tests ---

    def test_calculate_total_no_discount_below_shipping_threshold(self):
        self.calculator.add_item("A", 50.0, 1) # Subtotal = 50.0
        # Discounted = 50.0
        # Shipping = 10.0
        # Taxable = 50.0 + 10.0 = 60.0
        # Tax = 60.0 * 0.23 = 13.8
        # Total = 60.0 + 13.8 = 73.8
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_no_discount_above_shipping_threshold(self):
        self.calculator.add_item("A", 100.0, 1) # Subtotal = 100.0
        # Discounted = 100.0
        # Shipping = 0.0
        # Taxable = 100.0 + 0.0 = 100.0
        # Tax = 100.0 * 0.23 = 23.0
        # Total = 100.0 + 23.0 = 123.0
        self.assertAlmostEqual(self.calculator.calculate_total(), 123.0)

    def test_calculate_total_with_discount_below_shipping_threshold(self):
        self.calculator.add_item("A", 120.0, 1) # Subtotal = 120.0
        discount = 0.2 # 20%
        # Discounted = 120.0 * (1 - 0.2) = 96.0
        # Shipping = 10.0 (since 96.0 < 100.0)
        # Taxable = 96.0 + 10.0 = 106.0
        # Tax = 106.0 * 0.23 = 24.38
        # Total = 106.0 + 24.38 = 130.38
        self.assertAlmostEqual(self.calculator.calculate_total(discount=discount), 130.38)

    def test_calculate_total_with_discount_above_shipping_threshold(self):
        self.calculator.add_item("A", 150.0, 1) # Subtotal = 150.0
        discount = 0.2 # 20%
        # Discounted = 150.0 * (1 - 0.2) = 120.0
        # Shipping = 0.0 (since 120.0 >= 100.0)
        # Taxable = 120.0 + 0.0 = 120.0
        # Tax = 120.0 * 0.23 = 27.6
        # Total = 120.0 + 27.6 = 147.6
        self.assertAlmostEqual(self.calculator.calculate_total(discount=discount), 147.6)

    def test_calculate_total_hundred_percent_discount(self):
         self.calculator.add_item("A", 50.0, 1) # Subtotal = 50.0
         # Discounted = 0.0
         # Shipping = 10.0 (since 0.0 < 100.0)
         # Taxable = 0.0 + 10.0 = 10.0
         # Tax = 10.0 * 0.23 = 2.3
         # Total = 10.0 + 2.3 = 12.3
         # NOTE: This assumes tax is applied even if items are free but shipping is paid.
         #       If tax should be 0 when discounted subtotal is 0, this test needs adjustment.
         #       The current implementation calculates tax on (discounted_subtotal + shipping).
         self.assertAlmostEqual(self.calculator.calculate_total(discount=1.0), 12.3)

    def test_calculate_total_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate total for an empty order"):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_negative(self):
        self.calculator.add_item("A", 10.0)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0"):
            self.calculator.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_above_one(self):
        self.calculator.add_item("A", 10.0)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0"):
            self.calculator.calculate_total(discount=1.1)

    def test_calculate_total_invalid_type_discount(self):
        self.calculator.add_item("A", 10.0)
        with self.assertRaisesRegex(TypeError, "Discount must be a number"):
            self.calculator.calculate_total(discount="0.1") # type: ignore

    # --- total_items tests ---

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_one_item_quantity_one(self):
        self.calculator.add_item("A", 1.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_one_item_quantity_multiple(self):
        self.calculator.add_item("A", 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item(**self.item1) # quantity=2
        self.calculator.add_item(**self.item2) # quantity=4
        self.assertEqual(self.calculator.total_items(), 6)

    def test_total_items_after_add_and_remove(self):
        self.calculator.add_item(**self.item1) # quantity=2
        self.calculator.add_item(**self.item2) # quantity=4
        self.calculator.add_item("Apple", 1.5, 3) # quantity becomes 2+3=5
        self.calculator.remove_item("Banana")
        self.assertEqual(self.calculator.total_items(), 5) # Only Apple left

    # --- clear_order tests ---

    def test_clear_order_with_items(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item(**self.item2)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_clear_order_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.list_items(), [])

    # --- list_items tests ---

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_one_item(self):
        self.calculator.add_item(**self.item1)
        self.assertEqual(self.calculator.list_items(), ["Apple"])

    def test_list_items_multiple_items(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item(**self.item2)
        # Order might not be guaranteed, so check set equality
        self.assertCountEqual(self.calculator.list_items(), ["Apple", "Banana"])

    def test_list_items_after_duplicate_add(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item("Apple", 1.5, 3) # Add more Apples
        self.assertEqual(self.calculator.list_items(), ["Apple"]) # Only one entry for "Apple"

    def test_list_items_after_removal(self):
        self.calculator.add_item(**self.item1)
        self.calculator.add_item(**self.item2)
        self.calculator.remove_item("Apple")
        self.assertEqual(self.calculator.list_items(), ["Banana"])

    # --- is_empty tests ---

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item(**self.item1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_add_and_remove_all(self):
        self.calculator.add_item(**self.item1)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item(**self.item1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)