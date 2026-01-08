import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.2
        self.free_shipping_threshold = 100.0
        self.shipping_cost = 10.0
        self.calculator = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.free_shipping_threshold, shipping_cost=self.shipping_cost)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 60.0)
        self.assertEqual(calc.calculate_total(), 66.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_defaults(self):
        self.calculator.add_item('Banana', 1.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.0)

    def test_add_item_multiple_calls(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('A', 10.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('ZeroPrice', 0.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQtyNeg', 10.0, -1)

    def test_remove_item(self):
        self.calculator.add_item('Orange', 1.0, 5)
        self.calculator.remove_item('Orange')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertNotIn('Orange', self.calculator.list_items())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Ghost')

    def test_get_subtotal_mixed_items(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('B', 20.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 50.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 0.1
        expected = subtotal * (1 - discount)
        self.assertEqual(self.calculator.apply_discount(subtotal, discount), expected)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), self.shipping_cost)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        expected_tax = amount * self.tax_rate
        self.assertEqual(self.calculator.calculate_tax(amount), expected_tax)

    def test_calculate_total_simple(self):
        self.calculator.add_item('Item', 50.0)
        self.assertEqual(self.calculator.calculate_total(discount=0.0), 70.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('ExpensiveItem', 200.0)
        self.assertEqual(self.calculator.calculate_total(discount=0.1), 216.0)

    def test_clear_order(self):
        self.calculator.add_item('Item', 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items(self):
        self.calculator.add_item('X', 1.0)
        self.calculator.add_item('Y', 2.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('X', items)
        self.assertIn('Y', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())