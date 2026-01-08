import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_tax_rate_at_zero_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_tax_rate_at_one_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_invalid_tax_rate_greater_than_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_invalid_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_tax_rate_type_error_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_free_shipping_threshold_type_error_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_shipping_cost_type_error_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        calc.add_item('Cherry', 7.0, 4)
        self.assertEqual(calc.total_items(), 7)

    def test_add_duplicate_item_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_items_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 15.5, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 9.99 + 15.5 * 2, places=2)

    def test_add_item_invalid_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0, 1)

    def test_add_item_invalid_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 5.0, 1)

    def test_add_item_invalid_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_invalid_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0, 1)

    def test_add_item_invalid_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 5.0, 0)

    def test_add_item_invalid_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 5.0, -1)

    def test_add_item_invalid_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 6.0, 1)

    def test_add_item_type_error_name_as_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 5.0, 1)

    def test_add_item_type_error_price_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '10.50', 1)

    def test_add_item_type_error_quantity_as_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 5.0, 2.5)

    def test_add_item_edge_very_long_name(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 5.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_edge_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_edge_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01, 1)
        self.assertEqual(calc.get_subtotal(), 0.01)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.add_item('Cherry', 7.0, 1)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Cherry', items)
        self.assertNotIn('Banana', items)

    def test_remove_item_invalid_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_invalid_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_invalid_already_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_type_error_name_as_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_type_error_name_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_edge_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_get_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_with_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 15.5, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 40.99, places=2)

    def test_get_subtotal_invalid_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_edge_very_large_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0, 2)
        self.assertEqual(calc.get_subtotal(), 2000000.0)

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_partial_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.2)

    def test_apply_discount_invalid_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_type_error_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_type_error_discount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.5')

    def test_apply_discount_edge_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(1000.0, 0.001)
        self.assertAlmostEqual(result, 999.0, places=2)

    def test_calculate_shipping_free_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_free_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_paid_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_on_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_type_error_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_shipping_type_error_subtotal_as_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_shipping_edge_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_edge_very_large_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(1000000.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 10.0, places=2)

    def test_calculate_tax_with_zero_percent_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_type_error_amount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_edge_very_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(1000000.0)
        self.assertAlmostEqual(tax, 230000.0, places=2)

    def test_calculate_tax_edge_decimal_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_no_discount_no_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.0)
        expected = 100.0 + 23.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 200.0, 1)
        total = calc.calculate_total(0.5)
        discounted = 100.0
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 80.0
        expected = discounted + 10.0 + (discounted + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_one_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(1.0)
        discounted = 0.0
        expected = discounted + 10.0 + (discounted + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_order_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        calc.add_item('Banana', 30.0, 1)
        subtotal = 130.0
        discount = 0.1
        discounted_subtotal = subtotal * (1 - discount)
        shipping = 0.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        total = calc.calculate_total(discount)
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_invalid_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_calculate_total_invalid_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_invalid_discount_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_type_error_discount_as_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.5')

    def test_calculate_total_edge_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 125.0, 1)
        total = calc.calculate_total(0.2)
        discounted_subtotal = 100.0
        shipping = 0.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_edge_very_small_order_value(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01, 1)
        total = calc.calculate_total(0.0)
        subtotal = 0.01
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_edge_very_large_total_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.0, 500000)
        calc.add_item('Item2', 2.0, 500000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_readd_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.clear_order()
        calc.add_item('Banana', 3.0, 2)
        self.assertEqual(calc.total_items(), 2)
        items = calc.list_items()
        self.assertIn('Banana', items)
        self.assertNotIn('Apple', items)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Banana', 3.0, 1)
        calc.add_item('Cherry', 7.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_with_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_edge_verify_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_edge_order_independence(self):
        calc = OrderCalculator()
        calc.add_item('Zebra', 10.0, 1)
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Mango', 7.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Zebra', items)
        self.assertIn('Apple', items)
        self.assertIn('Mango', items)

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_not_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Banana', 3.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        calc.add_item('Cherry', 8.0, 1)
        calc.remove_item('Banana')
        subtotal = calc.get_subtotal()
        expected_subtotal = 10.0 * 2 + 8.0 * 1
        self.assertEqual(subtotal, expected_subtotal)
        total = calc.calculate_total(0.1)
        discounted_subtotal = expected_subtotal * 0.9
        shipping = 0.0
        tax = (discounted_subtotal + shipping) * 0.2
        expected_total = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected_total, places=2)

    def test_discount_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(0.1)
        discounted_subtotal = 90.0
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_free_shipping_qualification(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 80.0, 1)
        calc.add_item('Item2', 40.0, 1)
        total = calc.calculate_total(0.0)
        subtotal = 120.0
        shipping = 0.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_operations_on_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 5)
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 8)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_precision_and_rounding(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 15.49, 2)
        total = calc.calculate_total(0.15)
        subtotal = 9.99 + 15.49 * 2
        discounted_subtotal = subtotal * 0.85
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_persistence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        subtotal1 = calc.get_subtotal()
        self.assertEqual(subtotal1, 10.0)
        calc.add_item('Banana', 5.0, 2)
        subtotal2 = calc.get_subtotal()
        self.assertEqual(subtotal2, 20.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)