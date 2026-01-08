import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_integer_values(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

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

    def test_init_tax_rate_negative_raises_value_error(self):
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

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_free_shipping_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_item_single_default_quantity(self):
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
        calc.add_item('Orange', 2.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_same_item_twice_accumulates_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2, 1)
        self.assertEqual(calc.items[0]['price'], 2)

    def test_add_item_quantity_one_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01, 1)
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

    def test_add_item_name_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_name_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5)

    def test_add_item_price_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.50')

    def test_add_item_quantity_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_quantity_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '2')

    def test_remove_item_single_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_multi_item_order(self):
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

    def test_remove_item_name_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_calculation_accuracy(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 5.0, 2)
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

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
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal_with_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

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
        self.assertEqual(result, 23.0)

    def test_calculate_tax_accuracy(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(50.0)
        self.assertEqual(result, 5.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.08)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 8.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, 1)
        result = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 80.0, 1)
        result = calc.calculate_total(0.2)
        discounted = 80.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 200.0, 1)
        result = calc.calculate_total(0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_complete_calculation(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 40.0, 1)
        result = calc.calculate_total(0.1)
        discounted = 40.0 * 0.9
        shipping = 5.0
        expected = (discounted + shipping) * 1.1
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_zero_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        result = calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_discount_greater_than_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_calculate_total_discount_string_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_calculate_total_discount_none_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(None)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 4)
        self.assertEqual(calc.total_items(), 9)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_items_list_reset(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

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
        calc.add_item('Banana', 0.75)
        calc.add_item('Orange', 2.0)
        result = calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana', 'Orange'})

    def test_list_items_matches_added_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        result = calc.list_items()
        self.assertIn('Item1', result)
        self.assertIn('Item2', result)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
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
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 100.0)
        total = calc.calculate_total(0.1)
        discounted = 100.0 * 0.9
        expected = discounted * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_add_remove_verify_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_integration_add_same_item_accumulate_get_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Apple', 2.0, 2)
        self.assertEqual(calc.items[0]['quantity'], 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_integration_clear_order_then_get_subtotal_raises(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()