import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.23
        self.threshold = 100.0
        self.shipping = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.threshold, shipping_cost=self.shipping)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 8.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1200.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1200.0)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 75.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0')

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -1.0)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '1')

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_remove_item_success(self):
        self.calc.add_item('Book', 15.0)
        self.calc.remove_item('Book')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_missing(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_exceeding_subtotal(self):
        self.assertEqual(self.calc.apply_discount(50.0, 60.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-1.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_no_discount_with_shipping(self):
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 71.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(50.0), 184.5)

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('X', 1.0)
        self.assertFalse(self.calc.is_empty())