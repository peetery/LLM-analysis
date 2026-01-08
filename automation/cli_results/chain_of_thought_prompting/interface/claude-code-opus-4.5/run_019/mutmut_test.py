import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_add_item_single_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 5.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 2)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_item_decimal_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99, places=2)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 1.0, 1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_minimum_valid_price(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01, places=2)

    def test_add_item_explicit_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Single', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Duplicate', 10.0, 1)
        calc.add_item('Duplicate', 10.0, 1)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_none_name_raises_error(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item(None, 10.0, 1)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0, 1)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Free', 0.0, 1)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_add_item_non_integer_quantity_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 1.5)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.remove_item('Book')
        self.assertEqual(calc.list_items(), ['Pen'])

    def test_remove_item_only_item_makes_order_empty(self):
        calc = OrderCalculator()
        calc.add_item('Solo', 50.0, 1)
        calc.remove_item('Solo')
        self.assertTrue(calc.is_empty())

    def test_remove_item_updates_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.remove_item('Book')
        self.assertAlmostEqual(calc.get_subtotal(), 5.0, places=2)

    def test_remove_item_nonexistent_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        with self.assertRaises((ValueError, KeyError)):
            calc.remove_item('Nonexistent')

    def test_remove_item_from_empty_order_raises_error(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, KeyError)):
            calc.remove_item('Any')

    def test_remove_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_none_name_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        with self.assertRaises((TypeError, ValueError)):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 50.0, places=2)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 2)
        calc.add_item('Pen', 5.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 65.0, places=2)

    def test_get_subtotal_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        calc.add_item('B', 20.0, 2)
        calc.add_item('C', 5.0, 5)
        self.assertAlmostEqual(calc.get_subtotal(), 75.0, places=2)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 19.99, 1)
        calc.add_item('Item2', 9.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 39.97, places=2)

    def test_get_subtotal_after_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.remove_item('Pen')
        self.assertAlmostEqual(calc.get_subtotal(), 25.0, places=2)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_apply_discount_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_hundred_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 101.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 10.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(50.0)
        self.assertAlmostEqual(result, 11.5, places=2)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_total_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10.0)

    def test_calculate_total_discount_over_hundred_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(101.0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 2)
        calc.add_item('Pen', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 3)
        calc.add_item('Pen', 5.0, 2)
        calc.remove_item('Book')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_total_items_is_zero(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        self.assertEqual(calc.list_items(), ['Book'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.add_item('Pen', 5.0, 1)
        items = calc.list_items()
        self.assertIn('Book', items)
        self.assertIn('Pen', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_returns_strings(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        items = calc.list_items()
        self.assertIsInstance(items[0], str)

    def test_is_empty_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_add_remove_calculate(self):
        calc = OrderCalculator()
        calc.add_item('Book', 30.0, 2)
        calc.add_item('Pen', 5.0, 4)
        calc.remove_item('Book')
        total = calc.calculate_total()
        expected = (20.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_multiple_subtotal_calls(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        first_subtotal = calc.get_subtotal()
        calc.add_item('B', 20.0, 1)
        second_subtotal = calc.get_subtotal()
        self.assertAlmostEqual(first_subtotal, 10.0, places=2)
        self.assertAlmostEqual(second_subtotal, 30.0, places=2)

    def test_integration_clear_then_add_new_items(self):
        calc = OrderCalculator()
        calc.add_item('Old', 100.0, 1)
        calc.clear_order()
        calc.add_item('New', 50.0, 1)
        self.assertEqual(calc.list_items(), ['New'])
        self.assertAlmostEqual(calc.get_subtotal(), 50.0, places=2)

    def test_integration_tax_applied_correctly(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)