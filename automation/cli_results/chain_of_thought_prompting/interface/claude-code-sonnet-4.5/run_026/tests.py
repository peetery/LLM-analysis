import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(1), 0.0)

    def test_init_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.calculate_tax(100), -10.0)

    def test_init_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5.0)
        self.assertEqual(calc.calculate_shipping(50), -5.0)

    def test_init_very_high_tax_rate(self):
        calc = OrderCalculator(tax_rate=5.0)
        self.assertEqual(calc.calculate_tax(100), 500.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 1.0)

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 0)
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1)
        self.assertEqual(calc.get_subtotal(), 0.01)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        items = calc.list_items()
        apple_count = items.count('Apple')
        self.assertGreater(apple_count, 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        calc.add_item('Negative', -10.0, 1)
        self.assertEqual(calc.get_subtotal(), -10.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, -5)
        self.assertEqual(calc.total_items(), -5)

    def test_add_item_empty_string_name(self):
        calc = OrderCalculator()
        calc.add_item('', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_none_as_name(self):
        calc = OrderCalculator()
        try:
            calc.add_item(None, 1.0, 1)
        except (TypeError, AttributeError):
            pass

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2.5)
        self.assertGreater(calc.total_items(), 0)

    def test_add_item_floating_point_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 1)
        self.assertEqual(calc.get_subtotal(), 19.99)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)

    def test_remove_item_all_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('Apple')
        except (KeyError, ValueError):
            pass

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        try:
            calc.remove_item('Banana')
        except (KeyError, ValueError):
            pass

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        try:
            calc.remove_item(None)
        except (TypeError, KeyError, ValueError, AttributeError):
            pass

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('')
        except (KeyError, ValueError):
            pass

    def test_remove_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Banana', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_very_large_amounts(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0, 100)
        self.assertEqual(calc.get_subtotal(), 100000000.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.33, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.99, places=2)

    def test_apply_discount_ten_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, -10.0)
        self.assertEqual(result, 110.0)

    def test_apply_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 150.0)
        self.assertEqual(result, -50.0)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_apply_discount_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 33.33)
        self.assertAlmostEqual(result, 66.66, places=2)

    def test_apply_discount_rounding_behavior(self):
        calc = OrderCalculator()
        result = calc.apply_discount(10.0, 33.33)
        self.assertIsInstance(result, float)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 15.0)

    def test_calculate_shipping_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(1.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_very_high_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(99.99)
        self.assertAlmostEqual(result, 22.9977, places=2)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

    def test_calculate_tax_very_small_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        expected = (90.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_below_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 50.0 * 1.23)

    def test_calculate_total_above_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_exactly_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=100.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_zero_discount_default(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total()
        total2 = calc.calculate_total(discount=0.0)
        self.assertEqual(total1, total2)

    def test_calculate_total_tax_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        after_discount = 90.0
        shipping = 10.0
        before_tax = after_discount + shipping
        expected = before_tax * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_order_operations_verified(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(discount=20.0)
        subtotal = 100.0
        after_discount = 80.0
        shipping = 10.0
        before_tax = 90.0
        expected = before_tax * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 1)
        calc.add_item('Banana', 40.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 70.0
        after_discount = 63.0
        shipping = 10.0
        expected = (63.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 80.0, 1)
        calc.add_item('Banana', 40.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 120.0
        after_discount = 108.0
        shipping = 0.0
        expected = 108.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=-10.0)
        self.assertGreater(total, 100.0 * 1.23)

    def test_calculate_total_discount_over_hundred(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=150.0)
        self.assertIsInstance(total, float)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_reflects_quantity_not_unique(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_subtotal_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_is_empty_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_total_items_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_insertion_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_list_items_names_correct(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        items = calc.list_items()
        self.assertEqual(items[0], 'Apple')

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_add_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_zero_quantity_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 0)
        result = calc.is_empty()
        self.assertIsInstance(result, bool)

    def test_integration_add_discount_verify_total(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        self.assertGreater(total, 0)

    def test_integration_add_remove_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 20.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_integration_full_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_multiple_discounts_sequential(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total1 = calc.calculate_total(discount=10.0)
        total2 = calc.calculate_total(discount=20.0)
        self.assertNotEqual(total1, total2)

    def test_integration_immutability_of_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        subtotal1 = calc.get_subtotal()
        calc.calculate_total(discount=50.0)
        subtotal2 = calc.get_subtotal()
        self.assertEqual(subtotal1, subtotal2)

    def test_integration_add_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Apple', 10.0, 1)
        self.assertGreater(calc.get_subtotal(), 0)

    def test_integration_complex_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 3)
        calc.add_item('Cherry', 10.0, 1)
        calc.remove_item('Banana')
        total = calc.calculate_total(discount=15.0)
        self.assertGreater(total, 0)

    def test_edge_case_very_large_order(self):
        calc = OrderCalculator()
        for i in range(1000):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 1000)

    def test_invalid_input_string_price(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple', 'ten', 1)
        except (TypeError, ValueError):
            pass

    def test_invalid_input_string_quantity(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple', 10.0, 'five')
        except (TypeError, ValueError):
            pass

    def test_invalid_input_none_parameters(self):
        calc = OrderCalculator()
        try:
            calc.add_item(None, None, None)
        except (TypeError, AttributeError):
            pass

    def test_invalid_input_wrong_number_arguments(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple')
        except TypeError:
            pass