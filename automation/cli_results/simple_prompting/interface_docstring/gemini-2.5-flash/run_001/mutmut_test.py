from order_calculator import OrderCalculator, Item
import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_at_boundaries(self):
        calc_min = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc_min.tax_rate, 0.0)
        calc_max = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_max.tax_rate, 1.0)

    def test_init_shipping_costs_at_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_invalid_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_new_item(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 1200.0)
        self.assertIn('Laptop', self.calculator.list_items())

    def test_add_item_existing_item_same_price(self):
        self.calculator.add_item('Keyboard', 75.0, 2)
        self.calculator.add_item('Keyboard', 75.0, 1)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 225.0)

    def test_add_item_existing_item_different_price(self):
        self.calculator.add_item('Mouse', 25.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Mouse', 30.0, 1)

    def test_add_item_quantity_default(self):
        self.calculator.add_item('Monitor', 300.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 300.0)

    def test_add_item_large_quantity(self):
        self.calculator.add_item('Pen', 1.0, 1000)
        self.assertEqual(self.calculator.total_items(), 1000)
        self.assertEqual(self.calculator.get_subtotal(), 1000.0)

    def test_add_item_price_with_decimals(self):
        self.calculator.add_item('Book', 15.99, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 15.99)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Free Item', 0.0, 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Negative Item', -5.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item A', 10.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item B', 10.0, -1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item C', '10.00', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item D', 10.0, 1.5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Chair', 50.0, 2)
        self.calculator.remove_item('Chair')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        self.calculator.add_item('Table', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Lamp')

    def test_remove_item_last_item(self):
        self.calculator.add_item('Desk', 200.0, 1)
        self.calculator.remove_item('Desk')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_invalid_name_type(self):
        self.calculator.add_item('Book', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Shirt', 20.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 40.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Pants', 30.0, 1)
        self.calculator.add_item('Socks', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 30.0 + 15.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_zero_subtotal(self):
        self.assertAlmostEqual(self.calculator.apply_discount(0.0, 0.1), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_too_low(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_too_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_valid_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_no_discount_no_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=10.0, shipping_cost=5.0)
        calc.add_item('Item1', 50.0, 1)
        expected_total = 50.0 + 50.0 * 0.23
        self.assertAlmostEqual(calc.calculate_total(), expected_total)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item('Item1', 50.0, 1)
        expected_total = 50.0 + 5.0 + (50.0 + 5.0) * 0.23
        self.assertAlmostEqual(calc.calculate_total(), expected_total)

    def test_calculate_total_with_discount_no_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=10.0, shipping_cost=5.0)
        calc.add_item('Item1', 50.0, 1)
        discounted_subtotal = 50.0 * (1 - 0.1)
        expected_total = discounted_subtotal + discounted_subtotal * 0.23
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), expected_total)

    def test_calculate_total_with_discount_with_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item('Item1', 50.0, 1)
        discounted_subtotal = 50.0 * (1 - 0.1)
        expected_total = discounted_subtotal + 5.0 + (discounted_subtotal + 5.0) * 0.23
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_too_low(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_too_high(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.1)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.add_item('Orange', 0.75, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Grape', 0.2, 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single_item(self):
        self.calculator.add_item('Milk', 3.0, 1)
        self.assertEqual(self.calculator.list_items(), ['Milk'])

    def test_list_items_duplicate_item_names(self):
        self.calculator.add_item('Coffee', 5.0, 1)
        self.calculator.add_item('Coffee', 5.0, 2)
        self.assertEqual(self.calculator.list_items(), ['Coffee'])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Water', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_adding_and_removing(self):
        self.calculator.add_item('Juice', 2.0, 1)
        self.calculator.remove_item('Juice')
        self.assertTrue(self.calculator.is_empty())