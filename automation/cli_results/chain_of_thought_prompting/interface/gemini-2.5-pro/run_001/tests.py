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

    def test_init_custom_valid_values(self):
        custom_calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(custom_calculator.tax_rate, 0.1)
        self.assertEqual(custom_calculator.free_shipping_threshold, 200.0)
        self.assertEqual(custom_calculator.shipping_cost, 15.0)

    def test_init_invalid_values_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10)

    def test_add_item_new(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertIn('Apple', self.calculator.items)

    def test_add_item_existing_updates_quantity(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.items['Apple']['quantity'], 5)

    def test_add_item_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Banana', -1.0)

    def test_add_item_zero_or_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Banana', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Banana', 1.0, -1)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existing_does_not_raise_error(self):
        self.calculator.add_item('Apple', 1.0)
        try:
            self.calculator.remove_item('Banana')
        except Exception:
            self.fail('remove_item() raised an exception unexpectedly!')
        self.assertEqual(self.calculator.total_items(), 1)

    def test_remove_item_from_empty_order(self):
        try:
            self.calculator.remove_item('Apple')
        except Exception:
            self.fail('remove_item() on empty order raised an exception unexpectedly!')
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 5.5)

    def test_get_subtotal_empty_order_is_zero(self):
        self.assertEqual(self.calculator.get_subtotal(), 0)

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 10), 90)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 0), 100)

    def test_apply_discount_one_hundred_percent(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 100), 0)

    def test_apply_discount_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, -10)

    def test_apply_discount_over_one_hundred_percent_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, 110)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calculator.calculate_shipping(0), 10.0)

    def test_calculate_tax_positive_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100), 23)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0), 0)

    def test_calculate_total_no_discount_paid_shipping(self):
        self.calculator.add_item('Book', 50)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Book', 80)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=10), 100.86)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Laptop', 150)
        self.assertAlmostEqual(self.calculator.calculate_total(), 184.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Laptop', 150)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=10), 166.05)

    def test_calculate_total_empty_order(self):
        self.assertEqual(self.calculator.calculate_total(), 0)

    def test_total_items_sum_of_quantities(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 0.5, 10)
        self.assertEqual(self.calculator.total_items(), 15)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_removes_all_items(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 0.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_on_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_returns_formatted_strings(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.75, 1)
        items_list = self.calculator.list_items()
        self.assertIn('Apple - 2 x $1.50', items_list)
        self.assertIn('Banana - 1 x $0.75', items_list)
        self.assertEqual(len(items_list), 2)

    def test_list_items_empty_order_returns_empty_list(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_with_items_returns_false(self):
        self.calculator.add_item('Apple', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_new_order_returns_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear_returns_true(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())