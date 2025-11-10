import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_boundary_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_boundary_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_none_as_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_list_as_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_add_item_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 2)
        calc.add_item('Orange', 1.5, 3)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_duplicate_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_quantities_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0, 1)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.0, 1)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '10.50', 1)

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 3.5)

    def test_add_item_none_as_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', None, 1)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 1)
        calc.add_item('Orange', 1.5, 1)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        names = [item['name'] for item in calc.items]
        self.assertIn('Apple', names)
        self.assertIn('Orange', names)
        self.assertNotIn('Banana', names)

    def test_remove_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_already_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 5.0, 1)
        calc.add_item('Orange', 7.5, 1)
        self.assertEqual(calc.get_subtotal(), 22.5)

    def test_get_subtotal_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_mixed_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 9.99, 1)
        calc.add_item('Banana', 15.5, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 25.49, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_none_values(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_equal_to_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_cost_configured(self):
        calc = OrderCalculator(shipping_cost=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_threshold_configured(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(1.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_none_as_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_maximum_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_none_as_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_paid_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_to_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 110.0, 1)
        total = calc.calculate_total(discount=0.15)
        discounted = 93.5
        shipping = 10.0
        tax = (93.5 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=1.0)
        discounted = 0.0
        shipping = 10.0
        tax = (0.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complex(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 15.0, 3)
        calc.add_item('Orange', 20.0, 1)
        total = calc.calculate_total(discount=0.1)
        subtotal = 60.0 + 45.0 + 20.0
        discounted = subtotal * 0.9
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_none_as_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount=None)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Orange', 1.5, 4)
        self.assertEqual(calc.total_items(), 9)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 2)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_and_readd(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        calc.add_item('Banana', 0.5, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_unique(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 1)
        calc.add_item('Orange', 1.5, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_is_empty_new_calculator(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_full_workflow_integration(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 15.0, 3)
        calc.add_item('Orange', 20.0, 1)
        calc.remove_item('Banana')
        total = calc.calculate_total(discount=0.1)
        subtotal = 60.0 + 20.0
        discounted = subtotal * 0.9
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_add_remove_cycles(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Orange', 1.5, 1)
        self.assertEqual(len(calc.items), 2)
        names = [item['name'] for item in calc.items]
        self.assertIn('Banana', names)
        self.assertIn('Orange', names)

    def test_recalculate_total_after_modifications(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 60.0, 1)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)
        self.assertGreater(total2, total1)

    def test_very_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_very_large_prices(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99, places=2)

    def test_very_small_prices(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01, places=2)

    def test_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_long_item_names(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 1.0, 1)
        self.assertEqual(calc.items[0]['name'], long_name)

    def test_special_characters_in_name(self):
        calc = OrderCalculator()
        calc.add_item('Item!@#$%^&*()', 1.0, 1)
        self.assertEqual(calc.items[0]['name'], 'Item!@#$%^&*()')

    def test_unicode_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Café', 5.0, 1)
        calc.add_item('日本', 10.0, 1)
        items = calc.list_items()
        self.assertIn('Café', items)
        self.assertIn('日本', items)