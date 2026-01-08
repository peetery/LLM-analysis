import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.23
        self.free_shipping_threshold = 100.0
        self.shipping_cost = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.free_shipping_threshold, shipping_cost=self.shipping_cost)

    def test_init_default_values(self):
        default_calc = OrderCalculator()
        self.assertEqual(default_calc.get_subtotal(), 0.0)
        self.assertTrue(default_calc.is_empty())

    def test_is_empty_initially(self):
        self.assertTrue(self.calc.is_empty())

    def test_add_item_typical(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Test', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Test', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Test', 10.0, -5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 'ten')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Orange')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_apply_discount_typical(self):
        subtotal = 100.0
        discount = 20.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 80.0)

    def test_apply_discount_excessive(self):
        self.assertEqual(self.calc.apply_discount(50.0, 60.0), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), self.shipping_cost)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(self.free_shipping_threshold), 0.0)

    def test_calculate_tax_standard(self):
        amount = 100.0
        expected_tax = amount * self.tax_rate
        self.assertAlmostEqual(self.calc.calculate_tax(amount), expected_tax)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        subtotal = 50.0
        shipping = self.shipping_cost
        tax = subtotal * self.tax_rate
        expected_total = subtotal + tax + shipping
        self.assertAlmostEqual(self.calc.calculate_total(), expected_total)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('ExpensiveItem', 200.0, 1)
        discount = 50.0
        discounted_subtotal = 150.0
        shipping = 0.0
        tax = discounted_subtotal * self.tax_rate
        expected_total = discounted_subtotal + tax + shipping
        self.assertAlmostEqual(self.calc.calculate_total(discount), expected_total)

    def test_total_items_aggregation(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Pear', 1.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Pear', items)
        self.assertEqual(len(items), 2)