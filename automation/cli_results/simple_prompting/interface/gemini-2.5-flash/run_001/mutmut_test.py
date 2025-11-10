from order_calculator import OrderCalculator, Item
import unittest
from typing import TypedDict, List, Dict

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.05)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_single_item(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 1200.0)

    def test_add_multiple_items(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 1200.0 + 25.0 * 2)

    def test_add_same_item_updates_quantity(self):
        self.calculator.add_item('Keyboard', 75.0, 1)
        self.calculator.add_item('Keyboard', 75.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 75.0 * 3)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Monitor', 300.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Monitor', 300.0, -1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Monitor', 300.0, 1.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Desk', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Desk', -50.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Desk', 'invalid', 1)

    def test_add_item_invalid_name(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_remove_item_invalid_name(self):
        self.calculator.add_item('Book', 20.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_get_subtotal_one_item(self):
        self.calculator.add_item('Pen', 1.5, 5)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Notebook', 5.0, 2)
        self.calculator.add_item('Eraser', 0.75, 3)
        self.assertEqual(self.calculator.get_subtotal(), 5.0 * 2 + 0.75 * 3)

    def test_apply_zero_discount(self):
        subtotal = 50.0
        discounted = self.calculator.apply_discount(subtotal, 0.0)
        self.assertEqual(discounted, 50.0)

    def test_apply_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -5.0)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_positive_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_with_items_no_discount_below_threshold(self):
        self.calculator.add_item('Shirt', 20.0, 2)
        self.assertAlmostEqual(self.calculator.calculate_total(), 61.5)

    def test_calculate_total_with_items_no_discount_above_threshold(self):
        self.calculator.add_item('TV', 500.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 615.0)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('ItemA', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-5.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('ItemB', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='invalid')

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_one_item(self):
        self.calculator.add_item('Hat', 15.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Socks', 5.0, 3)
        self.calculator.add_item('Gloves', 12.0, 1)
        self.assertEqual(self.calculator.total_items(), 4)

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Orange', 0.75, 1)
        self.assertFalse(self.calculator.is_empty())