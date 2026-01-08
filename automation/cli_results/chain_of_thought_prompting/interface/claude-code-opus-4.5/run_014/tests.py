import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
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

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_with_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', -5.0)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_with_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item(None, 1.5)

    def test_add_item_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item(123, 1.5)

    def test_add_item_with_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Apple', 'expensive')

    def test_add_item_with_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Apple', 1.5, 'five')

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_with_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Apple', 1.5, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Banana')

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
        with self.assertRaises((TypeError, KeyError, ValueError)):
            calc.remove_item(None)

    def test_remove_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('apple')

    def test_remove_and_readd_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        calc.add_item('Apple', 2.0)
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 3)
        self.assertEqual(calc.get_subtotal(), 19.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_get_subtotal_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 10.0)

    def test_apply_discount_as_integer(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10)
        self.assertEqual(result, 90.0)

    def test_apply_discount_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(33.33, 33.33)
        self.assertAlmostEqual(result, 22.22, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-50.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

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

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

    def test_calculate_total_no_items(self):
        calc = OrderCalculator()
        result = calc.calculate_total()
        self.assertAlmostEqual(result, 12.3, places=2)

    def test_calculate_total_with_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        result = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        result = calc.calculate_total(10.0)
        expected = 90.0 + 10.0 + 100.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0)
        result = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        result = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_at_exact_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        result = calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        result = calc.calculate_total(100.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_calculation_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0)
        result = calc.calculate_total(20.0)
        discounted = 96.0
        shipping = 0.0
        tax = (96.0 + 0.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10.0)

    def test_calculate_total_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(150.0)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)

    def test_add_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 2.0)

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

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(items[0], 'Apple')
        self.assertEqual(items[1], 'Banana')
        self.assertEqual(items[2], 'Orange')

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_is_empty_on_new_order(self):
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

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(calc.get_subtotal(), 1050.0)
        self.assertEqual(calc.total_items(), 3)
        total = calc.calculate_total(10.0)
        discounted = 1050.0 * 0.9
        expected = discounted + 0.0 + discounted * 0.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_modification_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 10)
        calc.add_item('Banana', 3.0, 5)
        self.assertEqual(calc.get_subtotal(), 65.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 15.0)
        calc.add_item('Orange', 4.0, 3)
        self.assertEqual(calc.get_subtotal(), 27.0)
        total = calc.calculate_total()
        self.assertGreater(total, 0)

    def test_multiple_calculations_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total1 = calc.calculate_total(10.0)
        total2 = calc.calculate_total(10.0)
        total3 = calc.calculate_total(10.0)
        self.assertEqual(total1, total2)
        self.assertEqual(total2, total3)

    def test_state_consistency_after_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 2)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 40.0)
        self.assertFalse(calc.is_empty())
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(calc.get_subtotal(), 10.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(len(calc.list_items()), 1)