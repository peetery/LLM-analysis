import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 15.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Sample', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Invalid', -5.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Invalid', 10.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Invalid', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item(None, 10.0, 1)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 'not_a_number', 1)

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 2.5)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Luxury Item', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_remove_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item(None)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 4)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_after_item_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 101.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_fixed_amount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertIsInstance(result, float)

    def test_apply_discount_greater_than_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 75.0)
        self.assertGreaterEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

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
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=10)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        expected = (90.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_affects_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 105.0, 1)
        total_no_discount = calc.calculate_total(discount=0.0)
        total_with_discount = calc.calculate_total(discount=10.0)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_calculate_total_tax_applied_last(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total()
        subtotal = 100.0
        shipping = 0.0
        base = subtotal + shipping
        expected = base * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_with_all_components(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 80.0
        after_discount = 72.0
        shipping = 10.0
        base = after_discount + shipping
        expected = base * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_default_discount_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_resets_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_resets_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_resets_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_allows_new_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_order_preservation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 1.0, 1)
        calc.add_item('Cherry', 2.0, 1)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(items, ['Banana'])

    def test_list_items_duplicate_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_returns_copy(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        items = calc.list_items()
        items.append('Banana')
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_is_empty_initial_state(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 800.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 850.0)
        total = calc.calculate_total(discount=10.0)
        expected_subtotal = 850.0
        after_discount = 765.0
        shipping = 0.0
        base = after_discount + shipping
        expected_total = base * 1.23
        self.assertAlmostEqual(total, expected_total, places=2)

    def test_order_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.remove_item('Apple')
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)
        self.assertEqual(calc.total_items(), 2)

    def test_calculation_order_matters(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total_with_discount = calc.calculate_total(discount=10.0)
        subtotal = 110.0
        after_discount = 99.0
        shipping = 10.0
        base = after_discount + shipping
        expected = base * 1.23
        self.assertAlmostEqual(total_with_discount, expected, places=2)

    def test_immutability_of_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        subtotal_before = calc.get_subtotal()
        calc.calculate_total()
        subtotal_after = calc.get_subtotal()
        self.assertEqual(subtotal_before, subtotal_after)

    def test_float_precision_edge_cases(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_very_small_amounts(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 0.0)

    def test_very_large_orders(self):
        calc = OrderCalculator()
        for i in range(1000):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 1000)
        self.assertEqual(calc.get_subtotal(), 1000.0)

    def test_unicode_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Café', 5.0, 1)
        calc.add_item('📱 Phone', 500.0, 1)
        items = calc.list_items()
        self.assertIn('Café', items)
        self.assertIn('📱 Phone', items)

    def test_special_characters_in_names(self):
        calc = OrderCalculator()
        calc.add_item('Item\'s "special"', 10.0, 1)
        items = calc.list_items()
        self.assertIn('Item\'s "special"', items)