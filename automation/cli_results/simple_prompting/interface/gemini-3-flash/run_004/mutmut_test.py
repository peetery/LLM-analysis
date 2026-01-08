import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_custom_values(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        custom_calc.add_item('Test', 60.0)
        self.assertEqual(custom_calc.calculate_shipping(60.0), 0.0)
        self.assertEqual(custom_calc.calculate_tax(100.0), 10.0)

    def test_add_item_typical(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 5.0)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.5)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'free')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -5)

    def test_remove_item_typical(self):
        self.calc.add_item('Apple', 2.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_apply_discount_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 1.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())