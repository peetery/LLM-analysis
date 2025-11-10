from order_calculator import OrderCalculator, Item

import unittest
from unittest.mock import patch
from typing import List, Dict, Any
from stripped_class.full_order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_custom_valid_parameters(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.05)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_tax_rate_lower_boundary(self):
        calculator_min_tax = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calculator_min_tax.tax_rate, 0.0)

    def test_init_tax_rate_upper_boundary(self):
        calculator_max_tax = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calculator_max_tax.tax_rate, 1.0)

    def test_init_shipping_cost_and_threshold_zero(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calculator.free_shipping_threshold, 0.0)
        self.assertEqual(calculator.shipping_cost, 0.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0.'):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0.'):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaisesRegex(ValueError, 'Free shipping threshold cannot be negative.'):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaisesRegex(ValueError, 'Shipping cost cannot be negative.'):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_incorrect_type_tax_rate(self):
        with self.assertRaisesRegex(TypeError, 'Tax rate must be a float or int.'):
            OrderCalculator(tax_rate='0.23')

    def test_init_incorrect_type_free_shipping_threshold(self):
        with self.assertRaisesRegex(TypeError, 'Free shipping threshold must be a float or int.'):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_incorrect_type_shipping_cost(self):
        with self.assertRaisesRegex(TypeError, 'Shipping cost must be a float or int.'):
            OrderCalculator(shipping_cost='10')

    def test_add_single_item(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Laptop', 'price': 1200.0, 'quantity': 1})

    def test_add_multiple_distinct_items(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(len(self.calculator.items), 2)
        self.assertEqual(self.calculator.items[0]['name'], 'Laptop')
        self.assertEqual(self.calculator.items[1]['name'], 'Mouse')

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Keyboard', 75.0)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_existing_item_increase_quantity(self):
        self.calculator.add_item('Monitor', 300.0, 1)
        self.calculator.add_item('Monitor', 300.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_empty_name(self):
        with self.assertRaisesRegex(ValueError, 'Item name cannot be empty.'):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_price_zero(self):
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0.'):
            self.calculator.add_item('Book', 0.0, 1)

    def test_add_item_price_negative(self):
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0.'):
            self.calculator.add_item('Book', -5.0, 1)

    def test_add_item_quantity_zero(self):
        with self.assertRaisesRegex(ValueError, 'Quantity must be at least 1.'):
            self.calculator.add_item('Pen', 1.0, 0)

    def test_add_item_quantity_negative(self):
        with self.assertRaisesRegex(ValueError, 'Quantity must be at least 1.'):
            self.calculator.add_item('Pen', 1.0, -1)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item('Desk', 150.0, 1)
        with self.assertRaisesRegex(ValueError, 'Item with the same name but different price already exists.'):
            self.calculator.add_item('Desk', 160.0, 1)

    def test_add_item_incorrect_type_name(self):
        with self.assertRaisesRegex(TypeError, 'Item name must be a string.'):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_incorrect_type_price(self):
        with self.assertRaisesRegex(TypeError, 'Price must be a number.'):
            self.calculator.add_item('Chair', '50.0', 1)

    def test_add_item_incorrect_type_quantity(self):
        with self.assertRaisesRegex(TypeError, 'Quantity must be an integer.'):
            self.calculator.add_item('Table', 200.0, 1.5)

    def test_remove_existing_item(self):
        self.calculator.add_item('Shirt', 20.0, 1)
        self.calculator.add_item('Pants', 40.0, 1)
        self.calculator.remove_item('Shirt')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Pants')

    def test_remove_only_item(self):
        self.calculator.add_item('Hat', 15.0, 1)
        self.calculator.remove_item('Hat')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existent_item(self):
        self.calculator.add_item('Socks', 5.0, 1)
        with self.assertRaisesRegex(ValueError, "Item with name 'Gloves' does not exist in the order."):
            self.calculator.remove_item('Gloves')

    def test_remove_item_incorrect_type_name(self):
        self.calculator.add_item('Shoes', 60.0, 1)
        with self.assertRaisesRegex(TypeError, 'Item name must be a string.'):
            self.calculator.remove_item(123)

    def test_get_subtotal_one_item(self):
        self.calculator.add_item('Book', 10.0, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Book', 10.0, 2)
        self.calculator.add_item('Pen', 2.0, 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 30.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order.'):
            self.calculator.get_subtotal()

    def test_apply_discount_standard(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_subtotal_zero(self):
        self.assertAlmostEqual(self.calculator.apply_discount(0.0, 0.1), 0.0)

    def test_apply_discount_invalid_discount_low(self):
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0.'):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_high(self):
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0.'):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaisesRegex(ValueError, 'Cannot apply discount on negative subtotal.'):
            self.calculator.apply_discount(-50.0, 0.1)

    def test_apply_discount_incorrect_type_subtotal(self):
        with self.assertRaisesRegex(TypeError, 'Subtotal must be a number.'):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_incorrect_type_discount(self):
        with self.assertRaisesRegex(TypeError, 'Discount must be a number.'):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_subtotal_zero(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertAlmostEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_incorrect_type_discounted_subtotal(self):
        with self.assertRaisesRegex(TypeError, 'Discounted subtotal must be a number.'):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_positive_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        self.calculator.tax_rate = 0.1
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate tax on negative amount.'):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_incorrect_type_amount(self):
        with self.assertRaisesRegex(TypeError, 'Amount must be a number.'):
            self.calculator.calculate_tax('100')

    @patch.object(OrderCalculator, 'get_subtotal')
    @patch.object(OrderCalculator, 'apply_discount')
    @patch.object(OrderCalculator, 'calculate_shipping')
    @patch.object(OrderCalculator, 'calculate_tax')
    def test_calculate_total_no_discount(self, mock_calculate_tax, mock_calculate_shipping, mock_apply_discount, mock_get_subtotal):
        mock_get_subtotal.return_value = 100.0
        mock_apply_discount.return_value = 100.0
        mock_calculate_shipping.return_value = 10.0
        mock_calculate_tax.return_value = 23.0
        total = self.calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 100.0 + 10.0 + 23.0)
        mock_get_subtotal.assert_called_once()
        mock_apply_discount.assert_called_once_with(100.0, 0.0)
        mock_calculate_shipping.assert_called_once_with(100.0)
        mock_calculate_tax.assert_called_once_with(110.0)

    @patch.object(OrderCalculator, 'get_subtotal')
    @patch.object(OrderCalculator, 'apply_discount')
    @patch.object(OrderCalculator, 'calculate_shipping')
    @patch.object(OrderCalculator, 'calculate_tax')
    def test_calculate_total_with_discount(self, mock_calculate_tax, mock_calculate_shipping, mock_apply_discount, mock_get_subtotal):
        mock_get_subtotal.return_value = 100.0
        mock_apply_discount.return_value = 90.0
        mock_calculate_shipping.return_value = 10.0
        mock_calculate_tax.return_value = 23.0
        total = self.calculator.calculate_total(0.1)
        self.assertAlmostEqual(total, 90.0 + 10.0 + 23.0)
        mock_get_subtotal.assert_called_once()
        mock_apply_discount.assert_called_once_with(100.0, 0.1)
        mock_calculate_shipping.assert_called_once_with(90.0)
        mock_calculate_tax.assert_called_once_with(100.0)

    def test_calculate_total_integration_no_discount_no_free_shipping(self):
        self.calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=5.0)
        self.calculator.add_item('ItemA', 20.0, 2)
        expected_subtotal = 40.0
        expected_discounted_subtotal = 40.0
        expected_shipping = 5.0
        expected_tax_base = expected_discounted_subtotal + expected_shipping
        expected_tax = expected_tax_base * 0.1
        expected_total = expected_discounted_subtotal + expected_shipping + expected_tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_integration_with_discount_and_free_shipping(self):
        self.calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=5.0)
        self.calculator.add_item('ItemA', 60.0, 2)
        expected_subtotal = 120.0
        expected_discounted_subtotal = self.calculator.apply_discount(expected_subtotal, 0.1)
        expected_shipping = 0.0
        expected_tax_base = expected_discounted_subtotal + expected_shipping
        expected_tax = expected_tax_base * 0.1
        expected_total = expected_discounted_subtotal + expected_shipping + expected_tax
        self.assertAlmostEqual(self.calculator.calculate_total(0.1), expected_total)

    @patch.object(OrderCalculator, 'get_subtotal', side_effect=ValueError('Cannot calculate subtotal on empty order.'))
    def test_calculate_total_empty_order_exception(self, mock_get_subtotal):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order.'):
            self.calculator.calculate_total()
        mock_get_subtotal.assert_called_once()

    def test_calculate_total_invalid_discount_type(self):
        with self.assertRaisesRegex(TypeError, 'Discount must be a number.'):
            self.calculator.calculate_total('0.1')

    def test_calculate_total_invalid_discount_value(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0.'):
            self.calculator.calculate_total(1.5)

    def test_total_items_one_item(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Orange', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Item1', 10.0, 1)
        self.calculator.add_item('Item2', 20.0, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.items, [])

    def test_clear_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.items, [])

    def test_list_items_unique_names(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('B', 20.0, 1)
        self.assertCountEqual(self.calculator.list_items(), ['A', 'B'])

    def test_list_items_duplicate_names(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('B', 20.0, 1)
        self.calculator.add_item('A', 10.0, 2)
        self.assertCountEqual(self.calculator.list_items(), ['A', 'B'])

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Test', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_add_and_remove(self):
        self.calculator.add_item('Test', 1.0, 1)
        self.calculator.remove_item('Test')
        self.assertTrue(self.calculator.is_empty())