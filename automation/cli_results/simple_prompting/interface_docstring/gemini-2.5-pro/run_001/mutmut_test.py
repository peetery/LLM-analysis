from order_calculator import OrderCalculator, Item
import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a new OrderCalculator instance before each test."""
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_item_single(self):
        self.calculator.add_item('Laptop', 1500.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Laptop', self.calculator.list_items())

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_updates_quantity(self):
        self.calculator.add_item('Keyboard', 75.0, 1)
        self.calculator.add_item('Keyboard', 75.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 100.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 100.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', 'free')

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Sticker', 0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Sticker', -10)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Pen', 1.0, 1.5)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Pen', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Pen', 1.0, -1)

    def test_add_item_conflicting_price(self):
        self.calculator.add_item('Monitor', 300.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Monitor', 350.0)

    def test_remove_item_existing(self):
        self.calculator.add_item('Webcam', 50.0)
        self.calculator.remove_item('Webcam')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existing(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Microphone')

    def test_remove_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(12345)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Desk', 200.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 200.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Desk', 200.0, 1)
        self.calculator.add_item('Chair', 120.5, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 200.0 + 120.5 * 2)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10, 0.1)

    def test_apply_discount_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(50.0)
        self.assertEqual(cost, self.calculator.shipping_cost)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('ninety')

    def test_calculate_tax_positive_amount(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0 * self.calculator.tax_rate)

    def test_calculate_tax_zero_amount(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('one hundred')

    def test_calculate_total_no_discount_below_shipping(self):
        self.calculator.add_item('A', 50, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount_below_shipping(self):
        self.calculator.add_item('A', 80, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 100.86)

    def test_calculate_total_no_discount_above_shipping(self):
        self.calculator.add_item('A', 120, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 147.6)

    def test_calculate_total_with_discount_above_shipping(self):
        self.calculator.add_item('A', 150, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 147.6)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('A', 10, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        self.calculator.add_item('A', 10, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='zero')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('A', 1, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 1, 5)
        self.calculator.add_item('B', 1, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_clear_order(self):
        self.calculator.add_item('A', 1)
        self.calculator.add_item('B', 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_with_items(self):
        self.calculator.add_item('A', 1)
        self.calculator.add_item('B', 2)
        self.calculator.add_item('A', 1)
        self.assertCountEqual(self.calculator.list_items(), ['A', 'B'])

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('A', 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('A', 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())