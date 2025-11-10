import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
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

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_empty_items_list(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_string_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_string_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_string_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_none_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_list_as_parameter(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_single_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_same_item_accumulation(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, quantity=2)
        calc.add_item('Orange', 3.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_decimal_price(self):
        calc = OrderCalculator()
        calc.add_item('Product', 9.99)
        self.assertAlmostEqual(calc.get_subtotal(), 9.99)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, quantity=1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_minimum_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_very_long_name(self):
        calc = OrderCalculator()
        long_name = 'A' * 250
        calc.add_item(long_name, 10.0)
        self.assertIn(long_name, calc.list_items())

    def test_add_item_price_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.01)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_add_item_whitespace_in_name(self):
        calc = OrderCalculator()
        calc.add_item(' Product ', 5.0)
        self.assertIn(' Product ', calc.list_items())

    def test_add_item_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0)
        calc.clear_order()
        calc.add_item('New Item', 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=-1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_different_name_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 5.0)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_item_integer_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_add_item_string_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.50')

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, quantity=1.5)

    def test_add_item_string_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, quantity='5')

    def test_add_item_none_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', None)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.list_items()), 2)

    def test_remove_item_by_exact_name(self):
        calc = OrderCalculator()
        calc.add_item('Product', 5.0)
        calc.remove_item('Product')
        self.assertTrue(calc.is_empty())

    def test_remove_item_accumulated(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, quantity=3)
        calc.add_item('Item', 5.0, quantity=2)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Item')

    def test_remove_item_already_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitive(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_integer_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_list_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(['item'])

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, quantity=2)
        calc.add_item('Banana', 3.0, quantity=5)
        calc.add_item('Orange', 1.5, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 23.5)

    def test_get_subtotal_accumulated_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=5)
        calc.add_item('Item', 10.0, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 80.0)

    def test_get_subtotal_decimal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Product', 9.99, quantity=7)
        self.assertAlmostEqual(calc.get_subtotal(), 69.93)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 25.0)
        self.assertAlmostEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, quantity=1000)
        self.assertAlmostEqual(calc.get_subtotal(), 1000.0)

    def test_get_subtotal_many_items(self):
        calc = OrderCalculator()
        for i in range(25):
            calc.add_item(f'Item{i}', 1.0, quantity=2)
        self.assertAlmostEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_large_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(10000.0, 0.2)
        self.assertAlmostEqual(result, 8000.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(1000.0, 0.001)
        self.assertAlmostEqual(result, 999.0)

    def test_apply_discount_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.99)
        self.assertAlmostEqual(result, 1.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.5)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_above_one_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 2.0)

    def test_apply_discount_string_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.5)

    def test_apply_discount_string_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.5')

    def test_apply_discount_none_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_zero_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=25.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 25.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_very_high_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(10000.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_string_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_none_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_shipping_list_as_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping([100])

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_one_hundred_percent_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0)

    def test_calculate_tax_decimal_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=4)

    def test_calculate_tax_very_small_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100000.0)
        self.assertAlmostEqual(tax, 23000.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.08)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 8.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_string_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_none_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_tax_list_as_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax([100])

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, quantity=3)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 184.5)

    def test_calculate_total_with_shipping_cost(self):
        calc = OrderCalculator()
        calc.add_item('Item', 30.0, quantity=2)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 86.1)

    def test_calculate_total_tax_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 20.0, quantity=1)
        total = calc.calculate_total()
        expected = (20.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_default_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_one_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=1.0)
        self.assertAlmostEqual(total, 12.3)

    def test_calculate_total_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 25.0)
        total = calc.calculate_total()
        expected = (25.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_large_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=50)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 6150.0)

    def test_calculate_total_multiple_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total1 = calc.calculate_total()
        total2 = calc.calculate_total()
        self.assertAlmostEqual(total1, total2)

    def test_calculate_total_after_item_changes(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 40.0)
        total2 = calc.calculate_total()
        self.assertNotAlmostEqual(total1, total2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_string_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_none_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount=None)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=10)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_multiple_items_sum(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, quantity=2)
        calc.add_item('Item2', 20.0, quantity=5)
        calc.add_item('Item3', 30.0, quantity=3)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_accumulated_items(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=5)
        calc.add_item('Item', 10.0, quantity=3)
        self.assertEqual(calc.total_items(), 8)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, quantity=5)
        calc.add_item('Item2', 20.0, quantity=3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_many_items(self):
        calc = OrderCalculator()
        for i in range(50):
            calc.add_item(f'Item{i}', 1.0, quantity=2)
        self.assertEqual(calc.total_items(), 100)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_add(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.clear_order()
        calc.add_item('Item2', 20.0)
        self.assertEqual(calc.total_items(), 1)

    def test_clear_multiple_times(self):
        calc = OrderCalculator()
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_get_subtotal_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        self.assertIn('Apple', calc.list_items())

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.add_item('Banana', 20.0)
        calc.add_item('Orange', 30.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.add_item('Banana', 20.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_unique_names_only(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=3)
        calc.add_item('Apple', 10.0, quantity=2)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.add_item('Banana', 20.0)
        calc.add_item('Orange', 30.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertNotIn('Banana', items)

    def test_list_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_new_calculator(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        calc.remove_item('Item2')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_some_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.add_item('Item3', 30.0)
        calc.remove_item('Item1')
        self.assertFalse(calc.is_empty())

    def test_integration_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=4)
        calc.add_item('Banana', 3.0, quantity=6)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 38.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 34.2)
        shipping = calc.calculate_shipping(discounted)
        self.assertAlmostEqual(shipping, 10.0)
        tax = calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(tax, 10.166, places=3)
        total = calc.calculate_total(0.1)
        self.assertAlmostEqual(total, 54.366, places=3)

    def test_integration_shipping_threshold_edge(self):
        calc = OrderCalculator()
        calc.add_item('Item', 99.0)
        total_below = calc.calculate_total()
        calc.clear_order()
        calc.add_item('Item', 100.0)
        total_at = calc.calculate_total()
        self.assertGreater(total_below, total_at)

    def test_integration_order_modification_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 20.0)
        calc.add_item('Item2', 30.0)
        total1 = calc.calculate_total()
        calc.remove_item('Item1')
        calc.add_item('Item3', 40.0)
        total2 = calc.calculate_total()
        self.assertNotAlmostEqual(total1, total2)

    def test_integration_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, quantity=5)
        calc.add_item('Item2', 20.0, quantity=3)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 8)
        self.assertEqual(len(calc.list_items()), 2)
        calc.remove_item('Item1')
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 1)

    def test_stress_many_items_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, quantity=1)
        self.assertEqual(len(calc.list_items()), 100)
        self.assertEqual(calc.total_items(), 100)
        self.assertAlmostEqual(calc.get_subtotal(), 100.0)

    def test_stress_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, quantity=10000)
        self.assertEqual(calc.total_items(), 10000)
        self.assertAlmostEqual(calc.get_subtotal(), 10000.0)

    def test_stress_high_precision_decimals(self):
        calc = OrderCalculator()
        calc.add_item('Item', 9.999, quantity=3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 29.997, places=3)

    def test_boundary_zero_tax_and_shipping(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 50.0)

    def test_boundary_one_hundred_percent_tax(self):
        calc = OrderCalculator(tax_rate=1.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 200.0)

    def test_boundary_free_shipping_always(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        calc.add_item('Item', 10.0)
        shipping = calc.calculate_shipping(10.0)
        self.assertAlmostEqual(shipping, 0.0)