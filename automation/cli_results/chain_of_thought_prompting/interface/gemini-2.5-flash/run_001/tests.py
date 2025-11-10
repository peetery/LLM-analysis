from order_calculator import OrderCalculator, Item

import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertTrue(calculator.is_empty())

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_negative_tax_rate_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item_default_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1200.0)
        self.assertEqual(calculator.get_subtotal(), 1200.0)
        self.assertEqual(calculator.total_items(), 1)
        self.assertFalse(calculator.is_empty())
        self.assertIn('Laptop', calculator.list_items())

    def test_add_multiple_items_specified_quantities(self):
        calculator = OrderCalculator()
        calculator.add_item('Keyboard', 75.0, 2)
        calculator.add_item('Mouse', 25.0, 3)
        self.assertEqual(calculator.get_subtotal(), 75.0 * 2 + 25.0 * 3)
        self.assertEqual(calculator.total_items(), 5)
        self.assertListEqual(sorted(calculator.list_items()), sorted(['Keyboard', 'Mouse']))

    def test_add_existing_item_updates_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Monitor', 300.0, 1)
        calculator.add_item('Monitor', 300.0, 2)
        self.assertEqual(calculator.get_subtotal(), 300.0 * 3)
        self.assertEqual(calculator.total_items(), 3)
        self.assertListEqual(calculator.list_items(), ['Monitor'])

    def test_add_item_quantity_zero_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Pen', 1.0, 0)
        self.assertTrue(calculator.is_empty())

    def test_add_item_negative_price_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Book', -10.0)
        self.assertTrue(calculator.is_empty())

    def test_add_item_negative_quantity_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Pencil', 0.5, -2)
        self.assertTrue(calculator.is_empty())

    def test_add_item_empty_name_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 5.0)
        self.assertTrue(calculator.is_empty())

    def test_remove_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Chair', 150.0)
        calculator.add_item('Desk', 200.0)
        calculator.remove_item('Chair')
        self.assertEqual(calculator.get_subtotal(), 200.0)
        self.assertEqual(calculator.total_items(), 1)
        self.assertListEqual(calculator.list_items(), ['Desk'])

    def test_remove_non_existent_item_no_error(self):
        calculator = OrderCalculator()
        calculator.add_item('Table', 100.0)
        calculator.remove_item('NonExistentItem')
        self.assertEqual(calculator.get_subtotal(), 100.0)
        self.assertEqual(calculator.total_items(), 1)
        self.assertListEqual(calculator.list_items(), ['Table'])

    def test_remove_last_remaining_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Lamp', 30.0)
        calculator.remove_item('Lamp')
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.get_subtotal(), 0.0)
        self.assertEqual(calculator.total_items(), 0)

    def test_remove_item_empty_name_raises_error(self):
        calculator = OrderCalculator()
        calculator.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            calculator.remove_item('')
        self.assertFalse(calculator.is_empty())

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Shirt', 25.0, 2)
        self.assertEqual(calculator.get_subtotal(), 50.0)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Pants', 40.0, 1)
        calculator.add_item('Socks', 5.0, 4)
        self.assertEqual(calculator.get_subtotal(), 40.0 + 20.0)

    def test_get_subtotal_after_add_and_remove(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0, 2)
        calculator.add_item('B', 20.0, 1)
        calculator.remove_item('A')
        self.assertEqual(calculator.get_subtotal(), 20.0)

    def test_apply_valid_percentage_discount(self):
        calculator = OrderCalculator()
        discounted_amount = calculator.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(discounted_amount, 90.0)

    def test_apply_zero_discount(self):
        calculator = OrderCalculator()
        discounted_amount = calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(discounted_amount, 100.0)

    def test_apply_discount_results_in_zero_if_too_high(self):
        calculator = OrderCalculator()
        discounted_amount = calculator.apply_discount(10.0, 1.5)
        self.assertAlmostEqual(discounted_amount, 0.0)

    def test_apply_negative_discount_percentage_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-50.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calculator.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_subtotal_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        calculator = OrderCalculator(tax_rate=0.1)
        tax = calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 10.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator(tax_rate=0.1)
        tax = calculator.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative_amount_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.calculate_total(), 0.0)

    def test_calculate_total_items_no_discount(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 66.0)

    def test_calculate_total_items_with_valid_discount(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item1', 50.0, 1)
        calculator.add_item('Item2', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(discount=0.1), 99.0)

    def test_calculate_total_free_shipping_due_to_subtotal(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Expensive Item', 120.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 132.0)

    def test_calculate_total_negative_discount_percentage_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=-0.1)

    def test_calculate_total_discount_greater_than_one_raises_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=1.1)

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_total_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Widget', 10.0, 1)
        self.assertEqual(calculator.total_items(), 1)

    def test_total_items_multiple_items_and_quantities(self):
        calculator = OrderCalculator()
        calculator.add_item('Gadget', 20.0, 3)
        calculator.add_item('Doodad', 5.0, 2)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_after_add_and_remove(self):
        calculator = OrderCalculator()
        calculator.add_item('PartA', 1.0, 5)
        calculator.add_item('PartB', 2.0, 3)
        calculator.remove_item('PartA')
        self.assertEqual(calculator.total_items(), 3)

    def test_clear_order_with_items(self):
        calculator = OrderCalculator()
        calculator.add_item('ItemX', 10.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.get_subtotal(), 0.0)
        self.assertEqual(calculator.total_items(), 0)
        self.assertListEqual(calculator.list_items(), [])

    def test_clear_already_empty_order(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.get_subtotal(), 0.0)

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertListEqual(calculator.list_items(), [])

    def test_list_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.0)
        self.assertListEqual(calculator.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Banana', 0.5, 2)
        calculator.add_item('Orange', 0.75)
        self.assertListEqual(sorted(calculator.list_items()), sorted(['Banana', 'Orange']))

    def test_is_empty_initially_empty(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_not_empty_after_adding_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Grape', 0.2)
        self.assertFalse(calculator.is_empty())

    def test_is_empty_becomes_empty_after_removing_all_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Pear', 1.5)
        calculator.remove_item('Pear')
        self.assertTrue(calculator.is_empty())

    def test_is_empty_after_clear_order(self):
        calculator = OrderCalculator()
        calculator.add_item('Kiwi', 2.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())