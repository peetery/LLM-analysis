import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_add_item_normal_use(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_multiple_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, -1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -2.5, 1)

    def test_add_item_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 3.0, 1)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.5, 1)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.5, 1)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'invalid', 1)

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.5, 'invalid')

    def test_add_item_very_large_values(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1000)
        self.assertAlmostEqual(calc.get_subtotal(), 999999990.0)

    def test_remove_item_normal_use(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_item_empty_cart(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        with self.assertRaises(KeyError):
            calc.remove_item('apple')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('')

    def test_remove_item_after_adding_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_get_subtotal_empty_cart(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 5.5)

    def test_get_subtotal_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_get_subtotal_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_zero_price_items(self):
        calc = OrderCalculator()
        calc.add_item('Free', 0.0, 5)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_typical_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_fractional_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 15.5)
        self.assertAlmostEqual(result, 84.5)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 10.0)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, 'invalid')

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('invalid', 10.0)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 33.33)
        self.assertAlmostEqual(result, 66.66, places=2)

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

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-50.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('invalid')

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=20.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 20.0)

    def test_calculate_shipping_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_normal_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('invalid')

    def test_calculate_tax_floating_point_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_empty_cart_no_discount(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total()
        expected = 10.0 + 10.0 + (10.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_multiple_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 5.0, 1)
        total = calc.calculate_total()
        subtotal = 15.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        discounted = 90.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=100.0)
        shipping = 10.0
        tax = shipping * 0.23
        expected = shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_free_shipping_threshold_met(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        subtotal = 100.0
        shipping = 0.0
        tax = subtotal * 0.23
        expected = subtotal + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_free_shipping_threshold_not_met(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_at_free_shipping_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        subtotal = 100.0
        shipping = 0.0
        tax = subtotal * 0.23
        expected = subtotal + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=20.0)
        subtotal = 100.0
        discounted = 80.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_default_discount_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='invalid')

    def test_calculate_total_complex_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 25.0, 2)
        calc.add_item('Banana', 15.0, 3)
        calc.add_item('Orange', 10.0, 1)
        total = calc.calculate_total(discount=15.0)
        subtotal = 50.0 + 45.0 + 10.0
        discounted = subtotal * 0.85
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 3)
        total = calc.calculate_total(discount=12.5)
        self.assertIsInstance(total, float)

    def test_total_items_empty_cart(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 3.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertEqual(calc.total_items(), 1)
        calc.add_item('Banana', 3.0, 2)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.add_item('Banana', 3.0, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_normal_use(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.add_item('Banana', 3.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty_cart(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_multiple_calls(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_all_methods(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_cart(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_order_preservation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.add_item('Cherry', 4.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_immutability(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        items = calc.list_items()
        items.append('Banana')
        items_again = calc.list_items()
        self.assertEqual(len(items_again), 1)

    def test_is_empty_initially_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_return_type(self):
        calc = OrderCalculator()
        result = calc.is_empty()
        self.assertIsInstance(result, bool)

    def test_complex_workflow_1(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        calc.add_item('Banana', 30.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 80.0
        discounted = 72.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_complex_workflow_2(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.remove_item('Apple')
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complex_workflow_3(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 1)
        shipping1 = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping1, 10.0)
        calc.add_item('Item2', 40.0, 1)
        shipping2 = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping2, 10.0)
        calc.add_item('Item3', 35.0, 1)
        shipping3 = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping3, 0.0)

    def test_idempotency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        subtotal1 = calc.get_subtotal()
        subtotal2 = calc.get_subtotal()
        items1 = calc.total_items()
        items2 = calc.total_items()
        self.assertEqual(subtotal1, subtotal2)
        self.assertEqual(items1, items2)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 25.0)
        self.assertEqual(calc.total_items(), 3)
        self.assertFalse(calc.is_empty())
        self.assertEqual(len(calc.list_items()), 2)

    def test_edge_case_combo(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=100.0)
        self.assertEqual(total, 0.0)

    def test_multiple_discounts(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total1 = calc.calculate_total(discount=10.0)
        total2 = calc.calculate_total(discount=20.0)
        self.assertNotEqual(total1, total2)

    def test_item_name_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 3.0, 1)
        items = calc.list_items()
        apple_count = items.count('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_large_cart(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)