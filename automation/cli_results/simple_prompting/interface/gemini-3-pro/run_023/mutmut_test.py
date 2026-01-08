import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 10)
        self.assertEqual(self.calc.get_subtotal(), 15.0)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_multiple_valid(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calc.total_items(), 6)
        self.assertEqual(self.calc.get_subtotal(), 5.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_item_defaults(self):
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 2.0)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQtyNeg', 5.0, -1)

    def test_remove_item(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Banana', 2.0, 2)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 4.0)
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('NonExistent')

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(101.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_total_no_discount(self):
        calc_no_tax = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100, shipping_cost=10)
        calc_no_tax.add_item('A', 50, 1)
        self.assertEqual(calc_no_tax.calculate_total(), 60.0)

    def test_list_items(self):
        self.calc.add_item('A', 10, 1)
        self.calc.add_item('B', 20, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_total_items(self):
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 20, 3)
        self.assertEqual(self.calc.total_items(), 5)