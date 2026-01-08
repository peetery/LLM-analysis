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

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_shipping_cost_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_single_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_item_same_item_twice_merges_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Apple', 2.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_quantity_one_minimum_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.0)

    def test_add_item_whitespace_only_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 2.0)

    def test_add_item_price_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_price_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -5.0)

    def test_add_item_quantity_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 0)

    def test_add_item_quantity_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0)

    def test_add_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0)

    def test_add_item_price_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '2.0')

    def test_add_item_quantity_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.0, 2.5)

    def test_add_item_quantity_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.0, '2')

    def test_remove_item_existing_item_successfully(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_verify_gone_from_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_item_non_existent_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 1.5, 4)
        self.assertAlmostEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 10)
        self.assertAlmostEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_single_item_minimal_price(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_exactly_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 0.0)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_exactly_one(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_subtotal_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.2)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_subtotal_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_subtotal_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_subtotal_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_subtotal_zero(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping([100])

    def test_calculate_shipping_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_calculate_tax_verify_calculation(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(50.0)
        self.assertAlmostEqual(result, 5.0)

    def test_calculate_tax_amount_zero(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_without_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 20.0, 2)
        total = calc.calculate_total()
        expected = (40.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_without_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 3)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 4)
        total = calc.calculate_total(0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_formula_verification(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Item', 30.0, 2)
        total = calc.calculate_total(0.0)
        expected = (60.0 + 15.0) * 1.1
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_default_discount_zero(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 3)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 4)
        total = calc.calculate_total(0.5)
        expected = 100.0 * 1.1
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_discount_string_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_calculate_total_discount_none_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(None)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_same_item_added_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Apple', 2.0, 4)
        self.assertEqual(calc.total_items(), 7)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_total_items_returns_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_returns_all_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_multiple_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_no_duplicates_when_same_item_added(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Apple', 2.0, 3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_is_empty_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Apple', 10.0, 5)
        calc.add_item('Banana', 5.0, 10)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 100.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 90.0)
        shipping = calc.calculate_shipping(discounted)
        self.assertAlmostEqual(shipping, 15.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(tax, 10.5)
        total = calc.calculate_total(0.1)
        self.assertAlmostEqual(total, 115.5)

    def test_integration_add_and_remove_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_integration_complete_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=8.0)
        calc.add_item('Widget', 15.0, 4)
        self.assertEqual(calc.total_items(), 4)
        self.assertFalse(calc.is_empty())
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 60.0)
        discounted = calc.apply_discount(subtotal, 0.25)
        self.assertAlmostEqual(discounted, 45.0)
        shipping = calc.calculate_shipping(discounted)
        self.assertAlmostEqual(shipping, 8.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(tax, 10.6)
        total = calc.calculate_total(0.25)
        self.assertAlmostEqual(total, 63.6)