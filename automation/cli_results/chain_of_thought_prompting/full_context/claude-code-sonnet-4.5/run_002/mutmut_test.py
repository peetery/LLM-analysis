import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_integer_values_accepted_in_init(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_boundary_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_boundary_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_boundary_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_boundary_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_items_list_initialized_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

    def test_type_error_tax_rate_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_type_error_tax_rate_as_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_type_error_tax_rate_as_list(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_type_error_free_shipping_threshold_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_type_error_shipping_cost_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_value_error_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_value_error_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_value_error_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_value_error_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0)
        calc.add_item('Keyboard', 75.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_duplicate_item_same_name_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 2)
        calc.add_item('Laptop', 1000.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_duplicate_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(calc.items[0]['quantity'], 6)

    def test_float_price_accepted(self):
        calc = OrderCalculator()
        calc.add_item('Book', 19.99)
        self.assertEqual(calc.items[0]['price'], 19.99)

    def test_integer_price_accepted(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 20)
        self.assertEqual(calc.items[0]['price'], 20)

    def test_type_error_name_as_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_type_error_name_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_type_error_price_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_type_error_quantity_as_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 2.5)

    def test_type_error_quantity_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, '2')

    def test_value_error_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_value_error_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0.0)

    def test_value_error_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_value_error_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_value_error_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_value_error_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        with self.assertRaises(ValueError):
            calc.add_item('Laptop', 1200.0)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.remove_item('Laptop')
        self.assertEqual(len(calc.items), 0)

    def test_remove_one_item_from_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0)
        calc.add_item('Keyboard', 75.0)
        calc.remove_item('Mouse')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Mouse', [item['name'] for item in calc.items])

    def test_remove_item_by_exact_name(self):
        calc = OrderCalculator()
        calc.add_item('Laptop Pro', 1500.0)
        calc.add_item('Laptop', 1000.0)
        calc.remove_item('Laptop')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Laptop Pro')

    def test_type_error_remove_name_as_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_type_error_remove_name_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_value_error_item_doesnt_exist(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        with self.assertRaises(ValueError):
            calc.remove_item('Mouse')

    def test_value_error_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Item')

    def test_subtotal_with_single_item_quantity_1(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        self.assertEqual(calc.get_subtotal(), 1000.0)

    def test_subtotal_with_single_item_quantity_greater_than_1(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(calc.get_subtotal(), 75.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Keyboard', 75.0, 1)
        self.assertEqual(calc.get_subtotal(), 1125.0)

    def test_subtotal_calculation_accuracy(self):
        calc = OrderCalculator()
        calc.add_item('Book', 19.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 39.98, places=2)

    def test_value_error_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_float_subtotal_accepted_in_apply_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 0.1)
        self.assertAlmostEqual(result, 89.991, places=2)

    def test_integer_subtotal_accepted_in_apply_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.1)
        self.assertEqual(result, 90.0)

    def test_integer_discount_accepted(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_type_error_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_type_error_discount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_type_error_subtotal_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.1)

    def test_value_error_negative_subtotal_in_apply_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.1)

    def test_value_error_discount_less_than_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_value_error_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_subtotal_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_subtotal_equals_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_subtotal_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_zero_subtotal_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_integer_subtotal_accepted_in_calculate_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150)
        self.assertEqual(result, 0.0)

    def test_type_error_shipping_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_type_error_shipping_subtotal_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_tax_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_integer_amount_accepted_in_calculate_tax(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_type_error_tax_amount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_type_error_tax_amount_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_value_error_negative_amount_in_calculate_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_total_with_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 1000.0 + 0.0 + 1000.0 * 0.23)

    def test_total_with_discount_applied(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total(0.1)
        discounted = 900.0
        tax = discounted * 0.23
        self.assertEqual(total, discounted + 0.0 + tax)

    def test_total_with_free_shipping_threshold_met(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total()
        self.assertEqual(total, 1000.0 + 0.0 + 1000.0 * 0.23)

    def test_total_with_shipping_cost_threshold_not_met(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Mouse', 50.0)
        total = calc.calculate_total()
        tax = (50.0 + 10.0) * 0.23
        self.assertEqual(total, 50.0 + 10.0 + tax)

    def test_complex_integration_total(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0, 2)
        total = calc.calculate_total(0.2)
        subtotal = 1050.0
        discounted = 840.0
        shipping = 0.0
        tax = 840.0 * 0.23
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_total_equals_threshold_exactly_after_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 125.0)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        self.assertEqual(total, discounted + shipping + tax)

    def test_default_discount_parameter(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total()
        self.assertEqual(total, 1000.0 + 0.0 + 1000.0 * 0.23)

    def test_integer_discount_accepted_in_calculate_total(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total(0)
        self.assertEqual(total, 1000.0 + 0.0 + 1000.0 * 0.23)

    def test_type_error_total_discount_as_string(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_value_error_invalid_discount_in_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_value_error_empty_order_in_calculate_total(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_empty_order_returns_zero_total_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_single_item_quantity_1_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_single_item_quantity_greater_than_1_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_multiple_items_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 2)
        calc.add_item('Mouse', 25.0, 3)
        calc.add_item('Keyboard', 75.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_after_adding_duplicate_items_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_and_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_re_add_items(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.clear_order()
        calc.add_item('Mouse', 25.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Mouse')

    def test_empty_order_returns_empty_list_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_single_item_returns_list_with_one_name(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Laptop', items)

    def test_multiple_items_return_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0)
        calc.add_item('Keyboard', 75.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_duplicate_items_return_single_name(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Mouse', 25.0, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Mouse', items)

    def test_list_is_unordered_set_behavior(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.add_item('Mouse', 25.0)
        items = calc.list_items()
        self.assertEqual(set(items), {'Laptop', 'Mouse'})

    def test_new_order_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_order_with_items_is_not_empty(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        self.assertFalse(calc.is_empty())

    def test_order_after_clear_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_order_after_remove_all_items_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.remove_item('Laptop')
        self.assertTrue(calc.is_empty())

    def test_full_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 1050.0
        discounted = 945.0
        shipping = 0.0
        tax = 945.0 * 0.23
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_modify_order_and_recalculate(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total1 = calc.calculate_total()
        calc.add_item('Mouse', 25.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_shipping_threshold_edge_case(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 125.0)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        self.assertEqual(total, discounted + shipping + tax)

    def test_precision_test(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 19.99, 2)
        calc.add_item('Pen', 5.49, 3)
        subtotal = calc.get_subtotal()
        expected_subtotal = 19.99 * 2 + 5.49 * 3
        self.assertAlmostEqual(subtotal, expected_subtotal, places=2)

    def test_zero_tax_scenario(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 1000.0)
        total = calc.calculate_total()
        self.assertEqual(total, 1000.0)

    def test_maximum_discount_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Mouse', 50.0)
        total = calc.calculate_total(1.0)
        shipping = 10.0
        tax = (0.0 + shipping) * 0.23
        expected = 0.0 + shipping + tax
        self.assertEqual(total, expected)

    def test_add_and_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        calc.remove_item('Laptop')
        calc.add_item('Laptop', 1000.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Laptop')

    def test_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1000)
        self.assertEqual(calc.total_items(), 1000)
        self.assertEqual(calc.get_subtotal(), 10000.0)

    def test_many_items_in_order(self):
        calc = OrderCalculator()
        for i in range(50):
            calc.add_item(f'Item{i}', 10.0 + i, 1)
        self.assertEqual(len(calc.list_items()), 50)
        self.assertEqual(calc.total_items(), 50)

    def test_negative_subtotal_impossible(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        subtotal = calc.get_subtotal()
        self.assertGreater(subtotal, 0)

    def test_items_list_mutation_safety(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0)
        original_items = calc.items
        calc.add_item('Mouse', 25.0)
        self.assertIs(calc.items, original_items)

    def test_parameter_storage(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)