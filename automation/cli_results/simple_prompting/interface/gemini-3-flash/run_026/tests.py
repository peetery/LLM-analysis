import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_default_values(self):
        default_calc = OrderCalculator()
        self.assertEqual(default_calc.calculate_tax(100.0), 23.0)
        self.assertEqual(default_calc.calculate_shipping(99.9), 10.0)
        self.assertEqual(default_calc.calculate_shipping(100.0), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Broken', -10.0, 1)

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Broken', 10.0, 0)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Broken', '10.0', 1)

    def test_remove_item_typical(self):
        self.calc.add_item('Keyboard', 50.0, 1)
        self.calc.remove_item('Keyboard')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_with_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_exceeding_subtotal(self):
        self.assertEqual(self.calc.apply_discount(50.0, 100.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -5.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(200.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 70.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 120.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=20.0), 120.0)

    def test_total_items_typical(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Orange', 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Orange', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())