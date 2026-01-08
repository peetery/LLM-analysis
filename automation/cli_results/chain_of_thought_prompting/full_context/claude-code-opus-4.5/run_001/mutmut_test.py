import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_integer_values_accepted(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_tax_rate_zero_valid(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one_valid(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero_valid(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero_valid(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_free_shipping_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

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

    def test_add_item_default_quantity(self):
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
        calc.add_item('Banana', 0.75)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_integer_price_accepted(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2)
        self.assertEqual(calc.items[0]['price'], 2)

    def test_add_item_same_name_same_price_aggregates_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_quantity_one_minimum_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_price_just_above_zero_valid(self):
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
            calc.add_item('Apple', -5.0)

    def test_add_item_quantity_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_quantity_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_price_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.50')

    def test_add_item_quantity_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_leaves_other_items_intact(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_non_existent_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_typical_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_integer_discount_accepted(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent_returns_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal_returns_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_subtotal_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_integer_amount_accepted(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 25.0, 2)
        result = calc.calculate_total()
        self.assertAlmostEqual(result, 73.8, places=2)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 3)
        result = calc.calculate_total()
        self.assertAlmostEqual(result, 184.5, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 4)
        result = calc.calculate_total(0.2)
        self.assertAlmostEqual(result, 196.8, places=2)

    def test_calculate_total_default_discount_zero(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total()
        self.assertEqual(result, 60.0)

    def test_calculate_total_formula_verification(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 80.0, 1)
        result = calc.calculate_total(0.25)
        expected = 60.0 + 10.0 + 70.0 * 0.1
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 2)
        result = calc.calculate_total(1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 5)
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
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

    def test_list_items_returns_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        result = calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_list_items_unique_names_after_aggregation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        result = calc.list_items()
        self.assertEqual(result, ['Apple'])

    def test_list_items_empty_order_returns_empty_list(self):
        calc = OrderCalculator()
        result = calc.list_items()
        self.assertEqual(result, [])

    def test_is_empty_empty_order_returns_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items_returns_false(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear_order_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())