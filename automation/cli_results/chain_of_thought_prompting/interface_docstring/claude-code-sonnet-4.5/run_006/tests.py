import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_single_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_duplicate_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, 2)
        calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Luxury Item', 999999.99)
        self.assertEqual(calc.items[0]['price'], 999999.99)

    def test_add_item_decimal_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99)
        self.assertEqual(calc.items[0]['price'], 19.99)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calc.add_item('Item', 15.0)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 2.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_from_multi_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_then_verify_gone(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Item')

    def test_remove_item_case_sensitive_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 5.0, 4)
        calc.add_item('Item3', 2.0, 10)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 39.98, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_half_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.05)
        self.assertEqual(result, 95.0)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_very_large_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(999999.99)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_hundred_percent_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(10000.0)
        self.assertEqual(tax, 2300.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        expected_with_tax = expected * 1.23
        self.assertAlmostEqual(total, expected_with_tax, places=2)

    def test_calculate_total_with_discount_no_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        total = calc.calculate_total(discount=0.2)
        subtotal = 80.0
        discounted = 64.0
        with_shipping = 64.0 + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_exactly_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_calculate_total_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complex_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 3)
        total = calc.calculate_total(discount=0.1)
        subtotal = 120.0
        discounted = 108.0
        with_shipping = 108.0
        expected = 108.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_negative(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 15.0, 3)
        calc.add_item('Item3', 20.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        calc.add_item('Item2', 15.0, 3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 15.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_then_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_verify_total_items_zero(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_no_duplicates_after_duplicate_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Apple')

    def test_list_items_preserves_names(self):
        calc = OrderCalculator()
        calc.add_item('Test Item', 10.0)
        items = calc.list_items()
        self.assertEqual(items[0], 'Test Item')

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 15.0)
        self.assertFalse(calc.is_empty())

    def test_workflow_add_multiple_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 40.0, 1)
        total = calc.calculate_total(discount=0.1)
        subtotal = 100.0
        discounted = 90.0
        with_shipping = 90.0 + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_workflow_add_remove_verify_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_workflow_add_duplicate_items_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 2)
        calc.add_item('Item', 5.0, 3)
        calc.add_item('Item', 5.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_workflow_calculate_total_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total1 = calc.calculate_total()
        total2 = calc.calculate_total()
        self.assertEqual(total1, total2)

    def test_workflow_clear_and_readd_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        calc.add_item('Item2', 20.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Item2')

    def test_edge_case_very_small_prices(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 100)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1.0, places=2)

    def test_edge_case_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_edge_case_large_order_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_edge_case_maximum_values(self):
        calc = OrderCalculator()
        calc.add_item('Max Item', 999999.99, 999)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 999999.99 * 999, places=2)

    def test_edge_case_discount_to_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 111.11)
        total = calc.calculate_total(discount=0.1)
        discounted = 99.999
        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 10.0)

    def test_edge_case_zero_cost_order_full_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_consistency_remove_then_readd_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        calc.remove_item('Item')
        calc.add_item('Item', 10.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_state_consistency_multiple_discount_applications(self):
        calc = OrderCalculator()
        result1 = calc.apply_discount(100.0, 0.2)
        result2 = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result1, result2)

    def test_state_consistency_interleaved_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        calc.add_item('Item2', 20.0)
        total = calc.calculate_total()
        expected = (20.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)