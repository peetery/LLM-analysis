import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_empty_order_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_specific_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Orange', 1.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_add_duplicate_item_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_quantity_one_explicitly(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_with_price_as_integer(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2, 1)
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_add_item_with_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Candy', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 10000.0, 1)
        self.assertEqual(calc.get_subtotal(), 10000.0)

    def test_empty_name_string(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5, 1)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_same_name_but_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '1')

    def test_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)

    def test_remove_item_from_order_with_one_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_with_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_with_different_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 5)
        calc.add_item('Orange', 3.0, 10)
        self.assertEqual(calc.get_subtotal(), 41.0)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.25, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 3.75)

    def test_subtotal_with_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000)
        self.assertEqual(calc.get_subtotal(), 1500.0)

    def test_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_zero_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.0)

    def test_discount_very_close_to_one(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.99)
        self.assertAlmostEqual(result, 1.0)

    def test_negative_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_non_numeric_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_free_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_paid_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_shipping_exactly_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_shipping_zero_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_shipping_very_large_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(10000.0)
        self.assertEqual(result, 0.0)

    def test_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 20.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_tax_rates(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(50.0)
        self.assertEqual(result, 5.0)

    def test_tax_on_very_small_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.002)

    def test_tax_on_very_large_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(10000.0)
        self.assertEqual(result, 2000.0)

    def test_negative_amount_for_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_non_numeric_amount_for_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_total_with_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_with_valid_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        expected = (80.0 + 10.0) * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 2)
        total = calc.calculate_total()
        expected = 200.0 * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_requiring_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_with_maximum_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_with_single_item(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 30.0, 1)
        total = calc.calculate_total()
        expected = (30.0 + 5.0) * 1.1
        self.assertAlmostEqual(total, expected)

    def test_total_with_multiple_items(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 3)
        total = calc.calculate_total()
        expected = (120.0 + 0.0) * 1.1
        self.assertAlmostEqual(total, expected)

    def test_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.2
        self.assertAlmostEqual(total, expected)

    def test_complete_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 25.0, 2)
        calc.add_item('Banana', 30.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 110.0
        discounted = 99.0
        shipping = 10.0
        tax = (99.0 + 10.0) * 0.23
        expected = 99.0 + 10.0 + tax
        self.assertAlmostEqual(total, expected)

    def test_zero_tax_rate_total(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertAlmostEqual(total, expected)

    def test_zero_shipping_cost_total(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=0.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 * 1.2
        self.assertAlmostEqual(total, expected)

    def test_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_total_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 5)
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_on_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_after_adding_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_order_state_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_subtotal_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_on_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_with_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_not_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_empty_to_non_empty_transition(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_non_empty_to_empty_transition(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_purchase_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 25.0, 2)
        calc.add_item('Banana', 30.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 110.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 99.0)
        total = calc.calculate_total(0.1)
        expected = (99.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_multiple_discount_calculations(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.2)
        total3 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)
        self.assertNotEqual(total2, total3)

    def test_order_modification_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 20.0, 1)
        calc.remove_item('Apple')
        calc.add_item('Orange', 15.0, 3)
        self.assertEqual(calc.total_items(), 4)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 65.0)

    def test_all_thresholds_at_boundaries(self):
        calc = OrderCalculator(tax_rate=1.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 * 2.0
        self.assertAlmostEqual(total, expected)

    def test_minimum_viable_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.01, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 0)

    def test_maximum_complexity_order(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=500.0, shipping_cost=25.0)
        calc.add_item('Item1', 100.0, 10)
        calc.add_item('Item2', 50.0, 20)
        calc.add_item('Item3', 25.0, 40)
        total = calc.calculate_total(0.15)
        self.assertGreater(total, 0)

    def test_continue_after_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        try:
            calc.add_item('', 10.0, 1)
        except ValueError:
            pass
        calc.add_item('Banana', 20.0, 1)
        self.assertEqual(calc.total_items(), 2)

    def test_continue_after_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        try:
            calc.add_item(123, 10.0, 1)
        except TypeError:
            pass
        calc.add_item('Banana', 20.0, 1)
        self.assertEqual(calc.total_items(), 2)