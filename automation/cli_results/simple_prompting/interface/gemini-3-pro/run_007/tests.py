import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_initial_state(self):
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 100.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Price', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Qty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Qty', 10.0, -1)

    def test_remove_item_existing(self):
        self.calculator.add_item('Orange', 2.0, 3)
        self.calculator.remove_item('Orange')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Ghost')

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 0.2
        expected = 80.0
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, discount), expected)

    def test_calculate_shipping_below_threshold(self):
        subtotal = 50.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 10.0)

    def test_calculate_shipping_above_threshold(self):
        subtotal = 150.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 0.0)

    def test_calculate_shipping_at_threshold(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calculator.calculate_tax(amount), 23.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Expensive', 200.0)
        total = self.calculator.calculate_total()
        expected_tax = 200.0 * 0.23
        expected_total = 200.0 + expected_tax
        self.assertAlmostEqual(total, expected_total)

    def test_total_items_cumulative(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 10, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 20)
        items = self.calculator.list_items()
        self.assertListEqual(sorted(items), ['A', 'B'])

    def test_is_empty_after_manipulation(self):
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.remove_item('A')
        self.assertTrue(self.calculator.is_empty())