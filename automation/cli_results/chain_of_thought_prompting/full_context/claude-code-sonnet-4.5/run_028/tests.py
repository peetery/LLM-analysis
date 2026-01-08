import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_integer_parameters(self):
        calc = OrderCalculator(tax_rate=1, shipping_cost=5, free_shipping_threshold=100)
        self.assertEqual(calc.tax_rate, 1)
        self.assertEqual(calc.shipping_cost, 5)
        self.assertEqual(calc.free_shipping_threshold, 100)

    def test_string_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_string_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_string_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_none_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_list_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_tax_rate_slightly_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_single_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5, 5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 0.5)
        calc.add_item('Cherry', 2.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_with_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 1.99)
        self.assertEqual(calc.items[0]['price'], 1.99)

    def test_add_item_with_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Grape', 3)
        self.assertEqual(calc.items[0]['price'], 3)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 0.01, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_non_numeric_price_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.0')

    def test_add_item_non_integer_quantity_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 1.5)

    def test_add_item_none_as_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.0)

    def test_add_item_empty_string_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 0.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_after_quantity_increase(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_non_existent_item_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_already_removed_item_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.get_subtotal(), 1.0)

    def test_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 4)
        self.assertEqual(calc.get_subtotal(), 4.0)

    def test_subtotal_with_various_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.99, 1)
        calc.add_item('Banana', 0.49, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 2.97, places=2)

    def test_subtotal_on_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.05)
        self.assertEqual(result, 95.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_integer_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_string_discount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.5')

    def test_apply_discount_string_subtotal_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100.0', 0.5)

    def test_apply_discount_none_discount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.5)

    def test_calculate_shipping_threshold_met(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_threshold_not_met(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exact_threshold_match(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_string_input_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100.0')

    def test_calculate_shipping_none_input_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_string_amount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100.0')

    def test_calculate_tax_none_amount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total(discount=0.1)
        expected = 90.0 + 0.0 + 90.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_charged_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complete_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(discount=0.2)
        subtotal = 100.0
        discounted = 80.0
        shipping = 10.0
        tax = 90.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 125.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total()
        self.assertEqual(total, 100.0)

    def test_calculate_total_string_discount_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_calculate_total_none_discount_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount=None)

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_on_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Cherry', 2.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 0.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_and_re_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.clear_order()
        calc.add_item('Banana', 0.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_clear_after_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 0.5)
        calc.add_item('Cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_verify_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items, ['Apple'])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 0.5)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_not_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_not_empty_after_re_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.clear_order()
        calc.add_item('Banana', 0.5)
        self.assertFalse(calc.is_empty())

    def test_full_order_lifecycle(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 0.5, 2)
        total = calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_multiple_discounts_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total_no_discount = calc.calculate_total(0.0)
        total_half_discount = calc.calculate_total(0.5)
        self.assertLess(total_half_discount, total_no_discount)

    def test_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 111.11)
        total = calc.calculate_total(discount=0.1)
        discounted = 100.0
        tax = 100.0 * 0.23
        expected = discounted + 0.0 + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_order_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 99.99, 10)
        calc.add_item('Item2', 49.99, 20)
        calc.add_item('Item3', 19.99, 30)
        total = calc.calculate_total(discount=0.15)
        self.assertGreater(total, 0)

    def test_precision_test(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.1, 3)
        calc.add_item('Banana', 0.2, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.7, places=2)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_minimum_valid_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item('Apple', 0.01, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 0.01)

    def test_maximum_tax_scenario(self):
        calc = OrderCalculator(tax_rate=1.0)
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0
        self.assertEqual(total, expected)

    def test_float_precision_edge_cases(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.1, 1)
        calc.add_item('Banana', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(1000.0, 0.001)
        self.assertAlmostEqual(result, 999.0, places=2)

    def test_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 999999.99)