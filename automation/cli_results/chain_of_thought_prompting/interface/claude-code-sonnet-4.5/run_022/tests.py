import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(250), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_very_high_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=1000000.0)
        self.assertEqual(calc.calculate_shipping(50000), 10.0)

    def test_init_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        result = calc.calculate_tax(100)
        self.assertEqual(result, -10.0)

    def test_init_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5.0)
        result = calc.calculate_shipping(50)
        self.assertEqual(result, -5.0)

    def test_init_negative_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-100.0)
        result = calc.calculate_shipping(50)
        self.assertEqual(result, 0.0)

    def test_add_item_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_single_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_add_item_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        subtotal = calc.get_subtotal()
        self.assertIn(subtotal, [7.5, 4.5])

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 0)
        subtotal = calc.get_subtotal()
        self.assertIn(subtotal, [0.0, 1.5])

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_fractional_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99, places=2)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10.0, 1)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0, 1)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 'ten', 1)

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 2.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(calc.get_subtotal(), 4.5)
        self.assertNotIn('Banana', calc.list_items())

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_item_already_removed_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_different_case(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('apple')

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('')

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_get_subtotal_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_get_subtotal_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 10000)
        self.assertEqual(calc.get_subtotal(), 50000.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_get_subtotal_many_small_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 1.0, places=2)

    def test_apply_discount_percentage_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_discount_large_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(10000.0, 0.01)
        self.assertAlmostEqual(result, 9999.0, places=2)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, -10.0)
        self.assertEqual(result, 110.0)

    def test_apply_discount_greater_than_100_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 150.0)
        self.assertEqual(result, -50.0)

    def test_apply_discount_decimal_format(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 25.0)
        self.assertEqual(result, 75.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertIn(result, [0.0, 10.0])

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(-10.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=25.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 25.0)

    def test_calculate_tax_standard_tax_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_on_small_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_tax_on_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

    def test_calculate_tax_different_tax_rates(self):
        calc1 = OrderCalculator(tax_rate=0.05)
        calc2 = OrderCalculator(tax_rate=0.15)
        calc3 = OrderCalculator(tax_rate=0.3)
        self.assertEqual(calc1.calculate_tax(100), 5.0)
        self.assertEqual(calc2.calculate_tax(100), 15.0)
        self.assertEqual(calc3.calculate_tax(100), 30.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(-100.0)
        self.assertEqual(result, -23.0)

    def test_calculate_total_empty_order_no_discount(self):
        calc = OrderCalculator()
        result = calc.calculate_total()
        self.assertEqual(result, 0.0)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 15.0, 1)
        total = calc.calculate_total()
        subtotal = 35.0
        shipping = 10.0
        expected = (subtotal + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        discounted = 90.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_above_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_threshold_before_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=20.0)
        subtotal = 100.0
        discounted = 80.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0, 1)
        total = calc.calculate_total(discount=20.0)
        subtotal = 120.0
        discounted = 96.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_100_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(discount=100.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complete_order_flow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        discounted = 90.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_tax_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 60.0)

    def test_calculate_total_multiple_calls_same_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total(discount=10.0)
        total2 = calc.calculate_total(discount=10.0)
        self.assertEqual(total1, total2)

    def test_calculate_total_different_discount_each_call(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total1 = calc.calculate_total(discount=10.0)
        total2 = calc.calculate_total(discount=20.0)
        self.assertNotEqual(total1, total2)
        self.assertGreater(total1, total2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_1(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_5(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        total = calc.total_items()
        self.assertIn(total, [1, 5])

    def test_total_items_multiple_items_quantity_1_each(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 2.0, 5)
        total = calc.total_items()
        self.assertIn(total, [2, 8])

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_check_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_then_check_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_then_check_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_clear_order_then_add_new_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_order_preservation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(items[0], 'Apple')

    def test_list_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertNotIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_duplicate_handling(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Apple', 2.0, 1)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_returns_names_only(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        items = calc.list_items()
        self.assertEqual(items[0], 'Apple')
        self.assertIsInstance(items[0], str)

    def test_is_empty_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item_with_quantity_0(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 0)
        is_empty = calc.is_empty()
        self.assertIsInstance(is_empty, bool)

    def test_integration_complete_checkout_flow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 100.0)
        discounted = calc.apply_discount(subtotal, 10.0)
        self.assertEqual(discounted, 90.0)
        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 10.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertEqual(tax, 23.0)
        total = calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_integration_multiple_operations_on_same_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 20.0, 1)
        calc.remove_item('Apple')
        calc.add_item('Orange', 15.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_boundary_testing_around_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 90.0, 1)
        shipping1 = calc.calculate_shipping(90.0)
        self.assertEqual(shipping1, 10.0)
        calc.add_item('Item2', 15.0, 1)
        shipping2 = calc.calculate_shipping(105.0)
        self.assertEqual(shipping2, 0.0)

    def test_integration_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        subtotal = calc.get_subtotal()
        shipping_before = calc.calculate_shipping(subtotal)
        self.assertEqual(shipping_before, 0.0)
        discounted = calc.apply_discount(subtotal, 20.0)
        shipping_after = calc.calculate_shipping(discounted)
        self.assertEqual(shipping_after, 10.0)

    def test_integration_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 20.0, 1)
        items = calc.list_items()
        total_items = calc.total_items()
        is_empty = calc.is_empty()
        self.assertEqual(len(items), 2)
        self.assertEqual(total_items, 2)
        self.assertFalse(is_empty)

    def test_floating_point_arithmetic_cumulative(self):
        calc = OrderCalculator()
        for i in range(10):
            calc.add_item(f'Item{i}', 0.1, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1.0, places=10)

    def test_unicode_item_names(self):
        calc = OrderCalculator()
        calc.add_item('🍎 Apple', 10.0, 1)
        calc.add_item('Café', 5.0, 1)
        items = calc.list_items()
        self.assertIn('🍎 Apple', items)
        self.assertIn('Café', items)

    def test_very_long_item_names(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 10.0, 1)
        items = calc.list_items()
        self.assertIn(long_name, items)

    def test_special_characters_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Item "quoted"', 10.0, 1)
        calc.add_item('Item\\backslash', 5.0, 1)
        calc.add_item('Item\nwith\nnewlines', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_stress_large_order(self):
        calc = OrderCalculator()
        for i in range(1000):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 1000)
        self.assertAlmostEqual(calc.get_subtotal(), 1000.0, places=2)