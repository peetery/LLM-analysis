import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_boundary_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_boundary_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_boundary_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_boundary_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_integer_parameters(self):
        calc = OrderCalculator(tax_rate=1, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 1)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(len(calc.items), 3)

    def test_add_same_item_twice_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_same_name_same_price_different_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 4)
        self.assertEqual(calc.items[0]['quantity'], 6)

    def test_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 3)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 2)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 2)

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 2)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 2)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 2)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10000)
        self.assertEqual(calc.items[0]['quantity'], 10000)

    def test_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 999999.99, 1)
        self.assertEqual(calc.items[0]['price'], 999999.99)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in calc.items])

    def test_remove_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_non_string_name_for_removal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_by_exact_name_match(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'apple')

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        calc.remove_item('Orange')
        self.assertEqual(len(calc.items), 0)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_with_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_subtotal_with_fractional_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 19.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 49.97, places=2)

    def test_subtotal_with_large_values(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 100000.0, 10)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_apply_valid_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_non_numeric_subtotal_in_apply_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_non_numeric_discount_in_apply_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_negative_subtotal_in_apply_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_below_threshold_shipping_applied(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_above_threshold_free_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_non_numeric_discounted_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_zero_subtotal_for_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_very_large_subtotal_for_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(1000000.0)
        self.assertEqual(result, 0.0)

    def test_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_tax_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_non_numeric_amount_for_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_negative_amount_for_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_very_small_amount_for_tax(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 80.0
        shipping = 0.0
        tax = (80.0 + 0.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(0.0)
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_shipping_cost(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_non_numeric_discount_in_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_invalid_discount_in_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_complete_order_flow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 80.0
        discounted = 72.0
        shipping = 0.0
        tax = 72.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 110.0, 1)
        total = calc.calculate_total(0.15)
        discounted = 93.5
        shipping = 10.0
        tax = (93.5 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_enabling_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 95.0, 1)
        total = calc.calculate_total(0.0)
        discounted = 95.0
        shipping = 10.0
        tax = (95.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_with_complex_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 25.0, 2)
        calc.add_item('Item2', 15.0, 3)
        calc.add_item('Item3', 10.0, 1)
        calc.add_item('Item4', 20.0, 2)
        calc.add_item('Item5', 5.0, 4)
        total = calc.calculate_total(0.1)
        subtotal = 50.0 + 45.0 + 10.0 + 40.0 + 20.0
        discounted = subtotal * 0.9
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_all_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0, free_shipping_threshold=0.0)
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 50.0)

    def test_total_with_maximum_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total(1.0)
        discounted = 0.0
        shipping = 10.0
        tax = 10.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_empty_order_item_count(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_single_item_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_single_item_with_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_multiple_items_count(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.0, 2)
        calc.add_item('Item2', 2.0, 3)
        calc.add_item('Item3', 3.0, 4)
        self.assertEqual(calc.total_items(), 9)

    def test_after_adding_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_large_total_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.0, 5000)
        calc.add_item('Item2', 2.0, 5000)
        self.assertEqual(calc.total_items(), 10000)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_verify_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_verify_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_verify_get_subtotal_raises_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_from_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(sorted(items), sorted(['Apple', 'Banana', 'Orange']))

    def test_no_duplicates_in_list(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_uniqueness_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Apple', 1.5, 1)
        items = calc.list_items()
        self.assertEqual(sorted(items), sorted(['Apple', 'Banana']))

    def test_list_preserves_all_unique_names(self):
        calc = OrderCalculator()
        names = ['Item1', 'Item2', 'Item3', 'Item4', 'Item5', 'Item6', 'Item7', 'Item8', 'Item9', 'Item10']
        for i, name in enumerate(names):
            calc.add_item(name, 1.0, 1)
        items = calc.list_items()
        self.assertEqual(sorted(items), sorted(names))

    def test_new_order_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_order_with_items_is_not_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_empty_after_adding_then_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_not_empty_after_adding_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertFalse(calc.is_empty())

    def test_empty_after_removing_all_items_individually(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        calc.remove_item('Orange')
        self.assertTrue(calc.is_empty())

    def test_precise_calculation_with_decimals(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 19.99, 1)
        total = calc.calculate_total(0.15)
        subtotal = 29.98
        discounted = subtotal * 0.85
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_rounding_behavior(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.99, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 32.97, places=2)

    def test_full_lifecycle_test(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 20.0, 2)
        calc.add_item('Item2', 30.0, 1)
        calc.remove_item('Item2')
        calc.add_item('Item3', 15.0, 3)
        total = calc.calculate_total(0.1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_alternating_add_remove(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.remove_item('Item1')
        calc.add_item('Item2', 20.0, 1)
        calc.remove_item('Item2')
        self.assertTrue(calc.is_empty())

    def test_exact_threshold_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0, 1)
        discounted = 120.0 * (1 - 100.0 / 120.0)
        if abs(discounted - 100.0) < 0.01:
            total = calc.calculate_total(100.0 / 120.0)

    def test_just_below_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_state_after_exception(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        try:
            calc.add_item('', 2.0, 1)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')

    def test_multiple_invalid_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        try:
            calc.add_item('Banana', -1.0, 1)
        except ValueError:
            pass
        try:
            calc.remove_item('Orange')
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)

    def test_zero_tax_zero_shipping(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total(0.2)
        self.assertEqual(total, 40.0)

    def test_maximum_values(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 999999.99, 1000)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 999999990.0, places=2)

    def test_minimum_valid_values(self):
        calc = OrderCalculator()
        calc.add_item('CheapItem', 0.01, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 0.01)