import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
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

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_string_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_string_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_string_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_none_as_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_list_as_parameter(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_specified_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        calc.add_item('Tool', 15.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_merge_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 3)
        calc.add_item('Widget', 10.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 9.99)
        self.assertAlmostEqual(calc.get_subtotal(), 9.99)

    def test_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_item_with_spaces_in_name(self):
        calc = OrderCalculator()
        calc.add_item('Premium Widget', 10.0)
        self.assertIn('Premium Widget', calc.list_items())

    def test_minimum_valid_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 0.01)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 99999.99)
        self.assertAlmostEqual(calc.get_subtotal(), 99999.99)

    def test_multiple_merges(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 2)
        calc.add_item('Widget', 10.0, 3)
        calc.add_item('Widget', 10.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Widget', 0.0)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Widget', -10.0)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Widget', 10.0, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Widget', 10.0, -5)

    def test_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            calc.add_item('Widget', 15.0)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Widget', '10.00')

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Widget', 10.0, 5.5)

    def test_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_list_as_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Widget', [10.0])

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.remove_item('Widget')
        self.assertTrue(calc.is_empty())

    def test_remove_from_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        calc.add_item('Tool', 15.0)
        calc.remove_item('Gadget')
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Widget', items)
        self.assertIn('Tool', items)

    def test_remove_last_item(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.remove_item('Widget')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Widget')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Widget')

    def test_remove_already_removed_item(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.remove_item('Widget')
        with self.assertRaises(ValueError):
            calc.remove_item('Widget')

    def test_remove_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calc.remove_item('item')

    def test_single_item_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 10.0)

    def test_single_item_with_quantity_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 30.0)

    def test_multiple_items_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 2)
        calc.add_item('Gadget', 5.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 35.0)

    def test_float_precision_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 9.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 29.97, places=2)

    def test_empty_order_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_after_removing_all_items_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.remove_item('Widget')
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.0)

    def test_negative_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_negative_discount_rate(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_string_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_string_discount_rate(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_none_as_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.2)

    def test_none_as_discount_rate(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

    def test_string_input_shipping(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_none_input_shipping(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_list_input_shipping(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping([100.0])

    def test_positive_amount_tax(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_zero_amount_tax(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_small_amount_tax(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023, places=4)

    def test_large_amount_tax(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(10000.0)
        self.assertAlmostEqual(tax, 2300.0)

    def test_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 15.0)

    def test_negative_amount_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_string_amount_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_none_amount_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_list_amount_tax(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax([100.0])

    def test_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0, 2)
        total = calc.calculate_total(0.0)
        expected = (100.0 + 0.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_without_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 150.0)
        total = calc.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        total = calc.calculate_total(0.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_complete_calculation_flow(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 200.0
        discounted = 180.0
        shipping = 0.0
        tax = (180.0 + 0.0) * 0.23
        expected = 180.0 + 0.0 + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 30.0)
        calc.add_item('Gadget', 40.0)
        calc.add_item('Tool', 50.0)
        total = calc.calculate_total(0.0)
        expected = (120.0 + 0.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_discount_explicit(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        total1 = calc.calculate_total(0.0)
        total2 = calc.calculate_total()
        self.assertAlmostEqual(total1, total2)

    def test_empty_order_total(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_full_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0)
        total = calc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_subtotal_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 125.0)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        shipping = 0.0
        expected = (100.0 + 0.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_negative_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_discount_above_one_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_string_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_none_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(None)

    def test_list_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        with self.assertRaises(TypeError):
            calc.calculate_total([0.2])

    def test_empty_order_total_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_single_item_quantity_one_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_single_item_quantity_multiple_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_multiple_items_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 2)
        calc.add_item('Gadget', 15.0, 3)
        calc.add_item('Tool', 20.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_after_merge_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 3)
        calc.add_item('Widget', 10.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_after_removal_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 7)
        calc.add_item('Gadget', 15.0, 3)
        calc.remove_item('Gadget')
        self.assertEqual(calc.total_items(), 7)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_verify_items_gone(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_clear_and_verify_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_empty_order_list_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_single_item_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Widget', items)

    def test_multiple_items_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        calc.add_item('Tool', 15.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Widget', items)
        self.assertIn('Gadget', items)
        self.assertIn('Tool', items)

    def test_no_duplicates_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 3)
        calc.add_item('Widget', 10.0, 2)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Widget', items)

    def test_order_of_names_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_after_removal_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        calc.add_item('Tool', 15.0)
        calc.remove_item('Gadget')
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Widget', items)
        self.assertIn('Tool', items)

    def test_initially_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_after_adding_item_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        self.assertFalse(calc.is_empty())

    def test_after_removing_all_items_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.remove_item('Widget')
        self.assertTrue(calc.is_empty())

    def test_after_clearing_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_multiple_items_present_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        calc.add_item('Gadget', 20.0)
        self.assertFalse(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0, 2)
        calc.add_item('Gadget', 30.0)
        total = calc.calculate_total(0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_remove_add_cycle(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 3)
        calc.remove_item('Widget')
        calc.add_item('Widget', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_multiple_discounts(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 100.0)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.2)
        self.assertNotEqual(total1, total2)

    def test_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 125.0)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        shipping = calc.calculate_shipping(discounted)
        self.assertAlmostEqual(shipping, 0.0)

    def test_tax_calculation_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0)
        total = calc.calculate_total(0.0)
        base = 50.0 + 10.0
        expected = base * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_quantity_accumulation(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 1)
        calc.add_item('Widget', 10.0, 2)
        calc.add_item('Widget', 10.0, 3)
        self.assertEqual(calc.total_items(), 6)

    def test_mixed_operations(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0)
        calc.add_item('C', 30.0)
        calc.add_item('D', 40.0)
        calc.add_item('E', 50.0)
        calc.remove_item('B')
        calc.remove_item('D')
        calc.clear_order()
        calc.add_item('X', 15.0)
        calc.add_item('Y', 25.0)
        calc.add_item('Z', 35.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_free_shipping_qualification(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0)
        self.assertAlmostEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)
        calc.add_item('Gadget', 60.0)
        self.assertAlmostEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)

    def test_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 150.0)
        discounted = calc.apply_discount(150.0, 0.5)
        shipping = calc.calculate_shipping(discounted)
        self.assertAlmostEqual(shipping, 10.0)

    def test_full_workflow_with_custom_params(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item('Widget', 100.0, 2)
        total = calc.calculate_total(0.1)
        discounted = 180.0
        shipping = 15.0
        expected = (180.0 + 15.0) * 1.15
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_order_calculation(self):
        calc = OrderCalculator()
        for i in range(50):
            calc.add_item(f'Item{i}', 10.0 + i, 1)
        total = calc.calculate_total(0.1)
        self.assertGreater(total, 0)

    def test_precision_in_full_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 9.99, 3)
        total = calc.calculate_total(0.15)
        subtotal = 29.97
        discounted = 29.97 * 0.85
        shipping = calc.calculate_shipping(discounted)
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_after_exceptions(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0, 5)
        try:
            calc.add_item('Widget', 20.0)
        except ValueError:
            pass
        self.assertEqual(calc.total_items(), 5)

    def test_remove_and_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0, 2)
        calc.add_item('Gadget', 30.0, 1)
        calc.remove_item('Gadget')
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 100.0)

    def test_zero_total_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 50.0)
        total = calc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_minimal_order(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 0.01, 1)
        total = calc.calculate_total(0.0)
        expected = (0.01 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_maximum_values(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 99999.99, 1000)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_all_edge_combinations(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Widget', 50.0)
        total = calc.calculate_total(1.0)
        self.assertAlmostEqual(total, 0.0)

    def test_return_type_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        result = calc.get_subtotal()
        self.assertIsInstance(result, float)

    def test_return_type_total(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        result = calc.calculate_total()
        self.assertIsInstance(result, float)

    def test_return_type_total_items(self):
        calc = OrderCalculator()
        result = calc.total_items()
        self.assertIsInstance(result, int)

    def test_return_type_is_empty(self):
        calc = OrderCalculator()
        result = calc.is_empty()
        self.assertIsInstance(result, bool)

    def test_return_type_list_items(self):
        calc = OrderCalculator()
        result = calc.list_items()
        self.assertIsInstance(result, list)

    def test_meaningful_error_messages(self):
        calc = OrderCalculator()
        try:
            calc.add_item('', 10.0)
        except ValueError as e:
            self.assertIsInstance(str(e), str)

    def test_exception_on_invalid_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Widget', 10.0)
        try:
            calc.remove_item('Gadget')
        except ValueError as e:
            self.assertIsInstance(str(e), str)

    def test_independent_calculators(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Widget', 10.0)
        self.assertTrue(calc2.is_empty())

    def test_parameter_independence(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)