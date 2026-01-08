import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertIsNotNone(calc)

    def test_init_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertIsNotNone(calc)

    def test_init_with_tax_rate_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_with_tax_rate_at_boundary_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertIsNotNone(calc)

    def test_init_with_tax_rate_at_boundary_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertIsNotNone(calc)

    def test_init_with_invalid_tax_rate_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_init_with_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertIsNotNone(calc)

    def test_init_with_invalid_free_shipping_threshold_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')

    def test_init_with_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertIsNotNone(calc)

    def test_init_with_invalid_shipping_cost_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_single_item_normally(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_duplicate_item_same_name_and_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_same_name_but_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_with_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_with_invalid_name_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_add_item_with_price_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_with_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_add_item_with_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.01, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_invalid_price_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'invalid', 1)

    def test_add_item_with_quantity_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_with_invalid_quantity_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 'invalid')

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_remove_non_existent_item_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_with_invalid_name_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_then_verify_not_in_list(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_get_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.0, 5)
        self.assertEqual(calc.get_subtotal(), 11.0)

    def test_get_subtotal_with_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_apply_discount_with_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_with_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_with_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_with_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_with_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_with_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_invalid_subtotal_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('invalid', 0.2)

    def test_apply_discount_with_invalid_discount_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, 'invalid')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold_exactly(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_with_zero_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_negative_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(-50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_invalid_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('invalid')

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 20.0)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_on_negative_amount_raises_value_error(self):
        calc = OrderCalculator(tax_rate=0.2)
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_with_invalid_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('invalid')

    def test_calculate_tax_accuracy(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_total_with_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 72.0)

    def test_calculate_total_with_free_shipping_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 180.0)

    def test_calculate_total_with_shipping_cost_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 72.0)

    def test_calculate_total_with_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_calculate_total_with_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_with_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_with_invalid_discount_type_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('invalid')

    def test_calculate_total_complex_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(0.1)
        expected = (100.0 * 0.9 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 60.0)

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        expected = (80.0 + 10.0) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_with_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.5, 7)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_and_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_when_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_total_items_returns_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_from_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', calc.list_items())
        self.assertEqual(len(calc.list_items()), 1)

    def test_list_items_with_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_order_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        items1 = calc.list_items()
        items2 = calc.list_items()
        self.assertEqual(items1, items2)

    def test_is_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_complete_workflow_add_calculate_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_apply_discount_multiple_times_sequentially(self):
        calc = OrderCalculator()
        result1 = calc.apply_discount(100.0, 0.1)
        result2 = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result1, 90.0)
        self.assertEqual(result2, 80.0)

    def test_add_remove_add_again_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_calculate_total_multiple_times_idempotency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.1)
        self.assertEqual(total1, total2)

    def test_order_at_exact_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 120.0)

    def test_very_large_order_total(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 10000.0, 100)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 1000000.0)

    def test_exception_does_not_corrupt_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        try:
            calc.add_item('Apple', 2.0, 1)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 2)

    def test_unicode_characters_in_item_names(self):
        calc = OrderCalculator()
        calc.add_item('Ă„pfel', 1.5, 2)
        self.assertIn('Ă„pfel', calc.list_items())

    def test_very_long_item_names(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 1.5, 1)
        self.assertIn(long_name, calc.list_items())

    def test_floating_point_precision_in_calculations(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Apple', 0.1, 3)
        total = calc.calculate_total(0.0)
        self.assertIsInstance(total, float)

    def test_tax_on_shipping_cost(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_with_quantity_aggregation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Cherry', 3.0, 2)
        self.assertEqual(calc.total_items(), 10)
        self.assertAlmostEqual(calc.get_subtotal(), 17.0, places=2)