from order_calculator import OrderCalculator, Item

import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertTrue(calculator.is_empty())

    def test_init_custom_valid_parameters(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.05)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_init_type_error_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_item_single_new_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        self.assertEqual(calculator._items, [{'name': 'Laptop', 'price': 1200.0, 'quantity': 1}])

    def test_add_item_multiple_different_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(calculator._items, [{'name': 'Laptop', 'price': 1200.0, 'quantity': 1}, {'name': 'Mouse', 'price': 25.0, 'quantity': 2}])

    def test_add_item_existing_item_increases_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0, 1)
        calculator.add_item('Laptop', 1200.0, 2)
        self.assertEqual(calculator._items, [{'name': 'Laptop', 'price': 1200.0, 'quantity': 3}])

    def test_add_item_with_custom_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Keyboard', 75.0, 5)
        self.assertEqual(calculator._items, [{'name': 'Keyboard', 'price': 75.0, 'quantity': 5}])

    def test_add_item_empty_name_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 10.0)

    def test_add_item_zero_price_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Book', 0.0)

    def test_add_item_negative_price_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Book', -5.0)

    def test_add_item_quantity_less_than_one_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Pen', 1.0, 0)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calculator = OrderCalculator()
        calculator.add_item('Monitor', 200.0)
        with self.assertRaises(ValueError):
            calculator.add_item('Monitor', 250.0)

    def test_add_item_type_error_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Book', 'invalid')

    def test_add_item_type_error_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Pen', 1.0, 1.5)

    def test_remove_item_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.add_item('Mouse', 25.0)
        calculator.remove_item('Laptop')
        self.assertEqual(calculator._items, [{'name': 'Mouse', 'price': 25.0, 'quantity': 1}])

    def test_remove_item_last_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.remove_item('Laptop')
        self.assertTrue(calculator.is_empty())

    def test_remove_item_non_existent_item_raises_value_error(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        with self.assertRaises(ValueError):
            calculator.remove_item('Keyboard')

    def test_remove_item_type_error_name(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(calculator.get_subtotal(), 1200.0 + 25.0 * 2)

    def test_get_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0, 3)
        self.assertEqual(calculator.get_subtotal(), 1200.0 * 3)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_valid_discount(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_maximum_discount(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_below_zero_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_above_one_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount('invalid', 0.1)

    def test_apply_discount_type_error_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount(100.0, 'invalid')

    def test_calculate_shipping_qualifies_for_free_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(120.0), 0.0)

    def test_calculate_shipping_does_not_qualify_for_free_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(80.0), 10.0)

    def test_calculate_shipping_at_free_shipping_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error_discounted_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping('invalid')

    def test_calculate_shipping_negative_discounted_subtotal_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax('invalid')

    def test_calculate_total_no_discount_no_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item A', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 66.0)

    def test_calculate_total_with_discount_no_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item A', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(discount=0.1), 60.5)

    def test_calculate_total_no_discount_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item A', 60.0, 2)
        self.assertAlmostEqual(calculator.calculate_total(), 132.0)

    def test_calculate_total_with_discount_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item A', 60.0, 2)
        self.assertAlmostEqual(calculator.calculate_total(discount=0.1), 118.8)

    def test_calculate_total_zero_discount(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item A', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(discount=0.0), 66.0)

    def test_calculate_total_empty_order_raises_value_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calculator = OrderCalculator()
        calculator.add_item('Item A', 10.0)
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=1.1)
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=-0.1)

    def test_calculate_total_type_error_discount(self):
        calculator = OrderCalculator()
        calculator.add_item('Item A', 10.0)
        with self.assertRaises(TypeError):
            calculator.calculate_total(discount='invalid')

    def test_total_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1)
        calculator.add_item('Mouse', 2)
        self.assertEqual(calculator.total_items(), 3)

    def test_total_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Keyboard', 5)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_clear_order_already_empty(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_list_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.add_item('Mouse', 25.0)
        calculator.add_item('Keyboard', 75.0)
        self.assertListEqual(sorted(calculator.list_items()), ['Keyboard', 'Laptop', 'Mouse'])

    def test_list_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        self.assertListEqual(calculator.list_items(), ['Laptop'])

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertListEqual(calculator.list_items(), [])

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        self.assertFalse(calculator.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        calculator.remove_item('Laptop')
        self.assertTrue(calculator.is_empty())