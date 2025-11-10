import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_constructor_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_constructor_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_constructor_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_constructor_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_constructor_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_constructor_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_constructor_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.add_item('Item3', 30.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_same_item_twice_accumulates(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item1', 10.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.0, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_add_item_decimal_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', 10.0, 2.5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item1', -10.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item1', 10.0, -1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item1', 10.0, 0)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item(None, 10.0)

    def test_add_item_none_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', None)

    def test_add_item_string_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', '10.0')

    def test_add_item_string_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', 10.0, '5')

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_item_verify_gone_from_list(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item2')
        self.assertEqual(calc.total_items(), 1)

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_item_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item(None)

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_list_items_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_contains_all_added(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        items = calc.list_items()
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)

    def test_list_items_no_removed_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())

    def test_total_items_normal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 20.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Item2', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_accounts_for_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.clear_order()
        self.assertEqual(len(calc.list_items()), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_subtotal_zero(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_is_empty_true(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 20.0, 2)
        self.assertEqual(calc.get_subtotal(), 70.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_formula(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 15.5, 4)
        calc.add_item('Item2', 7.25, 3)
        expected = 15.5 * 4 + 7.25 * 3
        self.assertAlmostEqual(calc.get_subtotal(), expected, places=2)

    def test_get_subtotal_decimal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.99, 1)
        calc.add_item('Item2', 5.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 22.97, places=2)

    def test_apply_discount_valid_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

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

    def test_apply_discount_over_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_discount_decimal_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 15.5)
        self.assertAlmostEqual(result, 84.49145, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 15.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_formula(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(50.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_tax_decimal_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + (50.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(10.0)
        discounted = 90.0
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 80.0)
        total = calc.calculate_total(20.0)
        subtotal = 80.0
        after_discount = 64.0
        shipping = 10.0
        taxable = after_discount + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_discount_before_tax(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(50.0)
        discounted = 50.0
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 150.0)
        total = calc.calculate_total(10.0)
        discounted = 135.0
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0)
        total = calc.calculate_total()
        subtotal = 120.0
        shipping = 0.0
        taxable = subtotal + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_without_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        total = calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        taxable = subtotal + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(0.0)
        subtotal = 100.0
        shipping = 0.0
        taxable = subtotal + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 150.0)
        total = calc.calculate_total(40.0)
        discounted = 90.0
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complete_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total(25.0)
        subtotal = 80.0
        discounted = 60.0
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_decimal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 19.99, 3)
        total = calc.calculate_total(15.0)
        subtotal = 59.97
        discounted = 50.9745
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_add_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        calc.add_item('Item2', 50.0)
        total = calc.calculate_total(10.0)
        subtotal = 150.0
        discounted = 135.0
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_add_remove_verify(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        calc.add_item('Item2', 20.0, 3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)
        self.assertAlmostEqual(calc.get_subtotal(), 60.0, places=2)

    def test_integration_lifecycle(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        total = calc.calculate_total(5.0)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_integration_state_persistence(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        first_total = calc.calculate_total()
        calc.add_item('Item2', 20.0)
        second_total = calc.calculate_total()
        self.assertGreater(second_total, first_total)

    def test_integration_complex_order(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=150.0, shipping_cost=12.0)
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 3)
        calc.add_item('Item3', 20.0, 1)
        total = calc.calculate_total(15.0)
        subtotal = 50.0 * 2 + 30.0 * 3 + 20.0 * 1
        discounted = subtotal * 0.85
        shipping = 12.0
        taxable = discounted + shipping
        tax = taxable * 0.2
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)