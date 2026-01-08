import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_boundary_tax_rate_at_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_boundary_tax_rate_at_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_invalid_tax_rate_below_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_invalid_tax_rate_above_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_invalid_tax_rate_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_invalid_tax_rate_type_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_integer_parameters_accepted(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Cherry', 3.0, 1)
        self.assertEqual(len(calc.items), 3)

    def test_add_duplicate_item_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(calc.items[0]['quantity'], 10)

    def test_add_item_with_same_name_but_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_empty_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_whitespace_only_item_name(self):
        calc = OrderCalculator()
        calc.add_item(' ', 1.5, 1)
        self.assertEqual(calc.items[0]['name'], ' ')

    def test_non_string_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0, 1)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_large_quantity_value(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000000)
        self.assertEqual(calc.items[0]['quantity'], 1000000)

    def test_float_price_precision(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 1)
        self.assertEqual(calc.items[0]['price'], 19.99)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_after_quantity_increment(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_subtotal_after_adding_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_subtotal_with_fractional_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 1)
        self.assertEqual(calc.get_subtotal(), 19.99)

    def test_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_partial_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_small_discount_ten_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_negative_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.1)

    def test_zero_subtotal_for_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_non_numeric_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_integer_inputs_for_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_at_threshold_exactly(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_shipping_zero_discounted_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_non_numeric_discounted_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_with_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 50.0 + 10.0 + 60.0 * 0.23)

    def test_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 150.0 + 0.0 + 150.0 * 0.23)

    def test_total_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 50.0 + 10.0 + 60.0 * 0.23)

    def test_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_with_zero_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 50.0 + 10.0 + 60.0 * 0.23)

    def test_total_with_maximum_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=1.0)
        self.assertEqual(total, 0.0 + 10.0 + 10.0 * 0.23)

    def test_total_with_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_total_with_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_tax_applied_after_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected_tax = (50.0 + 10.0) * 0.23
        self.assertEqual(total, 50.0 + 10.0 + expected_tax)

    def test_total_integer_discount_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=0)
        self.assertEqual(total, 100.0 + 0.0 + 100.0 * 0.23)

    def test_empty_order_count(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_single_item_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_multiple_items_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_count_after_quantity_increment(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_count_after_item_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_re_add_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_list_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_after_adding_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_new_order_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_order_with_items_not_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_order_after_clear_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_order_after_add_then_remove_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Laptop', 500.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        total = calc.calculate_total(discount=0.1)
        subtotal = 550.0
        discounted = 495.0
        shipping = 0.0
        tax = 495.0 * 0.2
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_multiple_discount_scenarios(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(discount=0.0)
        total2 = calc.calculate_total(discount=0.5)
        self.assertNotEqual(total1, total2)

    def test_tax_calculation_on_mixed_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 30.0, 1)
        calc.add_item('B', 40.0, 1)
        total = calc.calculate_total(discount=0.1)
        subtotal = 70.0
        discounted = 63.0
        shipping = 10.0
        tax = 73.0 * 0.23
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_modify_order_and_recalculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 60.0, 1)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_edge_case_single_cheap_item(self):
        calc = OrderCalculator()
        calc.add_item('Candy', 1.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 1.0 + 10.0 + 11.0 * 0.23)

    def test_edge_case_single_expensive_item(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 500.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 500.0 + 0.0 + 500.0 * 0.23)

    def test_precision_in_full_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 3)
        total = calc.calculate_total(discount=0.15)
        subtotal = 59.97
        discounted = 50.9745
        shipping = 10.0
        tax = 60.9745 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=10)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 15.0, 1)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 2)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_remove_and_re_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.items), 1)

    def test_multiple_quantity_increments(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(calc.get_subtotal(), 60.0)