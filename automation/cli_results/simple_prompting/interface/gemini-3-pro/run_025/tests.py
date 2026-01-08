import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_initial_state(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)
        self.assertIn('Apple', self.calc.list_items()[0])

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.0)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', 5.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Ghost')

    def test_get_subtotal_mixed_items(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount_val = 10.0
        result = self.calc.apply_discount(subtotal, discount_val)
        self.assertTrue(result < subtotal)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(99.9)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_or_above_threshold(self):
        shipping_at = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping_at, 0.0)
        shipping_above = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping_above, 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        tax = self.calc.calculate_tax(amount)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        expected_subtotal = 50.0
        expected_tax = 50.0 * 0.2
        expected_shipping = 10.0
        self.assertAlmostEqual(total, expected_subtotal + expected_tax + expected_shipping)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 240.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total(discount=10.0)
        self.assertTrue(total > 0)

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('A', str(items))
        self.assertIn('B', str(items))