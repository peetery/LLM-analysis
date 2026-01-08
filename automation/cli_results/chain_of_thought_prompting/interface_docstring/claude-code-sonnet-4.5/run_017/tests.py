import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=150.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 150.0)
        self.assertEqual(calc.shipping_cost, 15.0)

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

    def test_empty_items_list_after_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(len(calc.list_items()), 0)

    def test_tax_rate_below_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_non_numeric_tax_rate_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_tax_rate_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Apple', calc.list_items())

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.list_items()), 3)
        self.assertIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())
        self.assertIn('Orange', calc.list_items())

    def test_add_duplicate_item_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_quantity_one_explicitly(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99)
        self.assertIn('Diamond', calc.list_items())

    def test_add_item_with_minimal_valid_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny', 0.01)
        self.assertIn('Penny', calc.list_items())

    def test_empty_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -10.0)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=-5)

    def test_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '10.0')

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, quantity=2.5)

    def test_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5)

    def test_none_as_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', None)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_item_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        calc.remove_item('Banana')
        self.assertNotIn('Banana', calc.list_items())
        self.assertIn('Apple', calc.list_items())
        self.assertIn('Orange', calc.list_items())

    def test_remove_last_remaining_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_single_item_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_multiple_items_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.add_item('Orange', 3.0, quantity=1)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_items_with_different_quantities_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, quantity=5)
        calc.add_item('Banana', 1.5, quantity=10)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_subtotal_after_duplicate_additions(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, quantity=3)
        calc.add_item('Apple', 2.0, quantity=2)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_empty_order_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.0)
        self.assertEqual(result, 100)

    def test_partial_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.2)
        self.assertEqual(result, 80)

    def test_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 1.0)
        self.assertEqual(result, 0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0, 0.5)
        self.assertEqual(result, 0)

    def test_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.01)
        self.assertEqual(result, 99)

    def test_negative_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100, 0.2)

    def test_discount_below_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100, -0.1)

    def test_discount_above_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100, 1.5)

    def test_non_numeric_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100, '0.2')

    def test_below_threshold_shipping_applies(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50)
        self.assertEqual(result, 10.0)

    def test_at_threshold_free_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100)
        self.assertEqual(result, 0.0)

    def test_above_threshold_free_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150)
        self.assertEqual(result, 0.0)

    def test_zero_subtotal_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0)
        self.assertEqual(result, 10.0)

    def test_just_below_threshold_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_just_above_threshold_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_non_numeric_shipping_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_none_as_shipping_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_positive_amount_tax(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 23)

    def test_zero_amount_tax(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0)
        self.assertEqual(result, 0)

    def test_various_tax_rates(self):
        calc1 = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc1.calculate_tax(100), 0)
        calc2 = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc2.calculate_tax(100), 15)
        calc3 = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc3.calculate_tax(100), 100)

    def test_small_amount_tax(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_negative_amount_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100)

    def test_non_numeric_tax_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_none_as_tax_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_single_item_no_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_single_item_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0)
        calc.add_item('Banana', 40.0)
        calc.add_item('Orange', 50.0)
        total = calc.calculate_total()
        expected = 120.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_with_discount_shipping_applies(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0)
        total = calc.calculate_total(discount=0.3)
        discounted = 120.0 * 0.7
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_with_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_full_discount_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_with_discount_and_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, quantity=2)
        calc.add_item('Banana', 20.0)
        total = calc.calculate_total(discount=0.1)
        subtotal = 80.0
        discounted = subtotal * 0.9
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_brings_subtotal_to_exactly_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 125.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_discount_explicitly(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_empty_order_calculate_total(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_invalid_discount_negative_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_invalid_discount_above_range_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_non_numeric_discount_calculate_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_five(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_different_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.add_item('Orange', 3.0, quantity=5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Apple', 1.5, quantity=4)
        self.assertEqual(calc.total_items(), 7)

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

    def test_clear_and_verify_all_state_reset(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.list_items(), [])

    def test_clear_then_add_new_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Apple', 1.5, quantity=2)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_order_independence(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0)
        calc.add_item('Apple', 1.5)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_is_empty_newly_initialized(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_then_removing_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, quantity=2)
        calc.add_item('Banana', 50.0)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 110.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 99.0)
        total = calc.calculate_total(discount=0.1)
        expected = (99.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5)
        self.assertIn('Apple', calc.list_items())

    def test_multiple_discount_calculations(self):
        calc = OrderCalculator()
        result1 = calc.apply_discount(100, 0.2)
        result2 = calc.apply_discount(100, 0.2)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, 80)

    def test_tax_calculation_consistency(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 90.0)
        total = calc.calculate_total(discount=0.0)
        discounted_subtotal = 90.0
        shipping = 10.0
        expected_tax = calc.calculate_tax(discounted_subtotal + shipping)
        expected_total = discounted_subtotal + shipping + expected_tax
        self.assertAlmostEqual(total, expected_total, places=2)

    def test_shipping_threshold_boundary_with_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 96.0
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_tax_rate_complete_order(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_maximum_values_integration(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Expensive', 999999.99, quantity=100)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)