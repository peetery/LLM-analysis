import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calculator.total_items(), 4)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_update_quantity(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 12.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_apply_discount_zero(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 110.0)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(99.9)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Item', 50.0, 1)
        total = self.calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 1, 5)
        self.calculator.add_item('B', 1, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_list_items(self):
        self.calculator.add_item('Item A', 10.0)
        self.calculator.add_item('Item B', 20.0)
        items = self.calculator.list_items()
        self.assertIn('Item A', items)
        self.assertIn('Item B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())