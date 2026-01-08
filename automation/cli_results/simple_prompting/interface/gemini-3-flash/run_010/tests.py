import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_initial_state_is_empty(self):
        self.assertTrue(self.calc.is_empty())

    def test_initial_total_items_is_zero(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_initial_subtotal_is_zero(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_initial_list_items_is_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_add_item_typical(self):
        self.calc.add_item('Widget', 10.5, 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 21.0)
        self.assertIn('Widget', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Gadget', 15.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 15.0)

    def test_add_multiple_items(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('B', 2.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 5.0)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0')

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -1.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_remove_item_typical(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_non_existent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0, 5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_exceeding_subtotal(self):
        self.assertEqual(self.calc.apply_discount(50.0, 100.0), 0.0)

    def test_apply_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Product', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 71.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(50.0), 184.5)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_custom_shipping_settings(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(55.0), 0.0)

    def test_list_items_returns_correct_names(self):
        names = ['Apple', 'Banana', 'Cherry']
        for name in names:
            self.calc.add_item(name, 1.0)
        result = self.calc.list_items()
        self.assertEqual(sorted(result), sorted(names))