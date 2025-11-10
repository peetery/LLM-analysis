from order_calculator import OrderCalculator, Item

import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_with_default_parameters(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200, shipping_cost=15)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200)
        self.assertEqual(calc.shipping_cost, 15)

    def test_init_with_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_raises_value_error_for_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_raises_value_error_for_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_raises_value_error_for_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_raises_type_error_for_non_numeric_parameters(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_item_new(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 2})

    def test_add_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 5)
        self.assertEqual(len(self.calculator.items), 2)

    def test_add_item_existing_updates_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_raises_value_error_for_same_name_different_price(self):
        self.calculator.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_add_item_raises_value_error_for_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)

    def test_add_item_raises_value_error_for_non_positive_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -10)

    def test_add_item_raises_value_error_for_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -1)

    def test_add_item_raises_type_error_for_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 'invalid')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, 'invalid')

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_raises_value_error_for_non_existing_item(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_raises_type_error_for_non_string_name(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calculator.get_subtotal(), 5.5)

    def test_get_subtotal_raises_value_error_on_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100, 0.2), 80.0)

    def test_apply_discount_zero_percent(self):
        self.assertEqual(self.calculator.apply_discount(100, 0.0), 100.0)

    def test_apply_discount_one_hundred_percent(self):
        self.assertEqual(self.calculator.apply_discount(100, 1.0), 0.0)

    def test_apply_discount_raises_value_error_for_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100, 1.1)

    def test_apply_discount_raises_value_error_for_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100, 0.2)

    def test_apply_discount_raises_type_error_for_non_numeric(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100, '0.2')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100), 0.0)

    def test_calculate_shipping_raises_type_error_for_non_numeric(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('invalid')

    def test_calculate_tax_on_positive_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100), 23.0)

    def test_calculate_tax_on_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0), 0.0)

    def test_calculate_tax_raises_value_error_for_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100)

    def test_calculate_tax_raises_type_error_for_non_numeric(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('invalid')

    def test_calculate_total_no_discount_with_shipping(self):
        self.calculator.add_item('Book', 50, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount_and_shipping(self):
        self.calculator.add_item('Book', 80, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 100.86)

    def test_calculate_total_no_discount_free_shipping(self):
        self.calculator.add_item('Laptop', 150, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 184.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Laptop', 120, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 132.84)

    def test_calculate_total_with_one_hundred_percent_discount(self):
        self.calculator.add_item('Book', 50, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=1.0), 12.3)

    def test_calculate_total_raises_value_error_on_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_raises_value_error_for_invalid_discount(self):
        self.calculator.add_item('Book', 50, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.1)

    def test_calculate_total_raises_type_error_for_non_numeric_discount(self):
        self.calculator.add_item('Book', 50, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='invalid')

    def test_total_items_returns_sum_of_quantities(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_total_items_returns_zero_for_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_empties_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_returns_unique_names(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 5)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertCountEqual(self.calculator.list_items(), ['Apple', 'Banana'])

    def test_list_items_returns_empty_list_for_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_returns_true_for_new_order_and_false_otherwise(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertFalse(self.calculator.is_empty())