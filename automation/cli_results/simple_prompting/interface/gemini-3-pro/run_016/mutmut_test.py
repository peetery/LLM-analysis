import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())
        calc.add_item('Test', 100.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertEqual(self.calc.get_subtotal(), 15.0)
        self.assertFalse(self.calc.is_empty())
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Book', 20.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_add_item_cumulative(self):
        self.calc.add_item('Pen', 1.0, 5)
        self.calc.add_item('Pen', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(self.calc.get_subtotal(), 8.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 6.0)
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_non_existing(self):
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Orange')

    def test_get_subtotal(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 42.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.2)
        self.assertEqual(discounted, 80.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=2.0)

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 10, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        self.calc.add_item('Item1', 10)
        self.calc.add_item('Item2', 20)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())