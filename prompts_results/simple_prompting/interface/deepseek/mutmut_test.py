import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_initial_state(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertTrue(self.calculator.is_empty())

    # def test_add_item_valid(self):
    #     self.calculator.add_item("item1", 10.0, 2)
    #     self.assertEqual(self.calculator.total_items(), 1)
    #     self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("item1", -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("item1", 10.0, 0)

    def test_remove_item_existing(self):
        self.calculator.add_item("item1", 10.0)
        self.calculator.remove_item("item1")
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("nonexistent")

    # def test_get_subtotal_empty(self):
    #     self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("item1", 10.0, 2)
        self.calculator.add_item("item2", 5.0)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    # def test_apply_discount_positive(self):
    #     discounted = self.calculator.apply_discount(100.0, 10.0)
    #     self.assertEqual(discounted, 90.0)

    def test_apply_discount_zero(self):
        discounted = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -5.0)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 110.0)

    def test_calculate_shipping_free(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_paid(self):
        shipping = self.calculator.calculate_shipping(99.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_positive(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item("item1", 100.0)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)

    # def test_calculate_total_with_discount(self):
    #     self.calculator.add_item("item1", 100.0)
    #     total = self.calculator.calculate_total(10.0)
    #     self.assertEqual(total, 101.7)

    # def test_total_items_multiple(self):
    #     self.calculator.add_item("item1", 10.0, 2)
    #     self.calculator.add_item("item2", 5.0, 3)
    #     self.assertEqual(self.calculator.total_items(), 2)

    def test_clear_order(self):
        self.calculator.add_item("item1", 10.0)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_multiple(self):
        self.calculator.add_item("item1", 10.0)
        self.calculator.add_item("item2", 20.0)
        items = self.calculator.list_items()
        self.assertIn("item1", items)
        self.assertIn("item2", items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("item1", 10.0)
        self.assertFalse(self.calculator.is_empty())