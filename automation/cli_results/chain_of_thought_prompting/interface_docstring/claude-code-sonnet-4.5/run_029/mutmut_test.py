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

    def test_init_tax_rate_at_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_at_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_at_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_at_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_wrong_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_wrong_type_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_free_shipping_threshold_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 2.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_duplicate_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 2.5, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 4)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99)
        self.assertEqual(calc.items[0]['price'], 999999.99)

    def test_add_item_very_low_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.5, 1)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -5.0, 1)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, -3)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0)

    def test_add_item_name_not_string_int(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.5, 1)

    def test_add_item_name_not_string_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 2.5, 1)

    def test_add_item_price_not_numeric_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '2.5', 1)

    def test_add_item_quantity_not_int_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.5, 1.5)

    def test_add_item_quantity_not_int_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.5, '1')

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in calc.items])

    def test_remove_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_already_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_not_string_int(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_name_not_string_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Cherry', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_get_subtotal_multiple_items_with_aggregated_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_get_subtotal_very_large_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 50000.0, 10)
        self.assertEqual(calc.get_subtotal(), 500000.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.05)
        self.assertEqual(result, 95.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.5)

    def test_apply_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_subtotal_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.5)

    def test_apply_discount_discount_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.5')

    def test_apply_discount_subtotal_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.5)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_input_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100.0')

    def test_calculate_shipping_input_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(1000000.0)
        self.assertEqual(tax, 230000.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_one_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_amount_wrong_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100.0')

    def test_calculate_tax_amount_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_no_discount_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_still_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 200.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_drops_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 120.0)
        total = calc.calculate_total(discount=0.3)
        discounted = 120.0 * 0.7
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 125.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 125.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_maximum_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_explicit_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_default_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complex_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 4)
        total = calc.calculate_total(discount=0.1)
        subtotal = 30.0 + 20.0
        discounted = subtotal * 0.9
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_below_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_discount_wrong_type_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.5')

    def test_calculate_total_discount_none(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(None)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Cherry', 3.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        calc.add_item('Banana', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_clear_order_verify_all_items_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 2.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_order_of_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_newly_created_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_multiple_items_present(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        self.assertFalse(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 35.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 31.5)
        total = calc.calculate_total(discount=0.1)
        expected = (31.5 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_calculate_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 20.0, 3)
        calc.add_item('Banana', 10.0, 2)
        calc.remove_item('Banana')
        total = calc.calculate_total()
        expected = (60.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_discount_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total1 = calc.calculate_total(discount=0.1)
        total2 = calc.calculate_total(discount=0.2)
        self.assertNotEqual(total1, total2)

    def test_shipping_threshold_crossing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 60.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_order_reuse(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        calc.calculate_total()
        calc.clear_order()
        calc.add_item('Banana', 30.0)
        total = calc.calculate_total()
        expected = (30.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_item_quantity_aggregation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.items[0]['quantity'], 5)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_state_after_exception(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        try:
            calc.add_item('', 5.0)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')

    def test_multiple_operations(self):
        calc = OrderCalculator()
        for i in range(10):
            calc.add_item(f'Item{i}', float(i + 1))
        self.assertEqual(len(calc.items), 10)
        calc.remove_item('Item5')
        self.assertEqual(len(calc.items), 9)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_boundary_interactions(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total(discount=0.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_floating_point_arithmetic(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_rounding_in_total(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.99)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_very_small_prices(self):
        calc = OrderCalculator()
        calc.add_item('Tiny', 0.001, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.001, places=3)

    def test_large_numbers(self):
        calc = OrderCalculator()
        calc.add_item('Huge', 999999.99, 999)
        subtotal = calc.get_subtotal()
        expected = 999999.99 * 999
        self.assertAlmostEqual(subtotal, expected, places=2)

    def test_unicode_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Äpfel', 2.5)
        calc.add_item('香蕉', 1.5)
        items = calc.list_items()
        self.assertIn('Äpfel', items)
        self.assertIn('香蕉', items)

    def test_very_long_item_names(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 2.5)
        items = calc.list_items()
        self.assertIn(long_name, items)

    def test_special_characters_in_names(self):
        calc = OrderCalculator()
        calc.add_item('Item@#$%', 2.5)
        items = calc.list_items()
        self.assertIn('Item@#$%', items)

    def test_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('apple', 2.5)
        self.assertEqual(len(calc.items), 2)

    def test_calculate_total_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total1 = calc.calculate_total()
        total2 = calc.calculate_total()
        self.assertEqual(total1, total2)
        self.assertEqual(len(calc.items), 1)

    def test_concurrent_like_operations(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0)
        for i in range(50):
            calc.remove_item(f'Item{i}')
        self.assertEqual(len(calc.items), 50)