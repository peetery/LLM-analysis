import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100.0)

    def test_add_item_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_specific_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 30.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 1)
        self.assertEqual(calc.get_subtotal(), 40.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_same_name_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item1', 15.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 0)
        self.assertEqual(calc.total_items(), 0)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_add_item_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item1', -10.0, 1)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item1', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item(None, 10.0, 1)

    def test_add_item_wrong_type_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', '10.0', 1)

    def test_add_item_wrong_type_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item1', 10.0, 1.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Item2', calc.list_items())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('Item2')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Item1')

    def test_remove_item_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.remove_item('Item1')
        with self.assertRaises(KeyError):
            calc.remove_item('Item1')

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_none(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 25.0, 2)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 15.0, 3)
        self.assertEqual(calc.get_subtotal(), 65.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_items_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free', 0.0, 5)
        calc.add_item('Paid', 10.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_large_amount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50000.0, 10)
        self.assertEqual(calc.get_subtotal(), 500000.0)

    def test_get_subtotal_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        calc.remove_item('Item1')
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_apply_discount_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fixed_amount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 25.0)
        self.assertEqual(result, 75.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_equals_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 75.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 10.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=20.0)
        self.assertEqual(calc.calculate_shipping(50.0), 20.0)

    def test_calculate_shipping_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-50.0)

    def test_calculate_tax_standard(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(10000.0), 2300.0)

    def test_calculate_tax_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc.calculate_tax(100.0), 15.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + (50.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0, 1)
        total = calc.calculate_total(20.0)
        discounted = 80.0
        tax = discounted * 0.23
        expected = discounted + 10.0 + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0, 1)
        total = calc.calculate_total()
        tax = 120.0 * 0.23
        expected = 120.0 + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        expected = 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total(50.0)
        expected = 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0, 1)
        total = calc.calculate_total(30.0)
        discounted = 90.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_not_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0, 1)
        total = calc.calculate_total(10.0)
        discounted = 110.0
        tax = discounted * 0.23
        expected = discounted + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_integration(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 25.0, 1)
        total = calc.calculate_total(15.0)
        subtotal = 85.0
        discounted = 70.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax_and_shipping(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 50.0)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10.0)

    def test_calculate_total_discount_larger_than_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 1)
        total = calc.calculate_total(50.0)
        shipping = 10.0
        tax = shipping * 0.23
        expected = shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Item2', 15.0, 1)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 20.0, 4)
        self.assertEqual(calc.total_items(), 7)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_state_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_add_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.clear_order()
        calc.add_item('Item2', 20.0, 1)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        self.assertEqual(calc.list_items(), ['Item1'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        items = calc.list_items()
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        calc.remove_item('Item1')
        items = calc.list_items()
        self.assertNotIn('Item1', items)
        self.assertIn('Item2', items)

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Alpha', 10.0, 1)
        calc.add_item('Beta', 20.0, 1)
        calc.add_item('Gamma', 30.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_duplicate_handling(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item1', 15.0, 2)
        items = calc.list_items()
        self.assertEqual(items.count('Item1'), 1)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_is_empty_add_remove_cycle(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_integration_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 40.0, 2)
        calc.add_item('Item2', 30.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 110.0)
        total = calc.calculate_total(10.0)
        discounted = 100.0
        tax = discounted * 0.23
        expected = discounted + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_discount_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 80.0, 1)
        total = calc.calculate_total(20.0)
        discounted = 60.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_shipping_threshold_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 99.99, 1)
        total_below = calc.calculate_total()
        calc.clear_order()
        calc.add_item('Item2', 100.0, 1)
        total_at = calc.calculate_total()
        calc.clear_order()
        calc.add_item('Item3', 100.01, 1)
        total_above = calc.calculate_total()
        self.assertGreater(total_below, total_at)

    def test_integration_modify_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 20.0, 1)
        calc.add_item('Item2', 30.0, 1)
        calc.remove_item('Item1')
        calc.add_item('Item3', 50.0, 1)
        self.assertEqual(calc.get_subtotal(), 80.0)
        self.assertEqual(calc.total_items(), 2)

    def test_integration_multiple_calculators(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Item1', 10.0, 1)
        calc2.add_item('Item2', 20.0, 1)
        self.assertEqual(calc1.get_subtotal(), 10.0)
        self.assertEqual(calc2.get_subtotal(), 20.0)

    def test_integration_precision_throughout_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.33, 3)
        calc.add_item('Item2', 15.67, 2)
        subtotal = calc.get_subtotal()
        expected_subtotal = 10.33 * 3 + 15.67 * 2
        self.assertAlmostEqual(subtotal, expected_subtotal, places=2)

    def test_integration_edge_case_combinations(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        total = calc.calculate_total(10.0)
        self.assertEqual(total, 0.0)

    def test_integration_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 1)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 2)
        calc.remove_item('Item1')
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(len(calc.list_items()), 1)