import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calc.calculate_shipping(0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100.0)

    def test_add_item_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Orange', 1.0, 1)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', -5.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', 5.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', 5.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0, 1)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 5.0, 1.5)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 10000000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 10000000000.0)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 5.0, 1)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 'five', 1)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_item_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.list_items()), 1)
        self.assertIn('Banana', calc.list_items())

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 10)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        calc.add_item('Item2', 0.2, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.9, places=10)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 110)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(-50.0), 10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(33.33), 7.6659, places=4)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(calc.calculate_total(), expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(calc.calculate_total(), expected, places=2)

    def test_calculate_total_default_discount_parameter(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(calc.calculate_total(), expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_qty_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_qty_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_populated(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_one_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        result = calc.list_items()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], str)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_some_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertFalse(calc.is_empty())

    def test_add_then_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        initial_empty = calc.is_empty()
        calc.remove_item('Apple')
        self.assertFalse(initial_empty)
        self.assertTrue(calc.is_empty())

    def test_order_modification_and_recalculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 60.0, 1)
        total2 = calc.calculate_total()
        self.assertGreater(total2, total1)