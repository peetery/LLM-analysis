from order_calculator import OrderCalculator, Item
import unittest
from typing import List, TypedDict

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_free_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_single_item(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Laptop', 'price': 1200.0, 'quantity': 1})

    def test_add_multiple_items(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(len(self.calculator.items), 2)
        self.assertEqual(self.calculator.items[1], {'name': 'Mouse', 'price': 25.0, 'quantity': 2})

    def test_add_existing_item_increases_quantity(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.calculator.add_item('Laptop', 1200.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_same_name_different_price_raises_error(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Laptop', 1300.0, 1)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 0.0, 1)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', -5.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', '10.0', 1)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Pen', 1.0, 0)

    def test_add_item_invalid_quantity_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Pen', 1.0, -1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Pen', 1.0, 1.5)

    def test_remove_existing_item(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.calculator.remove_item('Laptop')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Mouse')

    def test_remove_non_existent_item_raises_error(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Keyboard')

    def test_remove_item_from_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Book')

    def test_remove_item_invalid_name_type(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Book', 15.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Book', 15.0, 2)
        self.calculator.add_item('Pen', 2.5, 4)
        self.assertEqual(self.calculator.get_subtotal(), 30.0 + 10.0)

    def test_get_subtotal_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_valid_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_zero_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_full_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_out_of_range_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_discount_out_of_range_low(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_free_shipping(self):
        self.calculator.free_shipping_threshold = 100.0
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_paid_shipping(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_invalid_discounted_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_positive_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_no_discount_no_shipping(self):
        self.calculator.add_item('Item A', 50.0, 1)
        self.calculator.add_item('Item B', 60.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 135.3)

    def test_calculate_total_with_discount_no_shipping(self):
        self.calculator.add_item('Item A', 50.0, 1)
        self.calculator.add_item('Item B', 60.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 134.07)

    def test_calculate_total_with_discount_with_shipping(self):
        self.calculator.add_item('Item A', 40.0, 1)
        self.calculator.add_item('Item B', 30.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 89.79)

    def test_calculate_total_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_calculate_total_invalid_discount_value(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-0.1)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('Book', 15.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Book', 15.0, 2)
        self.calculator.add_item('Pen', 2.5, 4)
        self.assertEqual(self.calculator.total_items(), 6)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Book', 15.0, 2)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order_empty_order(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_unique_names(self):
        self.calculator.add_item('Book', 15.0, 1)
        self.calculator.add_item('Pen', 2.5, 1)
        self.assertCountEqual(self.calculator.list_items(), ['Book', 'Pen'])

    def test_list_items_duplicate_names(self):
        self.calculator.add_item('Book', 15.0, 1)
        self.calculator.add_item('Book', 15.0, 2)
        self.calculator.add_item('Pen', 2.5, 1)
        self.assertCountEqual(self.calculator.list_items(), ['Book', 'Pen'])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Book', 15.0, 1)
        self.assertFalse(self.calculator.is_empty())