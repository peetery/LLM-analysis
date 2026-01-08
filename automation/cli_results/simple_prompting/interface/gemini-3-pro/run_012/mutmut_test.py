import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertFalse(self.calc.is_empty())
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_accumulates_quantity(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Apple', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 40.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items[0] + items[1])

    def test_invalid_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad', -5.0)

    def test_invalid_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad', 5.0, -1)