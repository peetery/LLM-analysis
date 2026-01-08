import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc.tax_rate, 0.15)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        self.assertEqual(calc.free_shipping_threshold, 200.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=150.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 150.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_tax_rate_at_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_at_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_at_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_at_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_non_numeric_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_non_numeric_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_non_numeric_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 2.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_duplicate_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Apple', 2.5)
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_add_item_with_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Grape', 0.5, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99)
        self.assertEqual(calc.items[0]['price'], 999999.99)

    def test_add_item_price_as_integer(self):
        calc = OrderCalculator()
        calc.add_item('Book', 10, 2)
        self.assertEqual(calc.items[0]['price'], 10)

    def test_add_item_name_with_special_characters(self):
        calc = OrderCalculator()
        calc.add_item('Item-A #1 50%', 5.0)
        self.assertEqual(calc.items[0]['name'], 'Item-A #1 50%')

    def test_add_item_name_with_whitespace(self):
        calc = OrderCalculator()
        calc.add_item('  Item  ', 5.0)
        self.assertEqual(calc.items[0]['name'], '  Item  ')

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0)

    def test_add_item_whitespace_only_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0)

    def test_add_item_zero_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10)

    def test_add_item_zero_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 5.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 5.0, -5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 5.0)

    def test_add_item_non_numeric_price_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10')

    def test_add_item_non_integer_quantity_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 5.0, 1.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in calc.items])

    def test_remove_item_with_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_immediately_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_already_removed_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 4)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 9.5)

    def test_get_subtotal_mixed_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        calc.add_item('Banana', 1.0, 3)
        calc.add_item('Cherry', 3.0, 5)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_very_small_prices(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01, 10)
        self.assertAlmostEqual(calc.get_subtotal(), 0.1, places=2)

    def test_get_subtotal_large_values(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 9999.99, 10)
        self.assertAlmostEqual(calc.get_subtotal(), 99999.9, places=2)

    def test_get_subtotal_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_ten_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_various_subtotals(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 0.2), 40.0)
        self.assertEqual(calc.apply_discount(200.0, 0.15), 170.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_non_numeric_subtotal_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_non_numeric_discount_raises_type_error(self):
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

    def test_calculate_shipping_slightly_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_slightly_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_different_tax_rates(self):
        calc1 = OrderCalculator(tax_rate=0.1)
        calc2 = OrderCalculator(tax_rate=0.5)
        self.assertAlmostEqual(calc1.calculate_tax(100.0), 10.0, places=2)
        self.assertAlmostEqual(calc2.calculate_tax(100.0), 50.0, places=2)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_with_one_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_on_very_large_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(999999.99)
        self.assertAlmostEqual(result, 229999.9977, places=2)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_amount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total(discount=0.1)
        discounted = 90.0
        shipping = 10.0
        tax = (90.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping_cost(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_complex_calculation(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 3)
        total = calc.calculate_total(discount=0.1)
        subtotal = 120.0
        discounted = 108.0
        shipping = 0.0
        tax = 108.0 * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_free_shipping_boundary(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_just_below_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 99.99)
        total = calc.calculate_total()
        expected = 99.99 + 10.0 + 109.99 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total_with_zero = calc.calculate_total(discount=0.0)
        total_without = calc.calculate_total()
        self.assertAlmostEqual(total_with_zero, total_without, places=2)

    def test_calculate_total_with_full_discount_but_shipping_applies(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(discount=1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 0.0
        self.assertEqual(total, expected)

    def test_calculate_total_tax_on_discounted_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=20.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=0.5)
        discounted = 50.0
        shipping = 20.0
        tax = (50.0 + 20.0) * 0.1
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 7)
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Cherry', 3.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_then_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_order_independent(self):
        calc = OrderCalculator()
        calc.add_item('Cherry', 3.0)
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana', 'Cherry'})

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.remove_item('Apple')
        calc.add_item('Apple', 2.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_shipping_threshold_boundary_testing(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 50.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_tax_calculation_on_discounted_subtotal_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=200.0, shipping_cost=20.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=0.5)
        discounted = 50.0
        shipping = 20.0
        tax = (50.0 + 20.0) * 0.25
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Item1', 0.01, 3)
        calc.add_item('Item2', 0.99, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 2.01, places=2)

    def test_large_order(self):
        calc = OrderCalculator()
        for i in range(50):
            calc.add_item(f'Item{i}', 1.0 + i * 0.1, 1)
        self.assertEqual(len(calc.items), 50)
        subtotal = calc.get_subtotal()
        self.assertGreater(subtotal, 0)

    def test_state_independence_multiple_instances(self):
        calc1 = OrderCalculator(tax_rate=0.1)
        calc2 = OrderCalculator(tax_rate=0.2)
        calc1.add_item('Apple', 10.0)
        calc2.add_item('Banana', 20.0)
        self.assertEqual(len(calc1.items), 1)
        self.assertEqual(len(calc2.items), 1)
        self.assertNotEqual(calc1.items[0]['name'], calc2.items[0]['name'])

    def test_item_accumulation(self):
        calc = OrderCalculator()
        for _ in range(10):
            calc.add_item('Apple', 2.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 10)

    def test_comprehensive_exception_handling(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)
        with self.assertRaises(TypeError):
            calc.add_item(123, 50.0)