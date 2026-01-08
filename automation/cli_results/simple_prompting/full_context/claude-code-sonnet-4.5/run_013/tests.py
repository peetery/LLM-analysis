import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_free_shipping_threshold_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_shipping_cost_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.0)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_same_name_and_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 1)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_price_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_price_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_price_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.0', 1)

    def test_add_item_quantity_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_quantity_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_quantity_not_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 1.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_nonexistent_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 4)
        self.assertEqual(calc.get_subtotal(), 4.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_negative_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_subtotal_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_invalid_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 72.0)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 10)
        total = calc.calculate_total(0.1)
        self.assertEqual(total, 108.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 15)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 180.0)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_invalid_type_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 8)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 0.5, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_duplicate_names_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_is_empty_new_calculator(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_remove_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())