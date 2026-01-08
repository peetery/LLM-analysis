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

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item', 100.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        calc.add_item('Item', 10.0)
        shipping = calc.calculate_shipping(10.0)
        self.assertEqual(shipping, 0.0)

    def test_negative_parameters(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.add_item('Item3', 30.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

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
            calc.add_item('Item', 10.0, 1.5)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 999999.99)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_with_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        calc.remove_item('Item2')
        self.assertTrue(calc.is_empty())

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 1)
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_subtotal_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_subtotal_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 15.0, 4)
        self.assertEqual(calc.get_subtotal(), 60.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_typical_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_100_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_fractional_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.15)
        self.assertEqual(result, 85.0)

    def test_apply_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0001)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_shipping_empty_order(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(-10.0)
        self.assertEqual(shipping, 10.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(10.55)
        self.assertAlmostEqual(tax, 2.4265, places=4)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 150.0)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_exactly_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_multiple_items_and_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0)
        total = calc.calculate_total(discount=0.2)
        subtotal = 130.0
        discounted = subtotal * 0.8
        expected = discounted + 0.0 + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 20.0, 2)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_readd_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        calc.add_item('Item2', 20.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_clear_multiple_times(self):
        calc = OrderCalculator()
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Item1', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.add_item('Item3', 30.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)
        self.assertIn('Item3', items)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        items = calc.list_items()
        self.assertNotIn('Item1', items)
        self.assertIn('Item2', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 130.0)
        total = calc.calculate_total(discount=0.1)
        after_discount = 117.0
        tax = after_discount * 0.23
        expected = after_discount + 0.0 + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        calc.add_item('Item2', 20.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_boundary_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_tax_calculation_base(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(discount=0.1)
        discounted = 90.0
        tax = calc.calculate_tax(discounted)
        self.assertAlmostEqual(tax, 20.7, places=2)

    def test_precision_and_rounding(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.33, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 30.99, places=2)

    def test_state_consistency_after_errors(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        try:
            calc.add_item('', 20.0)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_concurrent_like_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        calc.add_item('Item3', 30.0)
        calc.remove_item('Item2')
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_type_checking_add_item(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_none_values_in_methods(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, None)

    def test_string_numbers(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_float_for_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 1.5)

    def test_item_structure_validation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Item1', items)