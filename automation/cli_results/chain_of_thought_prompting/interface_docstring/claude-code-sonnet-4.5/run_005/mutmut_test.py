import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_with_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_with_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_with_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_with_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.8)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_duplicate_item_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_with_minimum_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01)
        self.assertEqual(calc.get_subtotal(), 0.01)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Free Item', 0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -1.5)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_with_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_with_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_with_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_with_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, quantity=1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.list_items()), 1)
        self.assertIn('Banana', calc.list_items())

    def test_remove_last_item_results_in_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_with_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, quantity=1)
        calc.add_item('Banana', 2.0, quantity=2)
        calc.add_item('Orange', 3.0, quantity=3)
        self.assertEqual(calc.get_subtotal(), 14.0)

    def test_get_subtotal_with_floating_point_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, quantity=2)
        self.assertAlmostEqual(calc.get_subtotal(), 39.98, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_calculate_tax_various_amounts(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(50.0)
        self.assertAlmostEqual(tax, 11.5, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=5)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=10)
        total = calc.calculate_total(discount=0.2)
        expected = (80.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=15)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping_cost(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=5)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, quantity=2)
        total = calc.calculate_total(discount=0.5)
        subtotal = 100.0
        discounted = 50.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_integration(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Apple', 20.0, quantity=3)
        calc.add_item('Banana', 10.0, quantity=2)
        total = calc.calculate_total(discount=0.1)
        subtotal = 80.0
        discounted = 72.0
        shipping = 15.0
        expected = (discounted + shipping) * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_affects_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 60.0, quantity=2)
        total_no_discount = calc.calculate_total()
        calc2 = OrderCalculator()
        calc2.add_item('Apple', 60.0, quantity=2)
        total_with_discount = calc2.calculate_total(discount=0.2)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_calculate_total_hundred_percent_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, quantity=1)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, quantity=1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_state_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_clear_order_can_add_after(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 2.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 1)

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
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.8)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items, ['Apple'])

    def test_list_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.list_items()), 1)
        calc.add_item('Banana', 2.0)
        self.assertEqual(len(calc.list_items()), 2)

    def test_list_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items, ['Banana'])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_state_transitions(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_integration_complete_workflow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, quantity=3)
        calc.add_item('Banana', 5.0, quantity=4)
        total = calc.calculate_total(discount=0.1)
        subtotal = 50.0
        discounted = 45.0
        shipping = 5.0
        expected = (discounted + shipping) * 1.1
        self.assertAlmostEqual(total, expected, places=2)
        self.assertEqual(calc.total_items(), 7)
        self.assertEqual(len(calc.list_items()), 2)

    def test_integration_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=2)
        calc.add_item('Banana', 5.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 35.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 1)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_integration_just_below_threshold_after_discount(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item', 110.0, quantity=1)
        total = calc.calculate_total(discount=0.1)
        discounted = 99.0
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_just_above_threshold_after_discount(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item', 112.0, quantity=1)
        total = calc.calculate_total(discount=0.1)
        discounted = 100.8
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Item', 19.99, quantity=3)
        total = calc.calculate_total(discount=0.15)
        subtotal = 59.97
        discounted = 50.9745
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_adding_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=2)
        calc.add_item('Apple', 5.0, quantity=3)
        calc.add_item('Apple', 5.0, quantity=1)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(len(calc.list_items()), 1)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_integration_complex_scenario(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=75.0, shipping_cost=12.0)
        calc.add_item('Laptop', 50.0, quantity=1)
        calc.add_item('Mouse', 15.0, quantity=2)
        calc.add_item('Keyboard', 25.0, quantity=1)
        total = calc.calculate_total(discount=0.25)
        subtotal = 105.0
        discounted = 78.75
        shipping = 0.0
        expected = (discounted + shipping) * 1.08
        self.assertAlmostEqual(total, expected, places=2)