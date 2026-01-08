import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Bread', 2.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 5.0)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Bread', self.calc.list_items())

    def test_add_item_multiple_types(self):
        self.calc.add_item('Bread', 2.5, 1)
        self.calc.add_item('Milk', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 5.5)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_updates_existing(self):
        self.calc.add_item('Bread', 2.5, 1)
        self.calc.add_item('Bread', 2.5, 3)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 1.0, -1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 1.0, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Bread', 'free', 1)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(200.0), 0.0)

    def test_calculate_tax_default(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_total_items_multiple_calls(self):
        self.calc.add_item('A', 1, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.calc.add_item('B', 1, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1, 1)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.list_items()), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1, 1)
        self.calc.add_item('Banana', 1, 1)
        items = self.calc.list_items()
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('X', 1, 1)
        self.assertFalse(self.calc.is_empty())