import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertIsInstance(calc, OrderCalculator)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertIsInstance(calc, OrderCalculator)

    def test_add_item_single(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple_different(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -10.0, 1)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_calculated(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_apply_discount_standard(self):
        subtotal = 100.0
        discount = 20.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 80.0)

    def test_apply_discount_exceeds_subtotal(self):
        subtotal = 50.0
        discount = 60.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calc.calculate_tax(amount), 23.0)

    def test_calculate_total_integration(self):
        self.calc.add_item('Item1', 50.0, 2)
        total = self.calc.calculate_total(discount=20.0)
        self.assertGreater(total, 80.0)
        self.assertIsInstance(total, float)

    def test_calculate_total_default_discount(self):
        self.calc.add_item('Item1', 10.0, 1)
        total = self.calc.calculate_total()
        self.assertGreater(total, 10.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        total = self.calc.calculate_total()
        self.assertGreater(total, 200.0)

    def test_total_items(self):
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 10, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)