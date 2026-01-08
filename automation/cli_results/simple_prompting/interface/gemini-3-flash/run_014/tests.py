import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.2
        self.threshold = 100.0
        self.shipping_cost = 15.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.threshold, shipping_cost=self.shipping_cost)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Product A', 50.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 100.0)
        self.assertIn('Product A', self.calc.list_items())

    def test_add_item_invalid_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Product', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Product', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Product', 10.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Product A', 10.0, 1)
        self.calc.remove_item('Product A')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existing(self):
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_apply_discount_typical(self):
        result = self.calc.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_exceeding_subtotal(self):
        result = self.calc.apply_discount(50.0, 60.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), self.shipping_cost)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_basic(self):
        self.calc.add_item('Item', 50.0, 1)
        expected = 50.0 + 15.0 + 10.0
        self.assertAlmostEqual(self.calc.calculate_total(), expected)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 120.0, 1)
        expected = 100.0 + 0.0 + 20.0
        self.assertAlmostEqual(self.calc.calculate_total(discount=20.0), expected)

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.calc.add_item('Item', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_invalid_types_for_calculations(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)