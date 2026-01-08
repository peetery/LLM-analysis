import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Book', 20.0, 1)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)
        self.assertIn('Book', self.calculator.list_items())

    def test_add_item_multiple_items(self):
        self.calculator.add_item('Book', 20.0, 1)
        self.calculator.add_item('Pen', 5.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)
        items = self.calculator.list_items()
        self.assertIn('Book', items)
        self.assertIn('Pen', items)

    def test_add_item_accumulate_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(self.calculator.get_subtotal(), 16.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, -5)

    def test_add_item_invalid_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item('', 10.0)
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item(None, 10.0)

    def test_get_subtotal(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 50.5, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 70.5)

    def test_apply_discount(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 90.0)
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        tax = self.calculator.calculate_tax(amount)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_simple(self):
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('ExpensiveItem', 200.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 246.0, delta=0.01)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertTrue(total > 0)

    def test_list_items(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.add_item('B', 2.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_custom_config(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        custom_calc.add_item('Item', 40.0)
        self.assertEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)