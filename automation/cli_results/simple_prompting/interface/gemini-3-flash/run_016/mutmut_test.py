import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_init_defaults(self):
        default_calc = OrderCalculator()
        self.assertEqual(default_calc.calculate_tax(100), 23.0)
        self.assertEqual(default_calc.calculate_shipping(99.9), 10.0)
        self.assertEqual(default_calc.calculate_shipping(100.0), 0.0)

    def test_init_custom(self):
        self.assertEqual(self.calc.calculate_tax(100), 20.0)
        self.assertEqual(self.calc.calculate_shipping(90), 15.0)

    def test_is_empty_initially(self):
        self.assertTrue(self.calc.is_empty())

    def test_add_item_updates_state(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_multiple_items(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.calc.add_item('Keyboard', 50.0, 1)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 100.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises((TypeError, ValueError)):
            self.calc.add_item('Item', 'price')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, -1)

    def test_remove_item_success(self):
        self.calc.add_item('Item A', 10.0)
        self.calc.remove_item('Item A')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        self.calc.add_item('Item A', 10.0)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Non-existent')

    def test_get_subtotal(self):
        self.calc.add_item('A', 10.5, 2)
        self.calc.add_item('B', 20.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 41.0)

    def test_apply_discount_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 15.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(self.calc.calculate_tax(200.0), 40.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Monitor', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 240.0)

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)