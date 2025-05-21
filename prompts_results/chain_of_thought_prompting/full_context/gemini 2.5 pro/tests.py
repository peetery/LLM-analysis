import unittest
from decimal import Decimal, ROUND_HALF_UP

# Assuming the OrderCalculator class and Item TypedDict are in a file named order_calculator_module.py
# If you have the class in the same file, you might not need this import.
from order_calculator import OrderCalculator, Item


class TestOrderCalculator(unittest.TestCase):

    def assertFloatAlmostEqual(self, a, b, places=7):
        # Helper for comparing floats, especially after calculations involving currency
        # Using Decimal for more robust financial comparisons
        # Python's round() can have surprising behavior with .5, Decimal is more controllable
        decimal_a = Decimal(str(a)).quantize(Decimal('1e-{}'.format(places)), rounding=ROUND_HALF_UP)
        decimal_b = Decimal(str(b)).quantize(Decimal('1e-{}'.format(places)), rounding=ROUND_HALF_UP)
        self.assertEqual(decimal_a, decimal_b)

    # 1. __init__
    def test_init_default_parameters(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertEqual(calculator.items, [])

    def test_init_custom_valid_floats(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.5, shipping_cost=5.5)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.5)
        self.assertEqual(calculator.shipping_cost, 5.5)

    def test_init_custom_valid_integers(self):
        calculator = OrderCalculator(tax_rate=0, free_shipping_threshold=50, shipping_cost=5)
        self.assertEqual(calculator.tax_rate, 0)
        self.assertEqual(calculator.free_shipping_threshold, 50)
        self.assertEqual(calculator.shipping_cost, 5)

    def test_init_edge_case_tax_rate_zero(self):
        calculator = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calculator.tax_rate, 0.0)

    def test_init_edge_case_tax_rate_one(self):
        calculator = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calculator.tax_rate, 1.0)

    def test_init_edge_case_free_shipping_threshold_zero(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calculator.free_shipping_threshold, 0.0)

    def test_init_edge_case_shipping_cost_zero(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calculator.shipping_cost, 0.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaisesRegex(ValueError, "Tax rate must be between 0.0 and 1.0."):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_negative(self):
        with self.assertRaisesRegex(ValueError, "Free shipping threshold cannot be negative."):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaisesRegex(ValueError, "Shipping cost cannot be negative."):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaisesRegex(TypeError, "Tax rate must be a float or int."):
            OrderCalculator(tax_rate="0.23")

    def test_init_invalid_type_free_shipping_threshold(self):
        with self.assertRaisesRegex(TypeError, "Free shipping threshold must be a float or int."):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaisesRegex(TypeError, "Shipping cost must be a float or int."):
            OrderCalculator(shipping_cost="10")

    # 2. add_item
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_add_item_new_default_quantity(self):
        self.calculator.add_item("Apple", 0.5)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {"name": "Apple", "price": 0.5, "quantity": 1})

    def test_add_item_new_specified_quantity(self):
        self.calculator.add_item("Banana", 0.3, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {"name": "Banana", "price": 0.3, "quantity": 3})

    def test_add_item_multiple_distinct_items(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.add_item("Banana", 0.3, 2)
        self.assertEqual(len(self.calculator.items), 2)
        self.assertIn({"name": "Apple", "price": 0.5, "quantity": 1}, self.calculator.items)
        self.assertIn({"name": "Banana", "price": 0.3, "quantity": 2}, self.calculator.items)

    def test_add_item_existing_updates_quantity(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.calculator.add_item("Apple", 0.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 5)

    def test_add_item_price_as_integer(self):
        self.calculator.add_item("Cherry", 2, 2)  # price is int
        self.assertEqual(self.calculator.items[0], {"name": "Cherry", "price": 2, "quantity": 2})

    def test_add_item_invalid_name_empty(self):
        with self.assertRaisesRegex(ValueError, "Item name cannot be empty."):
            self.calculator.add_item("", 1.0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaisesRegex(ValueError, "Price must be greater than 0."):
            self.calculator.add_item("Apple", 0.0)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaisesRegex(ValueError, "Price must be greater than 0."):
            self.calculator.add_item("Apple", -1.0)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be at least 1."):
            self.calculator.add_item("Apple", 1.0, 0)

    def test_add_item_invalid_quantity_negative(self):
        with self.assertRaisesRegex(ValueError, "Quantity must be at least 1."):
            self.calculator.add_item("Apple", 1.0, -1)

    def test_add_item_conflicting_price(self):
        self.calculator.add_item("Apple", 1.0)
        with self.assertRaisesRegex(ValueError, "Item with the same name but different price already exists."):
            self.calculator.add_item("Apple", 1.5)

    def test_add_item_invalid_type_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            self.calculator.add_item(123, 1.0)

    def test_add_item_invalid_type_price(self):
        with self.assertRaisesRegex(TypeError, "Price must be a number."):
            self.calculator.add_item("Apple", "1.0")

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaisesRegex(TypeError, "Quantity must be an integer."):
            self.calculator.add_item("Apple", 1.0, 1.5)

    # 3. remove_item
    def test_remove_item_existing(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.add_item("Banana", 0.3)
        self.calculator.remove_item("Apple")
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Banana")

    def test_remove_item_only_item(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        self.calculator.add_item("Apple", 0.5)
        with self.assertRaisesRegex(ValueError, "Item with name 'Banana' does not exist in the order."):
            self.calculator.remove_item("Banana")

    def test_remove_item_from_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Item with name 'Apple' does not exist in the order."):
            self.calculator.remove_item("Apple")

    def test_remove_item_invalid_type_name(self):
        with self.assertRaisesRegex(TypeError, "Item name must be a string."):
            self.calculator.remove_item(123)

    # 4. get_subtotal
    def test_get_subtotal_single_item(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.assertFloatAlmostEqual(self.calculator.get_subtotal(), 1.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Apple", 0.5, 2)  # 1.0
        self.calculator.add_item("Banana", 0.3, 3)  # 0.9
        self.assertFloatAlmostEqual(self.calculator.get_subtotal(), 1.9)

    def test_get_subtotal_after_item_removal(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.calculator.add_item("Banana", 0.3, 3)
        self.calculator.remove_item("Apple")
        self.assertFloatAlmostEqual(self.calculator.get_subtotal(), 0.9)

    def test_get_subtotal_float_prices_quantities(self):
        self.calculator.add_item("ProductA", 10.55, 3)  # 31.65
        self.calculator.add_item("ProductB", 2.11, 2)  # 4.22
        self.assertFloatAlmostEqual(self.calculator.get_subtotal(), 35.87)

    def test_get_subtotal_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal on empty order."):
            self.calculator.get_subtotal()

    # 5. apply_discount
    def test_apply_discount_valid(self):
        self.assertFloatAlmostEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_subtotal_as_integer(self):
        self.assertFloatAlmostEqual(self.calculator.apply_discount(100, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        self.assertFloatAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        self.assertFloatAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_zero_subtotal(self):
        self.assertFloatAlmostEqual(self.calculator.apply_discount(0.0, 0.2), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaisesRegex(ValueError, "Cannot apply discount on negative subtotal."):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_negative(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_too_high(self):
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_type_subtotal(self):
        with self.assertRaisesRegex(TypeError, "Subtotal must be a number."):
            self.calculator.apply_discount("100.0", 0.1)

    def test_apply_discount_invalid_type_discount(self):
        with self.assertRaisesRegex(TypeError, "Discount must be a number."):
            self.calculator.apply_discount(100.0, "0.1")

    # 6. calculate_shipping
    def test_calculate_shipping_below_threshold(self):
        # Default threshold 100, shipping 10
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal_below_threshold(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_zero_subtotal_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertFloatAlmostEqual(calc.calculate_shipping(0.0), 0.0)

    def test_calculate_shipping_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertFloatAlmostEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertFloatAlmostEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_subtotal_as_integer(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(50), 10.0)

    def test_calculate_shipping_invalid_type_subtotal(self):
        with self.assertRaisesRegex(TypeError, "Discounted subtotal must be a number."):
            self.calculator.calculate_shipping("50.0")

    def test_calculate_shipping_negative_subtotal_behavior(self):
        # Current behavior: negative subtotal is less than threshold, incurs shipping cost
        self.assertFloatAlmostEqual(self.calculator.calculate_shipping(-10.0), self.calculator.shipping_cost)

    # 7. calculate_tax
    def test_calculate_tax_positive_amount(self):
        # Default tax_rate 0.23
        self.assertFloatAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_amount_as_integer(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_tax(100), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertFloatAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertFloatAlmostEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertFloatAlmostEqual(calc.calculate_tax(100.0), 100.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate tax on negative amount."):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type_amount(self):
        with self.assertRaisesRegex(TypeError, "Amount must be a number."):
            self.calculator.calculate_tax("100.0")

    # 8. calculate_total
    def test_calculate_total_no_discount_below_shipping_threshold(self):
        self.calculator.add_item("ItemA", 50, 1)  # Subtotal 50
        # Shipping 10 (50 < 100)
        # Amount for tax = 50 + 10 = 60
        # Tax = 60 * 0.23 = 13.8
        # Total = 50 + 10 + 13.8 = 73.8
        self.assertFloatAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount_below_shipping_threshold(self):
        self.calculator.add_item("ItemA", 100, 1)  # Subtotal 100
        # Discount 20% -> Discounted Subtotal = 80
        # Shipping 10 (80 < 100)
        # Amount for tax = 80 + 10 = 90
        # Tax = 90 * 0.23 = 20.7
        # Total = 80 + 10 + 20.7 = 110.7
        self.assertFloatAlmostEqual(self.calculator.calculate_total(discount=0.2), 110.7)

    def test_calculate_total_no_discount_above_shipping_threshold(self):
        self.calculator.add_item("ItemA", 120, 1)  # Subtotal 120
        # Shipping 0 (120 >= 100)
        # Amount for tax = 120 + 0 = 120
        # Tax = 120 * 0.23 = 27.6
        # Total = 120 + 0 + 27.6 = 147.6
        self.assertFloatAlmostEqual(self.calculator.calculate_total(), 147.6)

    def test_calculate_total_with_discount_above_shipping_threshold(self):
        self.calculator.add_item("ItemA", 150, 1)  # Subtotal 150
        # Discount 0.2 -> Discounted Subtotal = 120
        # Shipping 0 (120 >= 100)
        # Amount for tax = 120 + 0 = 120
        # Tax = 120 * 0.23 = 27.6
        # Total = 120 + 0 + 27.6 = 147.6
        self.assertFloatAlmostEqual(self.calculator.calculate_total(discount=0.2), 147.6)

    def test_calculate_total_exact_shipping_threshold_after_discount(self):
        self.calculator.add_item("ItemA", 125, 1)  # Subtotal 125
        # Discount 0.2 -> Discounted Subtotal = 100
        # Shipping 0 (100 >= 100)
        # Amount for tax = 100 + 0 = 100
        # Tax = 100 * 0.23 = 23
        # Total = 100 + 0 + 23 = 123
        self.assertFloatAlmostEqual(self.calculator.calculate_total(discount=0.2), 123.0)

    def test_calculate_total_100_percent_discount(self):
        self.calculator.add_item("ItemA", 50, 1)  # Subtotal 50
        # Discount 1.0 -> Discounted Subtotal = 0
        # Shipping 10 (0 < 100)
        # Amount for tax = 0 + 10 = 10
        # Tax = 10 * 0.23 = 2.3
        # Total = 0 + 10 + 2.3 = 12.3
        self.assertFloatAlmostEqual(self.calculator.calculate_total(discount=1.0), 12.3)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item("ItemA", 50, 1)  # Subtotal 50
        # Shipping 10
        # Tax 0
        # Total = 50 + 10 + 0 = 60
        self.assertFloatAlmostEqual(calc.calculate_total(), 60.0)

    def test_calculate_total_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item("ItemA", 50, 1)  # Subtotal 50
        # Shipping 0 (because shipping_cost is 0)
        # Tax = 50 * 0.23 = 11.5
        # Total = 50 + 0 + 11.5 = 61.5
        self.assertFloatAlmostEqual(calc.calculate_total(), 61.5)

    def test_calculate_total_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        calc.add_item("ItemA", 50, 1)  # Subtotal 50
        # Shipping 0 (50 >= 0)
        # Tax = 50 * 0.23 = 11.5
        # Total = 50 + 0 + 11.5 = 61.5
        self.assertFloatAlmostEqual(calc.calculate_total(), 61.5)

    def test_calculate_total_empty_order(self):
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal on empty order."):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_negative(self):
        self.calculator.add_item("ItemA", 50, 1)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_too_high(self):
        self.calculator.add_item("ItemA", 50, 1)
        with self.assertRaisesRegex(ValueError, "Discount must be between 0.0 and 1.0."):
            self.calculator.calculate_total(discount=1.1)

    def test_calculate_total_invalid_type_discount(self):
        self.calculator.add_item("ItemA", 50, 1)
        with self.assertRaisesRegex(TypeError, "Discount must be a number."):
            self.calculator.calculate_total(discount="0.1")

    # 9. total_items
    def test_total_items_single_item_type_quantity_many(self):
        self.calculator.add_item("Apple", 0.5, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_item_types(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.calculator.add_item("Banana", 0.3, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_after_add_and_remove(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.calculator.add_item("Banana", 0.3, 3)  # Total 5
        self.calculator.remove_item("Apple")  # Total 3
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item_type_quantity_one(self):
        self.calculator.add_item("Apple", 0.5, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    # 10. clear_order
    def test_clear_order_with_items(self):
        self.calculator.add_item("Apple", 0.5, 2)
        self.calculator.add_item("Banana", 0.3, 3)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_get_subtotal_raises_error(self):
        self.calculator.add_item("Apple", 0.5, 1)
        self.calculator.clear_order()
        with self.assertRaisesRegex(ValueError, "Cannot calculate subtotal on empty order."):
            self.calculator.get_subtotal()

    # 11. list_items
    def test_list_items_multiple_unique_items(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.add_item("Banana", 0.3)
        self.assertCountEqual(self.calculator.list_items(), ["Apple",
                                                             "Banana"])  # Use assertCountEqual for list comparison where order doesn't matter

    def test_list_items_duplicate_adds(self):
        self.calculator.add_item("Apple", 0.5, 1)
        self.calculator.add_item("Apple", 0.5, 2)  # Same item, quantity updated
        self.assertCountEqual(self.calculator.list_items(), ["Apple"])

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_one_item(self):
        self.calculator.add_item("Apple", 0.5)
        self.assertCountEqual(self.calculator.list_items(), ["Apple"])

    def test_list_items_after_removal(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.add_item("Banana", 0.3)
        self.calculator.remove_item("Apple")
        self.assertCountEqual(self.calculator.list_items(), ["Banana"])

    # 12. is_empty
    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add_one_item(self):
        self.calculator.add_item("Apple", 0.5)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_add_multiple_items(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.add_item("Banana", 0.3)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_add_and_remove_last_item(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calculator.add_item("Apple", 0.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()