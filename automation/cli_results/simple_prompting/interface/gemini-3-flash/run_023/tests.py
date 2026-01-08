import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.23
        self.threshold = 100.0
        self.shipping = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.threshold, shipping_cost=self.shipping)

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1000.0)

    def test_add_item_multiple(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.calc.add_item('Keyboard', 50.0, 1)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 100.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Freebie', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, -5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0')

    def test_remove_item_success(self):
        self.calc.add_item('Item', 10.0)
        self.calc.remove_item('Item')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_missing(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_valid(self):
        res = self.calc.apply_discount(100.0, 20.0)
        self.assertEqual(res, 80.0)

    def test_apply_discount_full(self):
        res = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(res, 0.0)

    def test_apply_discount_overflow(self):
        res = self.calc.apply_discount(100.0, 120.0)
        self.assertEqual(res, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), self.shipping)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(self.threshold), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        expected = 100.0 * self.tax_rate
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), expected)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 71.5)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=20.0), 108.4)

    def test_calculate_total_free_shipping_case(self):
        self.calc.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())