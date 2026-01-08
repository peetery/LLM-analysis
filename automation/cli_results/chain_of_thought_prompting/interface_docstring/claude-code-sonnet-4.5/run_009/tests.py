import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(len(calc.items), 0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_minimum_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_maximum_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_exceeds_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_add_item_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_duplicate_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, quantity=2)
        calc.add_item('Orange', 3.0, quantity=3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_price_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_quantity_not_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, quantity=2.5)

    def test_add_item_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_quantity_one_minimum_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 5.0, quantity=1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_from_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
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

    def test_remove_item_case_sensitive(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertAlmostEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        self.assertAlmostEqual(calc.get_subtotal(), 3.5)

    def test_get_subtotal_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_mixed_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=1)
        self.assertAlmostEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_exceeds_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_subtotal_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_apply_discount_zero_subtotal_returns_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 0.15)
        self.assertAlmostEqual(result, 84.9915, places=2)

    def test_calculate_shipping_equals_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_exceeds_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 15.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 10.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_hundred_percent_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_below_threshold_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total(discount=0.5)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_above_threshold_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 200.0)
        total = calc.calculate_total(discount=0.2)
        expected = 160.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(discount=1.0)
        self.assertAlmostEqual(total, 0.0)

    def test_calculate_total_discounted_subtotal_equals_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 200.0)
        total = calc.calculate_total(discount=0.5)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_exceeds_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_discount_not_number_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_calculate_total_integration_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, quantity=2)
        calc.add_item('Banana', 20.0, quantity=3)
        total = calc.calculate_total(discount=0.1)
        subtotal = 60.0 + 60.0
        discounted = subtotal * 0.9
        shipping = 0.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 99.99)
        total = calc.calculate_total(discount=0.15)
        self.assertGreater(total, 0.0)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Banana', 2.0, quantity=2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_total_items_returns_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_list_items_returns_empty_list(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

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
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_complete_shopping_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, quantity=2)
        calc.add_item('Banana', 20.0, quantity=3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 120.0)
        total = calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0.0)

    def test_integration_state_after_failed_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        try:
            calc.add_item('', 2.0)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')

    def test_integration_reach_exact_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_integration_remove_items_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 150.0)
        calc.add_item('Cheap', 10.0)
        calc.remove_item('Expensive')
        total = calc.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_integration_multiple_discount_applications(self):
        calc = OrderCalculator()
        subtotal = 100.0
        discounted1 = calc.apply_discount(subtotal, 0.1)
        discounted2 = calc.apply_discount(discounted1, 0.1)
        self.assertAlmostEqual(discounted2, 81.0)

    def test_integration_tax_on_subtotal_discount_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        total = calc.calculate_total(discount=0.2)
        subtotal = 80.0
        discounted = 64.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_integration_large_quantities_and_prices(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1000.0, quantity=100)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 100000.0)

    def test_integration_small_prices_and_discount_rounding(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, quantity=100)
        total = calc.calculate_total(discount=0.15)
        self.assertGreater(total, 0.0)

    def test_integration_partial_operations_state_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.add_item('Orange', 1.0, quantity=1)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertEqual(calc.total_items(), 3)
        self.assertIn('Apple', calc.list_items())
        self.assertIn('Orange', calc.list_items())
        self.assertNotIn('Banana', calc.list_items())