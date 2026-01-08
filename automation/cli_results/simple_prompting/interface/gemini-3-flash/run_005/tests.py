import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_initial_state(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(len(self.calc.list_items()), 0)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1000.0)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_multiple_quantities(self):
        self.calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 75.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, -5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Valid', '10.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Valid', 10.0, '1')

    def test_remove_item_typical(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        try:
            self.calc.remove_item('NonExistent')
        except Exception as e:
            self.fail(f'remove_item() raised {type(e).__name__} unexpectedly for non-existent item')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(200.0, 50.0), 150.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 71.5)

    def test_calculate_total_with_discount_param(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=10.0), 120.7)

    def test_total_items_quantities(self):
        self.calc.add_item('A', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 10)

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_order(self):
        self.calc.add_item('Zebra', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Zebra', items)
        self.assertIn('Apple', items)

    def test_is_empty_toggle(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())

    def test_custom_init(self):
        custom = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=20.0)
        custom.add_item('Item', 40.0, 1)
        self.assertAlmostEqual(custom.calculate_total(), 62.0)