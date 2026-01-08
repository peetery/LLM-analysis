import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc.tax_rate, 0.15)

    def test_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=75.0, shipping_cost=12.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 75.0)
        self.assertEqual(calc.shipping_cost, 12.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item1', 100.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        calc.add_item('Item1', 50.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item1', 50.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_high_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.tax_rate, -0.1)

    def test_negative_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-10.0)
        self.assertEqual(calc.free_shipping_threshold, -10.0)

    def test_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5.0)
        self.assertEqual(calc.shipping_cost, -5.0)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.add_item('Item3', 20.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_with_decimal_price(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 19.99)
        self.assertEqual(calc.get_subtotal(), 19.99)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 0)
        self.assertEqual(calc.total_items(), 0)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 999999.99)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        calc.add_item('Item1', 30.0, 2)
        items = calc.list_items()
        self.assertIn('Item1', items)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_explicit_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        calc.add_item('Item1', -50.0)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, -50.0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, -1)
        self.assertEqual(calc.total_items(), -1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        calc.add_item('', 50.0)
        self.assertIn('', calc.list_items())

    def test_add_item_with_none_as_name(self):
        calc = OrderCalculator()
        try:
            calc.add_item(None, 50.0)
        except (TypeError, AttributeError):
            pass

    def test_add_item_with_whitespace_only_name(self):
        calc = OrderCalculator()
        calc.add_item('   ', 50.0)
        self.assertIn('   ', calc.list_items())

    def test_add_item_with_non_numeric_price(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Item1', 'fifty')
        except TypeError:
            pass

    def test_add_item_with_non_integer_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1.5)
        total = calc.total_items()
        self.assertEqual(total, 1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())
        self.assertIn('Item2', calc.list_items())

    def test_remove_item_after_multiple_adds(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('Item1')
        except (KeyError, ValueError):
            pass

    def test_remove_last_remaining_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_with_exact_name_match(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        try:
            calc.remove_item('Item2')
        except (KeyError, ValueError):
            pass

    def test_remove_with_empty_string_name(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('')
        except (KeyError, ValueError):
            pass

    def test_remove_with_none_as_name(self):
        calc = OrderCalculator()
        try:
            calc.remove_item(None)
        except (TypeError, KeyError, ValueError):
            pass

    def test_remove_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.remove_item('Item1')
        try:
            calc.remove_item('Item1')
        except (KeyError, ValueError):
            pass

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 1)
        self.assertEqual(calc.get_subtotal(), 130.0)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 19.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 59.97, places=2)

    def test_subtotal_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_with_zero_price_item(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0, 5)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_after_item_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.remove_item('Item1')
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_subtotal_with_large_numbers(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100000.0, 10)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_total_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 3)
        calc.add_item('Item3', 20.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 3)
        calc.add_item('Item2', 30.0, 2)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 2)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        self.assertEqual(calc.list_items(), ['Item1'])

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.add_item('Item3', 20.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)
        self.assertIn('Item3', items)

    def test_list_preserves_order(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.add_item('Item3', 20.0)
        items = calc.list_items()
        self.assertEqual(items[0], 'Item1')
        self.assertEqual(items[1], 'Item2')
        self.assertEqual(items[2], 'Item3')

    def test_list_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.remove_item('Item1')
        self.assertNotIn('Item1', calc.list_items())

    def test_list_returns_copy_not_reference(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        items = calc.list_items()
        items.append('Item2')
        self.assertEqual(len(calc.list_items()), 1)

    def test_empty_order_returns_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_order_with_items_returns_false(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        self.assertFalse(calc.is_empty())

    def test_empty_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_not_empty_with_zero_price_item(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0)
        self.assertFalse(calc.is_empty())

    def test_apply_ten_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_negative_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, -0.1)
        self.assertEqual(result, 110.0)

    def test_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.5)
        self.assertEqual(result, -50.0)

    def test_discount_greater_than_subtotal_value(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 2.0)
        self.assertEqual(result, -100.0)

    def test_shipping_when_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_free_shipping_when_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_with_default_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_exactly_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_with_zero_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0)
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_with_very_high_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(10000.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_negative_discounted_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0)
        shipping = calc.calculate_shipping(-10.0)
        self.assertEqual(shipping, 10.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_with_default_rate(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 15.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_with_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_very_small_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023, places=4)

    def test_tax_with_hundred_percent_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(-100.0)
        self.assertEqual(tax, -23.0)

    def test_total_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total(0.0)
        expected = 100.0 + 10.0 + 110.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_ten_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total(0.1)
        discounted = 90.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item1', 60.0, 2)
        total = calc.calculate_total(0.0)
        expected = 120.0 + 120.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_of_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total(0.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_exactly_at_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(0.0)
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total = calc.calculate_total(1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item1', 50.0)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_total_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item1', 50.0)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 50.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_complete_order_flow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 130.0
        discounted = subtotal * 0.9
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_after_item_modifications(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        total1 = calc.calculate_total(0.0)
        calc.remove_item('Item2')
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)

    def test_multiple_discount_levels(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0)
        total0 = calc.calculate_total(0.0)
        total25 = calc.calculate_total(0.25)
        total50 = calc.calculate_total(0.5)
        total100 = calc.calculate_total(1.0)
        self.assertGreater(total0, total25)
        self.assertGreater(total25, total50)
        self.assertGreater(total50, total100)

    def test_threshold_boundary_with_discount(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item1', 120.0)
        total = calc.calculate_total(0.1667)
        discounted = 120.0 * (1 - 0.1667)
        self.assertAlmostEqual(discounted, 100.0, places=1)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_sets_subtotal_to_zero(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_sets_total_items_to_zero(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_twice_consecutively(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_operations_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.clear_order()
        calc.add_item('Item2', 30.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.add_item('Item2', 30.0)
        calc.remove_item('Item1')
        calc.add_item('Item3', 40.0)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_discount_affecting_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 110.0)
        total = calc.calculate_total(0.15)
        discounted = 110.0 * 0.85
        self.assertLess(discounted, 100.0)

    def test_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 10.0)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_decimal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.01, 1)
        calc.add_item('Item2', 0.99, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1.0, places=2)

    def test_order_modification_during_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        total1 = calc.calculate_total(0.0)
        calc.add_item('Item2', 30.0)
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)

    def test_zero_value_order_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0, 5)
        total = calc.calculate_total(0.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_high_value_order(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 100000.0)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 100000.0)

    def test_mixed_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 10.0, 5)
        calc.add_item('Item3', 10.0, 10)
        calc.add_item('Item4', 10.0, 100)
        self.assertEqual(calc.total_items(), 116)
        self.assertEqual(calc.get_subtotal(), 1160.0)

    def test_invalid_type_for_price(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Item1', 'fifty')
        except TypeError:
            pass

    def test_invalid_type_for_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1.5)
        self.assertEqual(calc.total_items(), 1.5)

    def test_invalid_type_for_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        try:
            calc.calculate_total('ten percent')
        except TypeError:
            pass

    def test_invalid_type_for_name(self):
        calc = OrderCalculator()
        try:
            calc.add_item(123, 50.0)
        except (TypeError, AttributeError):
            pass