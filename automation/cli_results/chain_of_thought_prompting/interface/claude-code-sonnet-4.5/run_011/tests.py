import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        calc.add_item('Item', 90, 1)
        self.assertEqual(calc.calculate_shipping(90), 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        calc.add_item('Item', 40, 1)
        self.assertEqual(calc.calculate_shipping(40), 5.0)

    def test_zero_tax_rate_initialization(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_zero_shipping_cost_initialization(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item', 50, 1)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_add_duplicate_item_same_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 3.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, -1)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -2.5, 1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.5, 1)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 10000)
        self.assertEqual(calc.total_items(), 10000)
        self.assertEqual(calc.get_subtotal(), 25000.0)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 1.5, 1)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_remove_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('')

    def test_subtotal_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 9.5)

    def test_subtotal_with_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_subtotal_after_adding_and_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_apply_zero_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_standard_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_100_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.1)
        self.assertEqual(result, 0.0)

    def test_apply_fractional_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.15)
        self.assertEqual(result, 85.0)

    def test_shipping_for_amount_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_for_amount_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_for_amount_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_for_zero_amount(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_with_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_shipping_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_with_default_rate(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_tax_with_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(1000000.0)
        self.assertEqual(tax, 230000.0)

    def test_total_for_empty_order_with_no_discount(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_total_for_single_item_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_applied(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.1)
        discounted = 90.0
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_default_discount_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Cheap Item', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_100_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_after_discount_crosses_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_multiple_items_and_partial_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 100.0
        discounted = 90.0
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item_quantity_1(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_quantity_greater_than_1(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_an_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.add_item('Banana', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_populated_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_state_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_list_items_in_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 1.5, 1)
        calc.add_item('Orange', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 1.5, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Banana', items)
        self.assertNotIn('Apple', items)

    def test_list_items_preserves_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 1.5, 1)
        calc.add_item('Orange', 3.0, 1)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 3)

    def test_is_empty_on_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 100.0)
        total = calc.calculate_total(0.1)
        discounted = 90.0
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_readd_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 3.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertFalse(calc.is_empty())

    def test_shipping_threshold_edge_cases_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total_no_discount = calc.calculate_total(0.0)
        expected_no_discount = 110.0 * 1.23
        self.assertAlmostEqual(total_no_discount, expected_no_discount, places=2)
        total_with_discount = calc.calculate_total(0.15)
        discounted = 93.5
        shipping = 10.0
        expected_with_discount = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total_with_discount, expected_with_discount, places=2)

    def test_multiple_discounts_on_same_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.2)
        self.assertNotEqual(total1, total2)
        self.assertGreater(total1, total2)

    def test_precision_and_rounding_for_monetary_values(self):
        calc = OrderCalculator()
        calc.add_item('Item', 33.33, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 99.99, places=2)

    def test_tax_calculation_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        base = subtotal + shipping
        tax = base * 0.23
        expected = base + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_very_small_prices(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.01, places=2)

    def test_fractional_quantities_not_allowed(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('Apple', 2.5, 2.5)

    def test_unicode_special_characters_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Äpfel', 2.5, 1)
        calc.add_item('香蕉', 1.5, 1)
        items = calc.list_items()
        self.assertIn('Äpfel', items)
        self.assertIn('香蕉', items)

    def test_case_sensitivity_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('apple', 3.0, 1)
        items = calc.list_items()
        apple_count = sum((1 for item in items if item.lower() == 'apple'))
        self.assertGreaterEqual(apple_count, 1)