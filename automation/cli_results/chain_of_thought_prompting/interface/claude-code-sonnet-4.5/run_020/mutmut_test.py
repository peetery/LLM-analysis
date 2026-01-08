import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_partial_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_very_high_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=10000.0)
        self.assertEqual(calc.free_shipping_threshold, 10000.0)

    def test_init_very_low_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.01)
        self.assertEqual(calc.free_shipping_threshold, 0.01)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_duplicate_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99, places=2)

    def test_add_item_fractional_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99, places=2)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Invalid', -10.0, 1)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Invalid', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0, 1)

    def test_add_item_none_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', None, 1)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 'invalid', 1)

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 'invalid')

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_remove_last_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 19.0, places=2)

    def test_get_subtotal_large_numbers(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 99999.99, 10)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.9, places=2)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.99, 3)
        calc.add_item('Item2', 5.49, 2)
        expected = 10.99 * 3 + 5.49 * 2
        self.assertAlmostEqual(calc.get_subtotal(), expected, places=2)

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_discount_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, 'invalid')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_very_high_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(10000.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertAlmostEqual(result, 230000.0, places=2)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(99.99)
        self.assertAlmostEqual(result, 14.9985, places=2)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 1)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_tax(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 0.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_shipping(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 0.0 + 50.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_calculate_total_discount_over_hundred(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=150.0)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_five(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_add_remove(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 3)
        calc.add_item('Item2', 20.0, 2)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.add_item('Banana', 20.0)
        calc.add_item('Cherry', 30.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.add_item('Banana', 20.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
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

    def test_is_empty_after_add_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        calc.add_item('B', 20.0, 2)
        calc.remove_item('A')
        calc.add_item('C', 30.0, 1)
        calc.clear_order()
        calc.add_item('D', 40.0, 1)
        self.assertEqual(calc.total_items(), 1)
        self.assertAlmostEqual(calc.get_subtotal(), 40.0)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 25.0, 2)
        calc.add_item('Item2', 50.0, 1)
        self.assertEqual(calc.total_items(), 3)
        self.assertAlmostEqual(calc.get_subtotal(), 100.0)
        self.assertEqual(len(calc.list_items()), 2)
        self.assertFalse(calc.is_empty())

    def test_large_order_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertAlmostEqual(calc.get_subtotal(), 100.0)