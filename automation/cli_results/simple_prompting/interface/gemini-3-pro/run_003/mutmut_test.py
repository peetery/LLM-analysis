import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Laptop', self.calculator.list_items())
        self.assertEqual(self.calculator.get_subtotal(), 1000.0)

    def test_add_item_multiple_quantities(self):
        self.calculator.add_item('Mouse', 20.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 100.0)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Keyboard', 50.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 50.0)

    def test_add_item_accumulate(self):
        self.calculator.add_item('Pen', 2.0, 5)
        self.calculator.add_item('Pen', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(self.calculator.get_subtotal(), 16.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('ZeroPrice', 0.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('NegativeQty', 10.0, -1)

    def test_remove_item_non_existent(self):
        with self.assertRaises((KeyError, ValueError)):
            self.calculator.remove_item('NonExistent')

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 0.1
        expected = 90.0
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, discount), expected)

    def test_apply_discount_zero(self):
        subtotal = 50.0
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 0.0), 50.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_with_discount_above_free_shipping(self):
        self.calculator.add_item('Console', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 216.0)

    def test_list_items(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)