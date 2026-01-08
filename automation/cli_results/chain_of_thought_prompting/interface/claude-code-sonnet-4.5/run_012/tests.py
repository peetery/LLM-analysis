import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_constructor_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)

    def test_constructor_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)

    def test_constructor_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_constructor_with_negative_parameters(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1, free_shipping_threshold=-100, shipping_cost=-10)

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_with_floating_point_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_add_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_list_items_in_populated_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_on_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_on_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_total_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_subtotal_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_of_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 5.97, places=2)

    def test_subtotal_with_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 10000)
        self.assertEqual(calc.get_subtotal(), 10000.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_valid_percentage_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_100_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_decimal_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 15.5)
        self.assertAlmostEqual(result, 84.49145, places=2)

    def test_apply_discount_as_decimal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 99.5)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_at_exact_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_shipping_with_zero_discounted_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_with_negative_discounted_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-50.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_total_of_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_total_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        discounted = 90.0
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_100_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=100.0)
        expected = 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=150.0)

    def test_total_calculation_order_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        discounted = 90.0
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_custom_shipping_settings(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 40.0, 1)
        total = calc.calculate_total()
        expected = 40.0 + 5.0 + 45.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_end_to_end_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 2)
        total = calc.calculate_total(discount=10.0)
        subtotal = 100.0
        discounted = 90.0
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        total1 = calc.calculate_total()
        calc.remove_item('Apple')
        calc.add_item('Banana', 50.0, 1)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_discount_edge_case_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 110.0, 1)
        total = calc.calculate_total(discount=10.0)
        discounted = 99.0
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_consistency_after_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        subtotal1 = calc.get_subtotal()
        calc.calculate_total()
        subtotal2 = calc.get_subtotal()
        self.assertEqual(subtotal1, subtotal2)

    def test_immutability_of_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        items_before = calc.total_items()
        calc.calculate_total()
        items_after = calc.total_items()
        self.assertEqual(items_before, items_after)

    def test_multiple_calculate_total_calls(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total(discount=10.0)
        total2 = calc.calculate_total(discount=10.0)
        self.assertEqual(total1, total2)

    def test_invalid_type_for_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_invalid_type_for_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'expensive', 1)

    def test_invalid_type_for_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 'many')

    def test_invalid_type_for_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='large')

    def test_precision_in_money_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.99, 3)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_rounding_behavior(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.005, 1)
        subtotal = calc.get_subtotal()
        self.assertIsInstance(subtotal, float)

    def test_very_small_amounts(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 0)

    def test_very_large_amounts(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 1000000.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 1000000.0)

    def test_exactly_at_free_shipping_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 111.11, 1)
        total = calc.calculate_total(discount=10.0)
        discounted = 100.0
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)