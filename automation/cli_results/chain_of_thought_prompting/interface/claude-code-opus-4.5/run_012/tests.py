import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_init_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_with_defaults(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', -5.0)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_add_item_with_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Item', 10.0, 2.5)

    def test_add_item_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item(123, 10.0)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Apple')

    def test_remove_item_with_empty_string(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('')

    def test_remove_item_then_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        calc.add_item('Cherry', 2.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Cherry', items)
        self.assertNotIn('Banana', items)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.99, 3)
        calc.add_item('Item2', 2.49, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 10.95, places=2)

    def test_get_subtotal_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Banana')
        self.assertEqual(calc.get_subtotal(), 4.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_small_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 150.0)
        self.assertGreaterEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_on_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(-50.0, 10.0)
        self.assertIsInstance(result, float)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 33.33)
        self.assertIsInstance(result, float)

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

    def test_calculate_shipping_slightly_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(-10.0)
        self.assertIsInstance(shipping, float)

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        shipping = calc.calculate_shipping(60.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_cost_configuration(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(10.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(-100.0)
        self.assertIsInstance(tax, float)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(200.0)
        self.assertEqual(tax, 46.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        discounted = 90.0
        expected = discounted + 10.0 + (discounted + 10.0) * 0.23
        self.assertIsInstance(total, float)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(discount=100.0)
        self.assertGreaterEqual(total, 0.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_calculate_total_default_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_calculate_total_order_verification(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(discount=20.0)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0.0)

    def test_calculate_total_free_shipping_boundary_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total_no_discount = calc.calculate_total(discount=0.0)
        total_with_discount = calc.calculate_total(discount=15.0)
        self.assertIsInstance(total_no_discount, float)
        self.assertIsInstance(total_with_discount, float)

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
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_then_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_verify_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_add_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 0.75)
        self.assertEqual(calc.list_items(), ['Banana'])

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
        calc.add_item('Banana', 0.75)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_returns_correct_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], str)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        calc.add_item('Cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false_one_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_false_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.75)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_new_instance(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 999.99, 1)
        calc.add_item('Mouse', 29.99, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1059.97, places=2)
        total = calc.calculate_total(discount=10.0)
        self.assertGreater(total, 0.0)

    def test_add_remove_add_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.list_items(), ['Banana'])
        self.assertEqual(calc.total_items(), 3)

    def test_multiple_calculations_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 50.0)
        total2 = calc.calculate_total()
        self.assertGreater(total2, total1)

    def test_free_shipping_boundary_with_discount_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0)
        shipping_before = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping_before, 0.0)
        discounted = calc.apply_discount(calc.get_subtotal(), 15.0)
        shipping_after = calc.calculate_shipping(discounted)
        self.assertEqual(shipping_after, 10.0)

    def test_order_modification_after_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 25.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_large_order_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 10.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 1000.0)