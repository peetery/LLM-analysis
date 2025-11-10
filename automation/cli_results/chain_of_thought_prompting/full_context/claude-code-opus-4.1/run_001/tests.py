import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_with_custom_parameters(self):
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

    def test_init_with_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_with_negative_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_string_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_string_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_string_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_item(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Apple')
        self.assertEqual(self.calculator.items[0]['price'], 2.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_multiple_different_items(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 2)

    def test_add_item_with_default_quantity(self):
        self.calculator.add_item('Orange', 3.0)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_same_name_same_price_updates_quantity(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Apple', 2.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_with_float_price(self):
        self.calculator.add_item('Item', 19.99, 1)
        self.assertEqual(self.calculator.items[0]['price'], 19.99)

    def test_add_item_with_integer_price(self):
        self.calculator.add_item('Item', 20, 1)
        self.assertEqual(self.calculator.items[0]['price'], 20)

    def test_add_item_with_very_large_quantity(self):
        self.calculator.add_item('Bulk', 0.01, 1000000)
        self.assertEqual(self.calculator.items[0]['quantity'], 1000000)

    def test_add_item_with_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_with_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 0, 1)

    def test_add_item_with_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -5.0, 1)

    def test_add_item_with_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, 0)

    def test_add_item_with_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calculator.add_item('Apple', 2.5, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 3.0, 1)

    def test_add_item_with_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_with_string_price_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', '10.0', 1)

    def test_add_item_with_float_quantity_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 10.0, 1.5)

    def test_remove_item_single_item(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_from_multiple_items(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_all_items_sequentially(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.calculator.remove_item('Banana')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_non_existent_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Item')

    def test_remove_item_with_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 2.5, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 10.5)

    def test_get_subtotal_with_large_quantities(self):
        self.calculator.add_item('Item', 0.01, 10000)
        self.assertEqual(self.calculator.get_subtotal(), 100.0)

    def test_get_subtotal_with_fractional_prices(self):
        self.calculator.add_item('Item1', 1.11, 1)
        self.calculator.add_item('Item2', 2.22, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.33, places=2)

    def test_get_subtotal_on_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_with_zero_discount(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_with_ten_percent(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_with_fifty_percent(self):
        result = self.calculator.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_with_hundred_percent(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_on_zero_subtotal(self):
        result = self.calculator.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_fractional_amounts(self):
        result = self.calculator.apply_discount(33.33, 0.15)
        self.assertAlmostEqual(result, 28.3305, places=4)

    def test_apply_discount_with_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_with_discount_over_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_on_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-50.0, 0.1)

    def test_apply_discount_with_string_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_with_string_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_with_zero_amount(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calculator.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_with_string_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_on_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_on_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_calculate_tax_with_fractional_amount(self):
        result = self.calculator.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_calculate_tax_on_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-50.0)

    def test_calculate_tax_with_string_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_without_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        result = self.calculator.calculate_total(0.0)
        self.assertEqual(result, 123.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        result = self.calculator.calculate_total(0.1)
        self.assertAlmostEqual(result, 122.07, places=2)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Item', 150.0, 1)
        result = self.calculator.calculate_total(0.0)
        self.assertEqual(result, 184.5)

    def test_calculate_total_with_paid_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        result = self.calculator.calculate_total(0.0)
        self.assertEqual(result, 73.8)

    def test_calculate_total_multiple_items_with_discount(self):
        self.calculator.add_item('Item1', 30.0, 2)
        self.calculator.add_item('Item2', 40.0, 1)
        result = self.calculator.calculate_total(0.2)
        self.assertAlmostEqual(result, 110.24, places=2)

    def test_calculate_total_on_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(0.0)

    def test_calculate_total_with_invalid_discount_raises_value_error(self):
        self.calculator.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_calculate_total_with_string_discount_raises_type_error(self):
        self.calculator.add_item('Item', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.1')

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('Item', 10.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Item1', 10.0, 3)
        self.calculator.add_item('Item2', 20.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_after_adding_same_item(self):
        self.calculator.add_item('Item', 10.0, 3)
        self.calculator.add_item('Item', 10.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Item1', 10.0, 1)
        self.calculator.add_item('Item2', 20.0, 1)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_on_empty_order(self):
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_clear_order_then_add_new_items(self):
        self.calculator.add_item('Item1', 10.0, 1)
        self.calculator.clear_order()
        self.calculator.add_item('Item2', 20.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Item2')

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single_item(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.assertEqual(set(self.calculator.list_items()), {'Apple'})

    def test_list_items_multiple_unique_items(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.calculator.add_item('Banana', 1.5, 1)
        self.assertEqual(set(self.calculator.list_items()), {'Apple', 'Banana'})

    def test_list_items_with_duplicate_additions(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.calculator.add_item('Apple', 2.5, 2)
        self.assertEqual(set(self.calculator.list_items()), {'Apple'})

    def test_is_empty_on_new_instance(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_with_items(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clearing(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())

    def test_full_workflow_simple_order(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        subtotal = self.calculator.get_subtotal()
        self.assertEqual(subtotal, 1050.0)
        total = self.calculator.calculate_total(0.1)
        self.assertAlmostEqual(total, 1158.75, places=2)

    def test_full_workflow_with_item_removal(self):
        self.calculator.add_item('Item1', 50.0, 1)
        self.calculator.add_item('Item2', 100.0, 1)
        self.calculator.remove_item('Item2')
        total = self.calculator.calculate_total(0.0)
        self.assertEqual(total, 73.8)

    def test_full_workflow_with_quantity_updates(self):
        self.calculator.add_item('Item', 20.0, 1)
        self.calculator.add_item('Item', 20.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        total = self.calculator.calculate_total(0.0)
        self.assertEqual(total, 86.1)

    def test_state_persistence_across_operations(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 30.0, 1)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        calc.add_item('Item2', 25.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 60.5)