import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.get_subtotal(), 15.0)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 2.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 2.0)

    def test_add_item_multiple_calls(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(self.calculator.get_subtotal(), 11.0)
        self.assertEqual(len(self.calculator.list_items()), 2)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, -1)

    def test_remove_item_not_found(self):
        self.calculator.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.2)
        self.assertEqual(discounted, 80.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

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
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Item1', 50.0)
        total = self.calculator.calculate_total()
        self.assertTrue(total > 50.0)
        self.assertIsInstance(total, float)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item1', 200.0)
        expected_total = 200.0 + 0.0 + 200.0 * 0.2
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item1', 100.0)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertTrue(total > 0)

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 20, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 20)
        items = self.calculator.list_items()
        self.assertListEqual(sorted(items), ['A', 'B'])

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())