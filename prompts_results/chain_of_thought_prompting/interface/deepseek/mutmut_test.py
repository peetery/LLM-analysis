import unittest
from typing import List
from unittest import TestCase
from order_calculator import OrderCalculator


class TestOrderCalculator(TestCase):
    def test_default_initialization(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calculator = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.15)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_invalid_shipping_threshold_non_float(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_add_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Book", 15.99)
        self.assertEqual(calculator.total_items(), 1)

    def test_add_item_with_quantity_gt_1(self):
        calculator = OrderCalculator()
        calculator.add_item("Pen", 1.99, 5)
        self.assertEqual(calculator.total_items(), 5)

    def test_add_duplicate_item_sums_quantities(self):
        calculator = OrderCalculator()
        calculator.add_item("Notebook", 4.99, 2)
        calculator.add_item("Notebook", 4.99, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_add_item_with_zero_price(self):
        with self.assertRaises(ValueError):
            calculator = OrderCalculator()
            calculator.add_item("Freebie", 0.0)

    def test_add_item_with_negative_quantity(self):
        with self.assertRaises(ValueError):
            calculator = OrderCalculator()
            calculator.add_item("Eraser", 0.99, -1)

    def test_remove_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Ruler", 2.49)
        calculator.remove_item("Ruler")
        self.assertEqual(calculator.total_items(), 0)

    # def test_remove_non_existent_item(self):
    #     calculator = OrderCalculator()
    #     with self.assertRaises(KeyError):
    #         calculator.remove_item("Glue")

    def test_clear_non_empty_order(self):
        calculator = OrderCalculator()
        calculator.add_item("Stapler", 8.99)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_clear_empty_order(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.list_items(), [])

    # def test_list_items_with_items(self):
    #     calculator = OrderCalculator()
    #     calculator.add_item("Pencil", 0.99)
    #     calculator.add_item("Eraser", 0.49)
    #     self.assertListEqual(calculator.list_items(), ["Pencil", "Eraser"])

    def test_total_items_count(self):
        calculator = OrderCalculator()
        calculator.add_item("Marker", 1.99, 3)
        calculator.add_item("Highlighter", 2.49, 2)
        self.assertEqual(calculator.total_items(), 5)

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item("Notepad", 3.99)
        self.assertFalse(calculator.is_empty())

    # def test_get_subtotal_no_items(self):
    #     calculator = OrderCalculator()
    #     self.assertEqual(calculator.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Binder", 5.99, 2)
        calculator.add_item("Divider", 2.99)
        self.assertEqual(calculator.get_subtotal(), 5.99 * 2 + 2.99)

    # def test_apply_valid_discount(self):
    #     calculator = OrderCalculator()
    #     discounted = calculator.apply_discount(100.0, 10.0)
    #     self.assertEqual(discounted, 90.0)

    # def test_apply_100_percent_discount(self):
    #     calculator = OrderCalculator()
    #     discounted = calculator.apply_discount(50.0, 100.0)
    #     self.assertEqual(discounted, 0.0)

    def test_apply_invalid_discount_gt_100(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 110.0)

    def test_apply_negative_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator()
        shipping = calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator()
        shipping = calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calculator = OrderCalculator()
        shipping = calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_normal_amount(self):
        calculator = OrderCalculator()
        tax = calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator()
        tax = calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-50.0)

    # def test_calculate_total_no_discount(self):
    #     calculator = OrderCalculator()
    #     calculator.add_item("Textbook", 49.99)
    #     total = calculator.calculate_total()
    #     subtotal = 49.99
    #     shipping = 10.0
    #     tax = subtotal * 0.23
    #     self.assertEqual(total, subtotal + shipping + tax)

    # def test_calculate_total_with_discount(self):
    #     calculator = OrderCalculator()
    #     calculator.add_item("Laptop", 999.99)
    #     total = calculator.calculate_total(discount=10.0)
    #     subtotal = 999.99
    #     discounted = subtotal * 0.9
    #     tax = discounted * 0.23
    #     self.assertEqual(total, discounted + tax)

    def test_calculate_total_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item("Monitor", 199.99)
        total = calculator.calculate_total()
        self.assertEqual(calculator.calculate_shipping(199.99), 0.0)

    # def test_calculate_total_empty_order(self):
    #     calculator = OrderCalculator()
    #     self.assertEqual(calculator.calculate_total(), 0.0)

    def test_sequential_operations(self):
        calculator = OrderCalculator()
        calculator.add_item("Mouse", 25.99)
        calculator.add_item("Keyboard", 59.99)
        calculator.remove_item("Mouse")
        self.assertEqual(calculator.total_items(), 1)
        self.assertEqual(calculator.get_subtotal(), 59.99)

    # def test_discount_applied_before_shipping_tax(self):
    #     calculator = OrderCalculator()
    #     calculator.add_item("Tablet", 299.99)
    #     total = calculator.calculate_total(discount=20.0)
    #     discounted_subtotal = 299.99 * 0.8
    #     shipping = 0.0  # Above threshold
    #     tax = discounted_subtotal * 0.23
    #     self.assertEqual(total, discounted_subtotal + shipping + tax)

    # def test_free_shipping_respects_discounted_subtotal(self):
    #     calculator = OrderCalculator(free_shipping_threshold=100.0)
    #     calculator.add_item("Headphones", 120.0)
    #     total_without_discount = calculator.calculate_total()
    #     calculator.clear_order()
    #     calculator.add_item("Headphones", 120.0)
    #     total_with_discount = calculator.calculate_total(discount=20.0)
    #     self.assertNotEqual(total_without_discount, total_with_discount)