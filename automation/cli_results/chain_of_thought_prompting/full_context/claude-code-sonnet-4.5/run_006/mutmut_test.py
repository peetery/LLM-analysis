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

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_string_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_string_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_string_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_none_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_list_as_parameter_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_slightly_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.0001)

    def test_init_tax_rate_slightly_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.0001)

    def test_add_first_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 100)
        self.assertEqual(calc.items[0]['quantity'], 100)

    def test_add_item_with_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 1)
        self.assertEqual(calc.items[0]['price'], 19.99)

    def test_add_duplicate_item_same_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 6)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 2)

    def test_add_item_none_as_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5, 2)

    def test_add_item_non_numeric_price_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '19.99', 2)

    def test_add_item_non_numeric_price_list_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', [10], 2)

    def test_add_item_non_integer_quantity_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_add_item_non_integer_quantity_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '2')

    def test_add_item_empty_string_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 2)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 2)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0, 2)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -5)

    def test_add_item_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_very_long_name(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 1.5, 1)
        self.assertEqual(calc.items[0]['name'], long_name)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in calc.items])

    def test_remove_item_added_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_non_existent_item_from_populated_order_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_empty_string_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_with_special_characters(self):
        calc = OrderCalculator()
        special_name = 'Item\'s "Special" Name'
        calc.add_item(special_name, 1.5, 1)
        calc.remove_item(special_name)
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.add_item('Orange', 7.0, 1)
        self.assertEqual(calc.get_subtotal(), 42.0)

    def test_get_subtotal_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.99, 1000)
        self.assertEqual(calc.get_subtotal(), 990.0)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 2)
        calc.add_item('Banana', 5.49, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 45.47, places=2)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_after_adding_and_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.add_item('Orange', 7.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(calc.get_subtotal(), 27.0)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_ten_percent_to_decimal_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(19.99, 0.1)
        self.assertAlmostEqual(result, 17.991, places=3)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_apply_discount_non_numeric_subtotal_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_none_as_subtotal_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.2)

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
            calc.apply_discount(-50.0, 0.2)

    def test_apply_discount_slightly_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.0001)

    def test_apply_discount_slightly_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.0001)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_calculate_tax_on_decimal_amount(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(19.99)
        self.assertAlmostEqual(tax, 2.9985, places=4)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_very_small_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023, places=4)

    def test_calculate_tax_non_numeric_amount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 15.0)

    def test_calculate_total_no_discount_shipping_applies(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_shipping_applies(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 12)
        total = calc.calculate_total(discount=0.2)
        subtotal = 120.0
        discounted = subtotal * 0.8
        with_shipping = discounted + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 15)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 15)
        total = calc.calculate_total(discount=0.1)
        discounted = 150.0 * 0.9
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_subtotal_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 11.0, 10)
        total = calc.calculate_total(discount=0.1)
        discounted = 110.0 * 0.9
        with_shipping = discounted + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 15)
        total = calc.calculate_total(discount=0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_minimal_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        total = calc.calculate_total()
        expected = (1.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_type_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_invalid_discount_value_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_multiple_items_discount_near_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 20.0, 3)
        calc.add_item('Banana', 15.0, 2)
        calc.add_item('Orange', 10.0, 1)
        total = calc.calculate_total(discount=0.15)
        subtotal = 60.0 + 30.0 + 10.0
        discounted = subtotal * 0.85
        with_shipping = discounted + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_after_adding_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.add_item('Banana', 5.0, 10)
        calc.remove_item('Banana')
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_custom_tax_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, 4)
        total = calc.calculate_total()
        expected = (40.0 + 5.0) * 1.15
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

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_adding_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_resets_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_clear_allows_new_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 0.8, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_clear_parameters_unchanged(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana', 'Orange'})

    def test_list_items_with_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Orange'})

    def test_list_items_with_special_characters(self):
        calc = OrderCalculator()
        special_name = 'Item\'s "Special" Name'
        calc.add_item(special_name, 1.5, 1)
        items = calc.list_items()
        self.assertEqual(items, [special_name])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_order_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_to_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.add_item('Banana', 5.0, 3)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 65.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 58.5, places=2)
        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 10.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(tax, 15.755, places=3)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 84.255, places=2)

    def test_add_remove_readd_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['price'], 2.0)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_multiple_discount_calculations(self):
        calc = OrderCalculator()
        subtotal = 100.0
        result1 = calc.apply_discount(subtotal, 0.1)
        result2 = calc.apply_discount(subtotal, 0.2)
        result3 = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(result1, 90.0)
        self.assertEqual(result2, 80.0)
        self.assertEqual(result1, result3)

    def test_calculate_total_propagates_get_subtotal_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_propagates_apply_discount_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_subtotal_with_repeating_decimals(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        calc.add_item('Item2', 0.2, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.7, places=10)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(19.99)
        self.assertAlmostEqual(tax, 4.5977, places=4)

    def test_total_calculation_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 3)
        total = calc.calculate_total(discount=0.15)
        subtotal = 59.97
        discounted = subtotal * 0.85
        with_shipping = discounted + 10.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)