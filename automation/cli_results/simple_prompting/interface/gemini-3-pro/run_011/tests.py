import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_multiple(self):
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 7.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 5.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_clear_order(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.calc.add_item('A', 10.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount(self):
        subtotal = 100.0
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 0.1), 90.0)
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        self.assertTrue(total > 50.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive', 200.0)
        total = self.calc.calculate_total()
        self.assertGreater(total, 200.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertTrue(total > 0)

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 20.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 3)
        self.calc.add_item('B', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 5)