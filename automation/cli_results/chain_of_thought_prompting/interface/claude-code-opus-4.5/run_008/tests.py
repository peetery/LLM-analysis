import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)
        calc.add_item('item', 100.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        calc.add_item('item', 10.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0)
        calc.add_item('item', 10.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_init_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.calculate_tax(100.0), -10.0)

    def test_init_negative_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-10.0)
        calc.add_item('item', 5.0)
        self.assertEqual(calc.calculate_shipping(5.0), 0.0)

    def test_init_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5.0)
        self.assertEqual(calc.shipping_cost, -5.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('apple', calc.list_items())

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.add_item('orange', 1.75)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 2)
        calc.add_item('apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 0)
        self.assertEqual(calc.total_items(), 0)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        calc.add_item('free_item', 0.0, 5)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_fractional_price(self):
        calc = OrderCalculator()
        calc.add_item('item', 19.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 59.97, places=2)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('item', -5.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('item', 5.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item(None, 5.0)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item(123, 5.0)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('item', 'five')

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('item', 5.0, 2.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_after_multiple_adds(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.add_item('orange', 1.75)
        calc.remove_item('banana')
        items = calc.list_items()
        self.assertNotIn('banana', items)
        self.assertEqual(len(items), 2)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('banana')

    def test_remove_item_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_then_readd(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        calc.add_item('apple', 2.0)
        self.assertIn('apple', calc.list_items())

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_none_name(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        with self.assertRaises((ValueError, TypeError)):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0)
        calc.add_item('banana', 5.0)
        calc.add_item('orange', 3.0)
        self.assertEqual(calc.get_subtotal(), 18.0)

    def test_get_subtotal_items_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0, 3)
        calc.add_item('banana', 5.0, 2)
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0)
        calc.add_item('banana', 5.0)
        calc.remove_item('apple')
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('item1', 0.1)
        calc.add_item('item2', 0.2)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_apply_discount_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_percentage_like(self):
        calc = OrderCalculator()
        result = calc.apply_discount(200.0, 40.0)
        self.assertEqual(result, 160.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_equals_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_exceeds_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(-50.0, 10.0)
        self.assertLessEqual(result, 0.0)

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

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(-10.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_various_amounts(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(50.0), 11.5, places=2)
        self.assertAlmostEqual(calc.calculate_tax(200.0), 46.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_small_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(-100.0)
        self.assertEqual(result, -23.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 100.0)
        total = calc.calculate_total(discount=20.0)
        expected = (80.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_achieved(self):
        calc = OrderCalculator()
        calc.add_item('item', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_shipping_charged(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_equals_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        total = calc.calculate_total(discount=50.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_exceeds_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        total = calc.calculate_total(discount=100.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('item', 100.0)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_full_calculation_verification(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('item1', 30.0)
        calc.add_item('item2', 20.0)
        subtotal = 50.0
        discount = 10.0
        discounted = 40.0
        shipping = 5.0
        total_before_tax = 45.0
        tax = 4.5
        expected = 49.5
        self.assertAlmostEqual(calc.calculate_total(discount=10.0), expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.add_item('orange', 1.75)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 5)
        calc.add_item('banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 8)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 3)
        calc.add_item('banana', 2.0, 2)
        calc.remove_item('apple')
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertEqual(calc.list_items(), ['apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.add_item('orange', 1.75)
        items = calc.list_items()
        self.assertIn('apple', items)
        self.assertIn('banana', items)
        self.assertIn('orange', items)
        self.assertEqual(len(items), 3)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.remove_item('apple')
        items = calc.list_items()
        self.assertNotIn('apple', items)
        self.assertIn('banana', items)

    def test_list_items_duplicate_names(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('apple', 2.0)
        items = calc.list_items()
        self.assertEqual(items.count('apple'), 1)

    def test_is_empty_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('laptop', 500.0)
        calc.add_item('mouse', 25.0, 2)
        self.assertEqual(calc.get_subtotal(), 550.0)
        self.assertEqual(calc.total_items(), 3)
        total = calc.calculate_total(discount=50.0)
        expected = 500.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_add_remove_add_sequence(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        calc.add_item('banana', 2.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.list_items(), ['banana'])

    def test_integration_custom_constructor_with_calculations(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item('item', 100.0)
        total = calc.calculate_total()
        expected = (100.0 + 15.0) * 1.05
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_threshold_boundary_behavior(self):
        calc = OrderCalculator()
        calc.add_item('item1', 50.0)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)
        calc.add_item('item2', 50.0)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)
        calc.remove_item('item2')
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)

    def test_integration_multiple_operations_consistency(self):
        calc = OrderCalculator()
        calc.add_item('a', 10.0, 2)
        calc.add_item('b', 20.0, 1)
        calc.add_item('c', 5.0, 4)
        self.assertEqual(calc.get_subtotal(), 60.0)
        self.assertEqual(calc.total_items(), 7)
        self.assertFalse(calc.is_empty())
        self.assertEqual(len(calc.list_items()), 3)
        calc.remove_item('b')
        self.assertEqual(calc.get_subtotal(), 40.0)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(len(calc.list_items()), 2)