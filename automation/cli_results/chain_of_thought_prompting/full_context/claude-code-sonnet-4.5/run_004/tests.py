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
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_very_large_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=999999.99)
        self.assertEqual(calc.free_shipping_threshold, 999999.99)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_exceeds_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_with_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99)
        self.assertEqual(calc.items[0]['price'], 19.99)

    def test_add_item_with_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 20)
        self.assertEqual(calc.items[0]['price'], 20)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 999999.99)
        self.assertEqual(calc.items[0]['price'], 999999.99)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_name_as_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_name_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5)

    def test_add_item_price_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '19.99')

    def test_add_item_quantity_as_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 5.5)

    def test_add_item_quantity_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '5')

    def test_add_item_whitespace_only_name(self):
        calc = OrderCalculator()
        calc.add_item('   ', 1.5)
        self.assertEqual(calc.items[0]['name'], '   ')

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_from_multi_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertEqual(calc.list_items(), ['Apple', 'Cherry'])

    def test_remove_all_items_individually(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        calc.remove_item('Cherry')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_as_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 5)
        calc.add_item('Cherry', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_items_with_different_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Banana', 3.0, 3)
        self.assertEqual(calc.get_subtotal(), 19.0)

    def test_get_subtotal_mixed_integer_and_float_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2, 3)
        calc.add_item('Banana', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_get_subtotal_very_large(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 5000.0, 3)
        self.assertEqual(calc.get_subtotal(), 15000.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_after_clearing_order_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.0)
        self.assertEqual(result, 100)

    def test_apply_discount_partial_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.2)
        self.assertEqual(result, 80)

    def test_apply_discount_half_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.5)
        self.assertEqual(result, 50)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 1.0)
        self.assertEqual(result, 0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0, 0.5)
        self.assertEqual(result, 0)

    def test_apply_discount_small_discount_large_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(10000, 0.1)
        self.assertEqual(result, 9000)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100, 0.2)

    def test_apply_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100, 1.5)

    def test_apply_discount_subtotal_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100, '0.2')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(1)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_very_large_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(999999)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_subtotal_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(10000)
        self.assertEqual(result, 2300.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100)

    def test_calculate_tax_amount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(0.0)
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_paid_shipping_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_single_item(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item('Apple', 20.0, 1)
        total = calc.calculate_total(0.0)
        expected = 20.0 + 5.0 + 25.0 * 0.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 1)
        total = calc.calculate_total(0.0)
        subtotal = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.2
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_large_discount_affecting_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(0.4)
        discounted = 90.0
        shipping = 10.0
        tax = (90.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_maximum_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(1.0)
        discounted = 0.0
        shipping = 10.0
        tax = (0.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_negative_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_invalid_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_discount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_calculate_total_complete_order_flow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 40.0, 2)
        calc.add_item('Banana', 30.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 110.0
        discounted = 99.0
        shipping = 10.0
        tax = (99.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_exactly_at_free_shipping_after_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 110.0, 1)
        total = calc.calculate_total(0.1)
        discounted = 99.0
        shipping = 10.0
        tax = (99.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

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
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Cherry', 2.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_and_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_and_verify_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.8, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana', 'Cherry'})

    def test_list_items_duplicate_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_order_of_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Cherry'})

    def test_is_empty_new_instance(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_failed_add(self):
        calc = OrderCalculator()
        try:
            calc.add_item('', 1.5)
        except ValueError:
            pass
        self.assertTrue(calc.is_empty())

    def test_complete_purchase_flow_integration(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=8.0)
        calc.add_item('Laptop', 500.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Keyboard', 75.0, 1)
        calc.remove_item('Mouse')
        total = calc.calculate_total(0.1)
        subtotal = 575.0
        discounted = 517.5
        shipping = 0.0
        tax = 517.5 * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_add_again_integration(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.items), 1)

    def test_multiple_discount_scenarios_integration(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(0.0)
        total2 = calc.calculate_total(0.1)
        total3 = calc.calculate_total(0.5)
        self.assertGreater(total1, total2)
        self.assertGreater(total2, total3)

    def test_shipping_threshold_boundary_integration(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 111.11, 1)
        total = calc.calculate_total(0.1)
        discounted = 99.999
        shipping = 10.0
        tax = (99.999 + 10.0) * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_all_methods_workflow_integration(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Banana', 1.5, 3)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 8)
        self.assertEqual(set(calc.list_items()), {'Apple', 'Banana'})
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 14.5)
        total = calc.calculate_total(0.2)
        self.assertGreater(total, 0)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_empty_add_clear_add_cycle_integration(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        calc.add_item('Banana', 2.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 1)

    def test_large_order_processing_integration(self):
        calc = OrderCalculator()
        for i in range(25):
            calc.add_item(f'Item{i}', 10.0, 2)
        self.assertEqual(calc.total_items(), 50)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 500.0)

    def test_tax_calculation_at_each_step_integration(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 80.0, 1)
        total1 = calc.calculate_total(0.0)
        total2 = calc.calculate_total(0.25)
        self.assertNotEqual(total1, total2)

    def test_duplicate_item_edge_cases_integration(self):
        calc = OrderCalculator()
        for i in range(5):
            calc.add_item('Apple', 1.5, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)
        self.assertEqual(calc.total_items(), 5)

    def test_error_recovery_integration(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        try:
            calc.add_item('Apple', 2.0)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['price'], 1.5)

    def test_very_small_prices_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 100)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1.0, places=2)

    def test_very_large_quantities_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, 999999)
        self.assertEqual(calc.total_items(), 999999)

    def test_floating_point_precision_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.99, 3)
        calc.add_item('Item2', 0.33, 7)
        subtotal = calc.get_subtotal()
        expected = 10.99 * 3 + 0.33 * 7
        self.assertAlmostEqual(subtotal, expected, places=2)

    def test_zero_shipping_cost_configuration_edge_case(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item', 50.0, 1)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_single_item_order_variations_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 5.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertFalse(calc.is_empty())

    def test_exactly_at_free_shipping_boundary_edge_case(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping1 = calc.calculate_shipping(99.99)
        shipping2 = calc.calculate_shipping(100.0)
        shipping3 = calc.calculate_shipping(100.01)
        self.assertEqual(shipping1, 10.0)
        self.assertEqual(shipping2, 0.0)
        self.assertEqual(shipping3, 0.0)

    def test_maximum_tax_rate_edge_case(self):
        calc = OrderCalculator(tax_rate=1.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 1.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_minimum_values_everywhere_edge_case(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 50.0)