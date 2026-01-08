import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_multiple_types(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 7)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_item_accumulate_quantity(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(self.calculator.get_subtotal(), 8.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, -1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_apply_discount(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.2), 80.0)
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(subtotal, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calculator.add_item('ExpensiveWidget', 20.0, 10)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 216.0)