import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_with_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_with_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_with_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_with_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_with_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_with_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_with_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_with_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_invalid_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_basic(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Apple')
        self.assertEqual(self.calculator.items[0]['price'], 1.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 2)

    def test_add_item_with_default_quantity(self):
        self.calculator.add_item('Orange', 2.0)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_multiple_different_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.assertEqual(len(self.calculator.items), 2)

    def test_add_item_same_name_same_price_increases_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_with_unicode_name(self):
        self.calculator.add_item('Äpfel', 1.5, 2)
        self.assertEqual(self.calculator.items[0]['name'], 'Äpfel')

    def test_add_item_with_special_characters(self):
        self.calculator.add_item('Item!@#$%', 1.5, 2)
        self.assertEqual(self.calculator.items[0]['name'], 'Item!@#$%')

    def test_add_item_with_very_small_price(self):
        self.calculator.add_item('Penny', 0.01, 1)
        self.assertEqual(self.calculator.items[0]['price'], 0.01)

    def test_add_item_with_very_large_price(self):
        self.calculator.add_item('Diamond', 1000000.0, 1)
        self.assertEqual(self.calculator.items[0]['price'], 1000000.0)

    def test_add_item_with_very_large_quantity(self):
        self.calculator.add_item('Grain', 0.01, 1000000)
        self.assertEqual(self.calculator.items[0]['quantity'], 1000000)

    def test_add_item_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5, 2)

    def test_add_item_with_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Free', 0.0, 1)

    def test_add_item_with_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Debt', -1.0, 1)

    def test_add_item_with_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Nothing', 1.0, 0)

    def test_add_item_with_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Negative', 1.0, -1)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_add_item_with_non_string_name(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5, 2)

    def test_add_item_with_non_numeric_price(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5', 2)

    def test_add_item_with_non_integer_quantity(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, 2.5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_from_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_remove_item_after_already_removed(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.remove_item('Apple')
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_remove_item_with_non_string_name(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_get_subtotal_after_removing_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.get_subtotal(), 1.5)

    def test_get_subtotal_with_large_quantities(self):
        self.calculator.add_item('Penny', 0.01, 1000000)
        self.assertEqual(self.calculator.get_subtotal(), 10000.0)

    def test_get_subtotal_with_decimal_precision(self):
        self.calculator.add_item('Item1', 0.33, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.99, places=2)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_normal(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_discount(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_on_zero_subtotal(self):
        result = self.calculator.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_fractional_discount(self):
        result = self.calculator.apply_discount(100.0, 0.15)
        self.assertEqual(result, 85.0)

    def test_apply_discount_with_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.2)

    def test_apply_discount_with_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_with_discount_above_one(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_with_non_numeric_subtotal(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_apply_discount_with_non_numeric_discount(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calculator.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_zero_subtotal(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_with_non_numeric_input(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_normal(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_with_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_with_decimal_precision(self):
        result = self.calculator.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=3)

    def test_calculate_tax_with_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_with_non_numeric_input(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_without_discount(self):
        self.calculator.add_item('Apple', 50.0, 2)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 123.0)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Apple', 60.0, 2)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 147.6)

    def test_calculate_total_zero_discount(self):
        self.calculator.add_item('Apple', 50.0, 2)
        result = self.calculator.calculate_total(0.0)
        self.assertEqual(result, 123.0)

    def test_calculate_total_full_discount(self):
        self.calculator.add_item('Apple', 50.0, 2)
        result = self.calculator.calculate_total(1.0)
        self.assertEqual(result, 12.3)

    def test_calculate_total_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Apple', 40.0, 2)
        result = calc.calculate_total()
        self.assertEqual(result, 98.4)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_with_negative_discount(self):
        self.calculator.add_item('Apple', 50.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_calculate_total_with_discount_above_one(self):
        self.calculator.add_item('Apple', 50.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)

    def test_calculate_total_with_non_numeric_discount(self):
        self.calculator.add_item('Apple', 50.0, 2)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.2')

    def test_total_items_single_item(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_total_items_after_removing_item(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Banana', 0.5, 5)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Banana', 0.5, 5)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_empty_order(self):
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_then_add_new_items(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.clear_order()
        self.calculator.add_item('Orange', 2.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Orange')

    def test_list_items_single_item(self):
        self.calculator.add_item('Apple', 1.5, 3)
        result = self.calculator.list_items()
        self.assertEqual(result, ['Apple'])

    def test_list_items_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Banana', 0.5, 5)
        result = self.calculator.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_list_items_empty_order(self):
        result = self.calculator.list_items()
        self.assertEqual(result, [])

    def test_list_items_after_clear(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.clear_order()
        result = self.calculator.list_items()
        self.assertEqual(result, [])

    def test_list_items_no_duplicates(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Apple', 1.5, 2)
        result = self.calculator.list_items()
        self.assertEqual(result, ['Apple'])

    def test_is_empty_when_empty(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_when_not_empty(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_integration_add_items_calculate_total(self):
        self.calculator.add_item('Apple', 30.0, 2)
        self.calculator.add_item('Banana', 20.0, 2)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)

    def test_integration_quantity_accumulation(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.calculator.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)

    def test_integration_free_shipping_edge_case_just_below(self):
        self.calculator.add_item('Item', 99.99, 1)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 135.2877, places=3)

    def test_integration_free_shipping_edge_case_exactly_at(self):
        self.calculator.add_item('Item', 100.0, 1)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)

    def test_integration_free_shipping_edge_case_just_above(self):
        self.calculator.add_item('Item', 100.01, 1)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 123.0123, places=3)

    def test_integration_clear_and_rebuild_order(self):
        self.calculator.add_item('Apple', 30.0, 2)
        self.calculator.clear_order()
        self.calculator.add_item('Banana', 50.0, 2)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)