import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_quantity_one_explicit(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Luxury', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_float_price_many_decimals(self):
        calc = OrderCalculator()
        calc.add_item('Precise', 1.123456789, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 1.123456789)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item(None, 1.5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('Apple', 'expensive')

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_subtotal_updates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_remove_item_single_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitive(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_none_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises((ValueError, TypeError)):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 1.25, 1)
        self.assertEqual(calc.get_subtotal(), 3.75)

    def test_get_subtotal_items_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_calculation_verification(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 4)
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_calculation_verification(self):
        calc = OrderCalculator()
        result = calc.apply_discount(200.0, 15.0)
        self.assertEqual(result, 170.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 110.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 10.0)

    def test_apply_discount_small_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(33.33, 33.33)
        self.assertAlmostEqual(result, 22.22, places=2)

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
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-50.0)

    def test_calculate_shipping_free_returns_zero(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(200.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_typical_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_calculation_verification(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(50.0)
        self.assertEqual(result, 5.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_very_small_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(10.0)
        expected = 90.0 + 10.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(100.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_brings_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total = calc.calculate_total(20.0)
        discounted = 88.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_keeps_above_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total(10.0)
        discounted = 135.0
        shipping = 0.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10.0)

    def test_calculate_total_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(110.0)

    def test_calculate_total_formula_verification(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 40.0, 1)
        total = calc.calculate_total(10.0)
        discounted = 36.0
        shipping = 5.0
        tax = (discounted + shipping) * 0.1
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 0.75, 1)
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.75, 5)
        self.assertEqual(calc.total_items(), 8)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_counts_quantity_not_unique(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_subtotal_becomes_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_total_items_becomes_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_names_correct(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_full_workflow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Widget', 25.0, 3)
        calc.add_item('Gadget', 15.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 105.0)
        discounted = calc.apply_discount(subtotal, 10.0)
        self.assertEqual(discounted, 94.5)
        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 10.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(tax, 10.45, places=2)
        total = calc.calculate_total(10.0)
        self.assertAlmostEqual(total, 114.95, places=2)

    def test_integration_add_remove_verify_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.add_item('Banana', 5.0, 4)
        self.assertEqual(calc.get_subtotal(), 70.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 20.0)
        self.assertEqual(calc.total_items(), 4)

    def test_integration_clear_add_new_items(self):
        calc = OrderCalculator()
        calc.add_item('OldItem', 100.0, 1)
        calc.clear_order()
        calc.add_item('NewItem', 50.0, 2)
        self.assertEqual(calc.get_subtotal(), 100.0)
        self.assertEqual(calc.total_items(), 2)
        self.assertIn('NewItem', calc.list_items())
        self.assertNotIn('OldItem', calc.list_items())

    def test_integration_boundary_cross_free_shipping_add(self):
        calc = OrderCalculator()
        calc.add_item('Small', 30.0, 1)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)
        calc.add_item('Large', 80.0, 1)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)

    def test_integration_boundary_cross_free_shipping_remove(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 60.0, 1)
        calc.add_item('Item2', 50.0, 1)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)
        calc.remove_item('Item2')
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)