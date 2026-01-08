import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_greater_than_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_tax_rate_wrong_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_free_shipping_threshold_wrong_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_shipping_cost_wrong_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_initial_state_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_initial_total_items_is_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 1.0, 5)
        self.assertEqual(calc.total_items(), 8)

    def test_add_same_item_twice_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_name_wrong_type_int(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_add_item_name_wrong_type_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5, 1)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_add_item_price_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_quantity_wrong_type_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_add_item_quantity_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '1')

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5, 1)

    def test_add_item_decimal_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_remove_last_remaining_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_wrong_type_int(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_name_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_then_remove_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_mixed_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 2.0, 2)
        calc.add_item('Orange', 0.5, 10)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_after_adding_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_get_subtotal_large_values(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 999999.99, 100)
        self.assertAlmostEqual(calc.get_subtotal(), 99999999.0, places=2)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.05)
        self.assertEqual(result, 95.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.5')

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.5)

    def test_apply_discount_subtotal_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.5)

    def test_apply_discount_boundary_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_boundary_one(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 0.33)
        self.assertAlmostEqual(result, 66.9933, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_wrong_type_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_very_large_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(999999.99)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_different_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 15.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_very_small_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023, places=4)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(1000000.0)
        self.assertEqual(tax, 230000.0)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 50.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 150.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_default_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 125.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_discount_wrong_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.5')

    def test_calculate_total_complex_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 1)
        calc.add_item('Orange', 10.0, 3)
        total = calc.calculate_total(discount=0.1)
        subtotal = 30.0 * 2 + 20.0 * 1 + 10.0 * 3
        discounted = subtotal * 0.9
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_recalculation_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        calc.add_item('Banana', 50.0, 1)
        calc.remove_item('Banana')
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_crossing_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0, 1)
        total_no_discount = calc.calculate_total(discount=0.0)
        total_with_discount = calc.calculate_total(discount=0.2)
        discounted_subtotal = 120.0 * 0.8
        expected_with_discount = (discounted_subtotal + 10.0) * 1.23
        self.assertAlmostEqual(total_with_discount, expected_with_discount, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_five(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_quantity_one_each(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 1.0, 1)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Orange', 1.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_total_items_zero_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_add_item_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 1.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_order_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        items1 = calc.list_items()
        items2 = calc.list_items()
        self.assertEqual(items1, items2)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_new_calculator(self):
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

    def test_is_empty_after_adding_then_removing_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 15.0, 1)
        total1 = calc.calculate_total(discount=0.1)
        calc.add_item('Orange', 5.0, 3)
        total2 = calc.calculate_total(discount=0.1)
        calc.remove_item('Banana')
        total3 = calc.calculate_total(discount=0.1)
        self.assertNotEqual(total1, total2)
        self.assertNotEqual(total2, total3)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        calc.add_item('Banana', 5.0, 1)
        self.assertFalse(calc.is_empty())

    def test_floating_point_precision_multiple_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.11, 3)
        calc.add_item('Banana', 2.22, 2)
        total = calc.calculate_total(discount=0.15)
        self.assertIsInstance(total, float)

    def test_large_order_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(len(calc.list_items()), 1)
        self.assertFalse(calc.is_empty())

    def test_failed_add_item_no_state_change(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        try:
            calc.add_item('Apple', 15.0, 1)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 1)

    def test_failed_remove_item_no_state_change(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        try:
            calc.remove_item('Banana')
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Apple', calc.list_items())