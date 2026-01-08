import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_high_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=10000.0)
        self.assertEqual(calc.free_shipping_threshold, 10000.0)

    def test_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.tax_rate, -0.1)

    def test_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5.0)
        self.assertEqual(calc.shipping_cost, -5.0)

    def test_negative_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-50.0)
        self.assertEqual(calc.free_shipping_threshold, -50.0)

    def test_very_high_tax_rate(self):
        calc = OrderCalculator(tax_rate=2.0)
        self.assertEqual(calc.tax_rate, 2.0)

    def test_float_precision_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.075)
        self.assertEqual(calc.tax_rate, 0.075)

    def test_non_numeric_tax_rate_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_shipping_values(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, quantity=1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_add_item_with_float_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=2.5)
        self.assertGreater(calc.total_items(), 0)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 99999.99)
        self.assertEqual(calc.get_subtotal(), 99999.99)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        calc.add_item('', 10.0)
        self.assertIn('', calc.list_items())

    def test_add_item_with_whitespace_name(self):
        calc = OrderCalculator()
        calc.add_item('   ', 10.0)
        self.assertIn('   ', calc.list_items())

    def test_add_item_with_special_characters(self):
        calc = OrderCalculator()
        calc.add_item('Ä‚Ă�\xadtem-123!@#', 10.0)
        self.assertIn('Ä‚Ă�\xadtem-123!@#', calc.list_items())

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10.0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=-5)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=0)

    def test_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_non_numeric_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, quantity='5')

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_remove_last_remaining_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('')

    def test_remove_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(KeyError):
            calc.remove_item('item')

    def test_remove_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_subtotal_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_of_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_subtotal_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_after_add_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_with_zero_price_items(self):
        calc = OrderCalculator()
        calc.add_item('Free', 0.0, quantity=5)
        calc.add_item('Paid', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_subtotal_with_large_values(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 99999.99, quantity=10)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.9, places=2)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.99, quantity=3)
        calc.add_item('Item2', 1.49, quantity=2)
        self.assertAlmostEqual(calc.get_subtotal(), 5.95, places=2)

    def test_subtotal_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_ten_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.1)
        self.assertEqual(result, 0.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_over_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.5)
        self.assertEqual(result, -50.0)

    def test_apply_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_float_precision_in_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(10.0, 0.333)
        self.assertAlmostEqual(result, 6.67, places=2)

    def test_negative_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, -0.1)
        self.assertEqual(result, 110.0)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_non_numeric_subtotal_in_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100.0', 0.1)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_shipping_at_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_shipping_on_zero_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_shipping_with_negative_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(-10.0)
        self.assertEqual(result, 10.0)

    def test_shipping_with_custom_rates(self):
        calc = OrderCalculator(free_shipping_threshold=200.0, shipping_cost=25.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 25.0)

    def test_shipping_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_very_high_subtotal_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(999999.0)
        self.assertEqual(result, 0.0)

    def test_non_numeric_subtotal_in_shipping(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50.0')

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_tax_with_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_on_very_large_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(999999.0)
        self.assertAlmostEqual(result, 229999.77, places=2)

    def test_tax_on_small_decimal(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_tax_with_negative_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(-100.0)
        self.assertEqual(result, -23.0)

    def test_non_numeric_amount_in_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100.0')

    def test_total_with_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 80.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_on_empty_order(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0)
        total = calc.calculate_total()
        self.assertGreaterEqual(total, 0.0)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 150.0)
        total = calc.calculate_total(discount=0.0)
        expected = 150.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_without_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0 + (50.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_multiple_items(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 30.0, quantity=2)
        calc.add_item('Item2', 40.0)
        total = calc.calculate_total(discount=0.0)
        subtotal = 100.0
        shipping = 0.0
        tax = subtotal * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=0.0)
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_over_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=1.5)
        self.assertIsInstance(total, float)

    def test_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_total_with_zero_shipping_cost(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=0.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 50.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_after_modifications(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 60.0)
        calc.remove_item('Item2')
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0 + (50.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_complex_order_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 30.0, quantity=2)
        calc.add_item('Item2', 25.0, quantity=2)
        total = calc.calculate_total(discount=0.2)
        subtotal = 110.0
        discounted = 88.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_edge_case_combination(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=1.0)
        self.assertEqual(total, 0.0)

    def test_precision_test(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 0.1, quantity=3)
        calc.add_item('Item2', 0.2, quantity=2)
        total = calc.calculate_total(discount=0.1)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    def test_negative_discount_in_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=-0.1)
        self.assertGreater(total, 100.0)

    def test_non_numeric_discount_in_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_count_on_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_count_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_count_single_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_count_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_count_after_add_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Banana', 2.0, quantity=2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_count_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_count_with_zero_quantity_items(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Item', 10.0, quantity=0)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 0)

    def test_count_with_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, quantity=10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_re_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_clear_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_after_clear_subtotal_is_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_after_clear_is_empty_is_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_after_clear_total_items_is_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=10)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_after_clear_list_items_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertIn('Banana', items)

    def test_list_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_order_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items1 = calc.list_items()
        items2 = calc.list_items()
        self.assertEqual(items1, items2)

    def test_list_with_duplicate_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Apple', 2.0)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_list_is_mutable(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        items.append('Banana')
        self.assertNotIn('Banana', calc.list_items())

    def test_list_contains_strings(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        for item in items:
            self.assertIsInstance(item, str)

    def test_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_not_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_empty_after_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_empty_state_consistency(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), calc.total_items() == 0)
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.is_empty(), calc.total_items() == 0)

    def test_empty_with_zero_quantity_items(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Item', 10.0, quantity=0)
        except ValueError:
            pass
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 40.0, quantity=2)
        calc.add_item('Item2', 30.0)
        total = calc.calculate_total(discount=0.1)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    def test_modify_and_recalculate(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0)
        total1 = calc.calculate_total()
        calc.remove_item('Item1')
        calc.add_item('Item2', 30.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_multiple_orders_with_same_calculator(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.calculate_total()
        calc.clear_order()
        calc.add_item('Item2', 20.0)
        total = calc.calculate_total()
        self.assertGreater(total, 0)

    def test_shipping_threshold_edge_cases(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, quantity=2)
        total = calc.calculate_total()
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_affecting_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 96.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_item_name_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 2.0, quantity=3)
        items = calc.list_items()
        apple_count = items.count('Apple')
        self.assertGreaterEqual(apple_count, 1)

    def test_float_precision_across_calculations(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 0.1, quantity=10)
        calc.add_item('Item2', 0.2, quantity=5)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Banana', 2.0, quantity=2)
        total_items = calc.total_items()
        is_empty = calc.is_empty()
        list_items = calc.list_items()
        subtotal = calc.get_subtotal()
        self.assertEqual(total_items == 0, is_empty)
        self.assertEqual(len(list_items), 2)
        self.assertGreater(subtotal, 0)