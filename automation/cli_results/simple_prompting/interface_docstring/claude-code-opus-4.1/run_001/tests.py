import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()
        self.custom_calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=75.0, shipping_cost=7.5)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 75.0)
        self.assertEqual(calc.shipping_cost, 7.5)

    def test_init_edge_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_over_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Apple')
        self.assertEqual(self.calculator.items[0]['price'], 2.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 1.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Banana', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 2)

    def test_add_item_same_name_same_price_increases_quantity(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price_raises_error(self):
        self.calculator.add_item('Apple', 2.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 3.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.5, 1)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Free', 0.0, 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.5, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.5, -1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 2.5, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '2.5', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 2.5, '1')

    def test_add_item_float_quantity(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 2.5, 1.5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Banana', 1.5, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_non_existing(self):
        self.calculator.add_item('Apple', 2.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_remove_item_last_item(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Banana', 1.5, 3)
        self.calculator.add_item('Orange', 3.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 12.5)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_get_subtotal_large_quantities(self):
        self.calculator.add_item('Item', 0.01, 1000)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_get_subtotal_precision(self):
        self.calculator.add_item('Item1', 0.33, 3)
        self.calculator.add_item('Item2', 0.77, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 2.53, places=2)

    def test_apply_discount_zero_discount(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calculator.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_apply_discount_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_custom_values(self):
        result = self.custom_calculator.calculate_shipping(49.99)
        self.assertEqual(result, 5.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_custom_rate(self):
        result = self.custom_calculator.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_precision(self):
        result = self.calculator.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_calculate_total_no_discount_no_shipping(self):
        self.calculator.add_item('Item', 100.0, 1)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 123.0)

    def test_calculate_total_no_discount_with_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 73.3)

    def test_calculate_total_with_discount_no_shipping(self):
        self.calculator.add_item('Item', 150.0, 1)
        result = self.calculator.calculate_total(0.2)
        self.assertEqual(result, 147.6)

    def test_calculate_total_with_discount_with_shipping(self):
        self.calculator.add_item('Item', 100.0, 1)
        result = self.calculator.calculate_total(0.5)
        self.assertEqual(result, 73.8)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_negative(self):
        self.calculator.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_calculate_total_invalid_discount_over_one(self):
        self.calculator.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.2')

    def test_calculate_total_full_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        result = self.calculator.calculate_total(1.0)
        self.assertEqual(result, 12.3)

    def test_calculate_total_multiple_items(self):
        self.calculator.add_item('Item1', 30.0, 2)
        self.calculator.add_item('Item2', 40.0, 1)
        result = self.calculator.calculate_total(0.1)
        self.assertEqual(result, 116.01)

    def test_total_items_single(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.add_item('Orange', 3.0, 5)
        self.assertEqual(self.calculator.total_items(), 10)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_after_removal(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 2)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_then_add(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.clear_order()
        self.calculator.add_item('Banana', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 2.5, 3)
        result = self.calculator.list_items()
        self.assertEqual(result, ['Apple'])

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.add_item('Orange', 3.0, 1)
        result = self.calculator.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana', 'Orange'})

    def test_list_items_empty(self):
        result = self.calculator.list_items()
        self.assertEqual(result, [])

    def test_list_items_no_duplicates(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Apple', 2.5, 2)
        result = self.calculator.list_items()
        self.assertEqual(result, ['Apple'])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_integration_full_order_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=80.0, shipping_cost=8.0)
        calc.add_item('Laptop', 500.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Keyboard', 75.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 625.0)
        total = calc.calculate_total(0.1)
        self.assertEqual(total, 675.0)
        self.assertEqual(calc.total_items(), 4)
        self.assertIn('Laptop', calc.list_items())
        self.assertFalse(calc.is_empty())

    def test_integration_edge_case_one_cent(self):
        self.calculator.add_item('Penny', 0.01, 1)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 12.3123, places=4)

    def test_integration_large_order(self):
        for i in range(100):
            self.calculator.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(self.calculator.total_items(), 100)
        self.assertEqual(len(self.calculator.list_items()), 100)
        self.assertEqual(self.calculator.get_subtotal(), 100.0)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)