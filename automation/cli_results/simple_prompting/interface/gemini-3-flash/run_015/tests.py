import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.23
        self.threshold = 100.0
        self.shipping = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.threshold, shipping_cost=self.shipping)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -10.0, 1)

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, -1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '1')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Orange')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_typical(self):
        subtotal = 100.0
        discount = 20.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(50.0, 50.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -5.0)

    def test_apply_discount_exceeding_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 150.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_return_type(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_calculate_total_with_discount_logic(self):
        self.calc.add_item('Item', 100.0, 1)
        total_discounted = self.calc.calculate_total(discount=10.0)
        total_regular = self.calc.calculate_total(discount=0.0)
        self.assertLess(total_discounted, total_regular)

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Pear', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Apple', items)
        self.assertIn('Pear', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_state(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())