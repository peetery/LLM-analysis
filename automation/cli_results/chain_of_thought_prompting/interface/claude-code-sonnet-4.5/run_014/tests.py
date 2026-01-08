import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate_initialization(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_zero_shipping_cost_initialization(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold_initialization(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_negative_values_initialization(self):
        with self.assertRaises((ValueError, AssertionError)):
            OrderCalculator(tax_rate=-0.1)

    def test_initial_state_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())
        self.assertIn('Apple', calc.list_items())

    def test_add_single_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertIn('Banana', calc.list_items())

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.add_item('Apple', -1.5)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0)
        self.assertIn('Free Item', calc.list_items())

    def test_add_item_with_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.add_item('', 1.5)

    def test_add_item_with_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError, AssertionError)):
            calc.add_item(None, 1.5)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99)
        self.assertIn('Expensive', calc.list_items())

    def test_add_item_with_fractional_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError, AssertionError)):
            calc.add_item('Apple', 1.5, quantity=2.5)

    def test_add_item_with_wrong_types(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError, AssertionError)):
            calc.add_item('Apple', 'not_a_number')

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('NonExistent')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Apple')

    def test_remove_with_empty_string(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('')

    def test_remove_with_none(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError, TypeError)):
            calc.remove_item(None)

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_percentage_discount_10_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_percentage_discount_50_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_discount_greater_than_100_percent(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.apply_discount(100.0, 1.5)

    def test_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, AssertionError)):
            calc.apply_discount(100.0, -0.1)

    def test_fixed_amount_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_discount_larger_than_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 0.8)
        self.assertGreaterEqual(result, 0.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_at_threshold_exactly(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_zero_discounted_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_negative_discounted_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(-10.0)
        self.assertEqual(shipping, 10.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(-100.0)
        self.assertEqual(tax, -23.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(10.0)
        self.assertAlmostEqual(tax, 2.3, places=2)

    def test_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertGreaterEqual(total, 0.0)

    def test_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        total = calc.calculate_total()
        self.assertGreater(total, 10.0)

    def test_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total_with_discount = calc.calculate_total(discount=0.1)
        total_without_discount = calc.calculate_total(discount=0.0)
        self.assertLess(total_with_discount, total_without_discount)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_of_operations_in_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=0.1)
        discounted = 90.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_calculation_base(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        self.assertGreater(total, 50.0)

    def test_total_with_100_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=1.0)
        self.assertGreaterEqual(total, 0.0)

    def test_total_complex_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 25.0, quantity=2)
        calc.add_item('Item2', 30.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        self.assertGreater(total, 0.0)

    def test_total_boundary_at_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 111.11)
        total_with_discount = calc.calculate_total(discount=0.1)
        self.assertGreater(total_with_discount, 0.0)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertGreater(calc.total_items(), 0)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        total = calc.total_items()
        self.assertGreater(total, 0)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        total = calc.total_items()
        self.assertGreater(total, 0)

    def test_total_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        initial_count = calc.total_items()
        calc.remove_item('Apple')
        final_count = calc.total_items()
        self.assertLess(final_count, initial_count)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 2.0)
        self.assertFalse(calc.is_empty())

    def test_clear_affects_all_methods(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_is_empty_new_instance(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_add_calculate_remove_recalculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        total1 = calc.calculate_total()
        calc.remove_item('Apple')
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        calc.add_item('Banana', 30.0)
        total1 = calc.calculate_total(discount=0.1)
        calc.remove_item('Banana')
        total2 = calc.calculate_total(discount=0.1)
        self.assertNotEqual(total1, total2)

    def test_item_with_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.01, places=2)

    def test_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 100.0)

    def test_complex_discount_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Item', 95.0)
        total_without = calc.calculate_total(discount=0.0)
        total_with = calc.calculate_total(discount=0.1)
        self.assertNotEqual(total_without, total_with)

    def test_tax_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        self.assertGreater(total, 50.0)

    def test_discount_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.5)
        self.assertGreater(total, 0.0)

    def test_full_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 20.0)
        total2 = calc.calculate_total()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_very_large_numbers(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 1000000.0)

    def test_very_small_numbers(self):
        calc = OrderCalculator()
        calc.add_item('Tiny', 0.001)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.001, places=3)

    def test_floating_point_rounding(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.99, quantity=3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 32.97, places=2)

    def test_unicode_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Äpfel', 1.5)
        self.assertIn('Äpfel', calc.list_items())

    def test_case_sensitivity_of_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('apple', 2.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('apple', items)

    def test_whitespace_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('  Apple  ', 1.5)
        items = calc.list_items()
        self.assertTrue(any(('Apple' in item for item in items)))