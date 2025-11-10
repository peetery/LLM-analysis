from order_calculator import OrderCalculator, Item

import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200, shipping_cost=15)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200)
        self.assertEqual(calc.shipping_cost, 15)

    def test_init_edge_cases(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)
        calc_one = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_one.tax_rate, 1.0)

    def test_init_invalid_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_invalid_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1)

    def test_init_invalid_types_raise_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='abc')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='abc')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='abc')

    def test_add_item_single(self):
        self.calculator.add_item('Laptop', 1500.0, 1)
        self.assertIn('Laptop', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_unique(self):
        self.calculator.add_item('Laptop', 1500.0, 1)
        self.calculator.add_item('Mouse', 50.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertIn('Laptop', self.calculator.list_items())
        self.assertIn('Mouse', self.calculator.list_items())

    def test_add_item_updates_quantity(self):
        self.calculator.add_item('Laptop', 1500.0, 1)
        self.calculator.add_item('Laptop', 1500.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_add_item_invalid_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', -10.0)

    def test_add_item_invalid_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 10.0, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calculator.add_item('Book', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 12.0)

    def test_add_item_invalid_types_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', '10.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', 10.0, '1')

    def test_remove_item_existing(self):
        self.calculator.add_item('Book', 10.0)
        self.calculator.remove_item('Book')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Book')

    def test_remove_item_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_with_items(self):
        self.calculator.add_item('Book', 10.0, 2)
        self.calculator.add_item('Pen', 1.5, 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 27.5)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_normal_case(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 0.2), 80)

    def test_apply_discount_edge_cases(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 0.0), 100)
        self.assertAlmostEqual(self.calculator.apply_discount(100, 1.0), 0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100, 0.1)

    def test_apply_discount_invalid_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, 1.1)

    def test_apply_discount_invalid_types_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100), 0.0)

    def test_calculate_shipping_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100), 23)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0), 0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100)

    def test_calculate_tax_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_paid_shipping_no_discount(self):
        self.calculator.add_item('Item A', 50, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_paid_shipping_with_discount(self):
        self.calculator.add_item('Item A', 80, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 91.02)

    def test_calculate_total_free_shipping_no_discount(self):
        self.calculator.add_item('Item B', 120, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 147.6)

    def test_calculate_total_free_shipping_with_discount(self):
        self.calculator.add_item('Item C', 200, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 221.4)

    def test_calculate_total_discount_drops_below_free_shipping(self):
        self.calculator.add_item('Item D', 120, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 130.38)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        self.calculator.add_item('Item', 10)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.1)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_with_items(self):
        self.calculator.add_item('Item A', 10, 2)
        self.calculator.add_item('Item B', 20, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_populated(self):
        self.calculator.add_item('Item A', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_with_items(self):
        self.calculator.add_item('Item A', 10)
        self.calculator.add_item('Item B', 20)
        self.assertCountEqual(self.calculator.list_items(), ['Item A', 'Item B'])

    def test_is_empty_on_new_order(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item('Item', 10)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clearing_order(self):
        self.calculator.add_item('Item', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())