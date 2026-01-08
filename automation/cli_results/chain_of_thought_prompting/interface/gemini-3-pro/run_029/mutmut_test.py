import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.get_subtotal(), 1.5)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Banana', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_aggregation(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, 0)

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 2.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false_after_add(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 2.0, 1)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_get_subtotal_normal(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 31.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        expected_subtotal = 200.0
        expected_tax = 200.0 * 0.23
        expected_shipping = 0.0
        expected_total = 200.0 + 46.0 + 0.0
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)