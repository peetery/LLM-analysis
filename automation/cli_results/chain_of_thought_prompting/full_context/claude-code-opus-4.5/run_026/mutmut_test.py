import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_minimum_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_maximum_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_integer_inputs_accepted(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_non_numeric_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_non_numeric_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_non_numeric_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_items_list_initialized_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

    def test_add_item_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_same_item_twice_merges_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_integer_price_accepted(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2)
        self.assertEqual(calc.items[0]['price'], 2)

    def test_add_item_quantity_exactly_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_price_very_small_positive(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.01)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_price_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_price_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_quantity_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_quantity_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_non_numeric_price_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_float_quantity_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_none_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_leaves_other_items_intact(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_non_existent_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_items_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_minimum_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_maximum_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_integer_inputs(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_non_numeric_subtotal_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

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

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(200.0)
        self.assertEqual(result, 46.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_integer_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        result = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 200.0, 1)
        result = calc.calculate_total(0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_default_discount_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        result = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_discounted_subtotal_exactly_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 125.0, 1)
        result = calc.calculate_total(0.2)
        discounted = 125.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_tax_on_discounted_subtotal_plus_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.items, [])

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(calc.items, [])

    def test_clear_order_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_returns_all_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        result = calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Apple', 1.5, 2)
        result = calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'Apple')

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
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        calc.add_item('Banana', 25.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 150.0)
        total = calc.calculate_total(0.1)
        discounted = 150.0 * 0.9
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_integration_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 99.0, 1)
        total_below = calc.calculate_total()
        expected_below = (99.0 + 10.0) * 1.23
        self.assertAlmostEqual(total_below, expected_below)
        calc.clear_order()
        calc.add_item('Apple', 100.0, 1)
        total_at = calc.calculate_total()
        expected_at = 100.0 * 1.23
        self.assertAlmostEqual(total_at, expected_at)

    def test_integration_quantity_merge_reflects_in_totals(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_integration_remove_and_recalculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        calc.add_item('Banana', 25.0, 2)
        calc.remove_item('Apple')
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 50.0)

    def test_integration_clear_and_restart(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        calc.clear_order()
        calc.add_item('Banana', 30.0, 3)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 90.0)