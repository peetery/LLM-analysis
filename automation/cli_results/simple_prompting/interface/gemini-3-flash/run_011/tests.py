import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.2
        self.threshold = 100.0
        self.shipping = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.threshold, shipping_cost=self.shipping)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Item A', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Item B', 15.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 15.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, -5)

    def test_remove_item_success(self):
        self.calc.add_item('Target', 10.0, 1)
        self.calc.remove_item('Target')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_apply_discount_typical(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -5.0)

    def test_apply_discount_exceeding_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, 51.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(200.0), 40.0)

    def test_calculate_tax_zero(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 30.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.0), 82.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Expensive', 150.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=30.0), 144.0)

    def test_total_items_aggregation(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_returns_names(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Orange', 1.0, 1)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Apple', items)
        self.assertIn('Orange', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_logic(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('X', 1.0, 1)
        self.assertFalse(self.calc.is_empty())