import unittest
from typing import Dict, List
from unittest import TestCase
from order_calculator import OrderCalculator


class TestOrderCalculator(TestCase):
    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_init_valid_custom_parameters(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_free_shipping_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_add_item_new_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        self.assertEqual(calculator.total_items(), 1)

    def test_add_item_update_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0, 1)
        calculator.add_item("Book", 20.0, 1)
        self.assertEqual(calculator.total_items(), 2)

    def test_add_item_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("", 20.0)

    def test_add_item_non_string_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 20.0)

    def test_add_item_zero_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Book", 0.0)

    def test_add_item_negative_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Book", -10.0)

    def test_add_item_non_float_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Book", "20.0")

    def test_add_item_zero_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Book", 20.0, 0)

    def test_add_item_negative_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Book", 20.0, -1)

    def test_add_item_non_int_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Book", 20.0, "1")

    def test_add_item_conflicting_price(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        with self.assertRaises(ValueError):
            calculator.add_item("Book", 25.0)

    def test_remove_item_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        calculator.remove_item("Book")
        self.assertTrue(calculator.is_empty())

    def test_remove_item_non_existent_item(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item("Nonexistent")

    def test_remove_item_non_string_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_get_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0, 2)
        self.assertEqual(calculator.get_subtotal(), 40.0)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0, 2)
        calculator.add_item("Pen", 5.0, 3)
        self.assertEqual(calculator.get_subtotal(), 55.0)

    def test_get_subtotal_floating_point_precision(self):
        calculator = OrderCalculator()
        calculator.add_item("Item", 0.1, 3)
        self.assertAlmostEqual(calculator.get_subtotal(), 0.3)

    def test_apply_discount_valid_discount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_full_discount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_negative_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_one(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_non_float_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount("100", 0.1)

    def test_apply_discount_non_float_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount(100.0, "0.1")

    def test_calculate_shipping_free_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_shipping_applied(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calculator.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_shipping(-1.0)

    def test_calculate_shipping_non_float_input(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping("100.0")

    def test_calculate_tax_normal_case(self):
        calculator = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_tax_non_float_input(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax("100.0")

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_with_discount_shipping_tax(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        calculator.add_item("Book", 80.0, 2)
        total = calculator.calculate_total(0.1)
        expected = (144.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_invalid_discount(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        with self.assertRaises(ValueError):
            calculator.calculate_total(1.1)

    def test_calculate_total_non_float_discount(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        with self.assertRaises(TypeError):
            calculator.calculate_total("0.1")

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_total_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0, 3)
        self.assertEqual(calculator.total_items(), 3)

    def test_total_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0, 2)
        calculator.add_item("Pen", 5.0, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_clear_order_non_empty(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_clear_order_empty(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.list_items(), [])

    def test_list_items_multiple_unique_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        calculator.add_item("Pen", 5.0)
        self.assertEqual(set(calculator.list_items()), {"Book", "Pen"})

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 20.0)
        self.assertFalse(calculator.is_empty())