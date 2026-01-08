import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1000.0)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_multiple_items_and_quantities(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.calc.add_item('Keyboard', 50.0)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 100.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 'free')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', -10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Zero Quantity', 10.0, 0)

    def test_remove_item_typical(self):
        self.calc.add_item('Item1', 10.0)
        self.calc.remove_item('Item1')
        self.assertTrue(self.calc.is_empty())

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 15.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Book', 50.0)
        total = self.calc.calculate_total(discount=0.0)
        self.assertGreater(total, 50.0)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('X', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)