import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_same_item_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_empty_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -5)

    def test_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 3)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '10.99')

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 5.5)

    def test_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.0)

    def test_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99)

    def test_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_item_name_with_special_characters(self):
        calc = OrderCalculator()
        calc.add_item('Test-Item_123!@#', 1.5, 1)
        self.assertIn('Test-Item_123!@#', calc.list_items())

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.list_items()), 1)
        self.assertIn('Banana', calc.list_items())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_already_removed_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_case_sensitivity_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 3.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 5.4)

    def test_subtotal_after_adding_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 7.5)

    def test_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_subtotal_with_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000)
        self.assertAlmostEqual(calc.get_subtotal(), 1500.0)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.33, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.99, places=2)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_twenty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_negative_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_non_numeric_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.001)
        self.assertAlmostEqual(result, 99.9)

    def test_discount_boundary_one(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_shipping_none_as_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_very_large_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(999999.99)
        self.assertAlmostEqual(shipping, 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_tax_with_different_tax_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 15.0)

    def test_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_tax_none_as_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_tax_very_small_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023)

    def test_tax_very_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(999999.99)
        self.assertAlmostEqual(tax, 229999.9977)

    def test_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_total_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total(0.0)
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.2)
        expected = (40.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_above_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(0.1)
        expected = 135.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_zero_discount_explicitly(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_at_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_total_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_complex_calculation_flow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(0.2)
        subtotal = 100.0
        discounted = 80.0
        with_shipping = 90.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected)

    def test_discount_brings_subtotal_to_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=80.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        expected = 80.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_discount_brings_subtotal_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0, 1)
        total = calc.calculate_total(0.2)
        expected = (96.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_total_items_after_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_re_add_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 0.8, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertIn('Banana', calc.list_items())

    def test_clear_multiple_times(self):
        calc = OrderCalculator()
        calc.clear_order()
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Banana', items)

    def test_list_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_on_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 35.0)
        total = calc.calculate_total(0.1)
        discounted = 31.5
        with_shipping = 41.5
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.remove_item('Banana')
        calc.add_item('Orange', 8.0, 1)
        total = calc.calculate_total(0.0)
        subtotal = 28.0
        with_shipping = 38.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected)

    def test_exact_threshold_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        with_shipping = 106.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected)

    def test_exact_threshold_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_add_remove_re_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_multiple_discounts_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.2)
        self.assertNotEqual(total1, total2)

    def test_tax_calculation_on_subtotal_plus_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        base = 60.0
        expected = base * 1.23
        self.assertAlmostEqual(total, expected)

    def test_zero_tax_and_zero_shipping_scenario(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 50.0)

    def test_large_order_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0, 10)
        calc.add_item('Item2', 200.0, 5)
        calc.add_item('Item3', 50.0, 20)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 3000.0)

    def test_items_persist_after_failed_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        try:
            calc.add_item('', 1.0)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 2)

    def test_order_state_after_exception(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        try:
            calc.remove_item('Banana')
        except ValueError:
            pass
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 2)

    def test_concurrent_modifications(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total1 = calc.calculate_total(0.0)
        calc.add_item('Banana', 5.0, 1)
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)

    def test_remove_item_doesnt_affect_other_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.remove_item('Apple')
        self.assertAlmostEqual(calc.get_subtotal(), 15.0)

    def test_minimum_viable_order(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.01)

    def test_maximum_practical_values(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1000)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 999999990.0)

    def test_threshold_boundary_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 99.999, 1)
        shipping = calc.calculate_shipping(99.999)
        self.assertAlmostEqual(shipping, 10.0)
        calc2 = OrderCalculator()
        calc2.add_item('Item', 100.001, 1)
        shipping2 = calc2.calculate_shipping(100.001)
        self.assertAlmostEqual(shipping2, 0.0)

    def test_all_zero_configuration(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0, free_shipping_threshold=0.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 50.0)