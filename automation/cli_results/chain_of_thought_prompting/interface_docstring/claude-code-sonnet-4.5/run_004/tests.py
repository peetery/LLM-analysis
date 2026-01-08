import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_with_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_with_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_with_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_with_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_exceeding_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_with_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_with_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_with_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_same_item_increments_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_with_quantity_one_explicitly(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_with_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5)

    def test_add_item_with_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_with_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -2)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_with_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_with_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10000)
        self.assertEqual(calc.total_items(), 10000)

    def test_add_item_with_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Candy', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_decreases_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_with_multiple_items_present(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Cherry', items)
        self.assertNotIn('Banana', items)

    def test_get_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 5.4)

    def test_get_subtotal_with_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        calc.add_item('Banana', 1.0, 5)
        calc.add_item('Cherry', 3.0, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 13.0)

    def test_get_subtotal_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 3)
        calc.remove_item('Banana')
        self.assertAlmostEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_decimal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.99, 1)
        calc.add_item('Item2', 5.49, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 21.97)

    def test_get_subtotal_updates_dynamically(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        subtotal1 = calc.get_subtotal()
        calc.add_item('Banana', 2.0, 1)
        subtotal2 = calc.get_subtotal()
        self.assertAlmostEqual(subtotal1, 1.0)
        self.assertAlmostEqual(subtotal2, 3.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_exceeding_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_to_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_to_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 0.15)
        self.assertAlmostEqual(result, 84.9915)

    def test_apply_very_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_for_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_with_custom_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 15.0)

    def test_calculate_shipping_with_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_with_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_near_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_with_one_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0)

    def test_calculate_tax_on_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_with_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977)

    def test_calculate_tax_with_small_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.01)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 1.0)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        expected = 100.0 * 0.8 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_above_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_at_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_default_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_one_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_with_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_with_discount_exceeding_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_with_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.2)
        subtotal = 100.0
        discounted = subtotal * 0.8
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_multiple_items_with_discount_and_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 80.0
        discounted = subtotal * 0.9
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_brings_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 110.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 110.0 * 0.8
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_brings_to_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(1.0)
        shipping = 10.0
        taxable = 0.0 + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 60.0, 1)
        total = calc.calculate_total(0.1)
        discounted = 60.0 * 0.9
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.15
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 157.89, 1)
        total = calc.calculate_total(0.15)
        discounted = 157.89 * 0.85
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_very_large_order(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 10000.0, 1)
        total = calc.calculate_total()
        expected = 10000.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_multiple_items_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.8, 5)
        calc.add_item('Cherry', 2.0, 3)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_quantity_aggregation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_and_verify_total_items_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_and_verify_get_subtotal_raises(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_clear_order_and_verify_list_items_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.add_item('Cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.8)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Banana', items)
        self.assertNotIn('Apple', items)

    def test_list_items_exact_names(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.0)
        calc.add_item('Item2', 2.0)
        items = calc.list_items()
        self.assertIn('Item1', items)
        self.assertIn('Item2', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_at_various_workflow_stages(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())
        calc.add_item('Banana', 0.8)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_full_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 40.0
        discounted = subtotal * 0.9
        shipping = 10.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_integration_add_remove_calculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 20.0, 2)
        calc.add_item('Banana', 10.0, 3)
        calc.remove_item('Banana')
        total = calc.calculate_total()
        subtotal = 40.0
        shipping = 10.0
        taxable = subtotal + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_integration_quantity_aggregation_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 25.0)

    def test_integration_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 120.0 * 0.8
        shipping = 0.0
        taxable = discounted + shipping
        tax = taxable * 0.23
        expected = taxable + tax
        self.assertAlmostEqual(total, expected)

    def test_integration_multiple_calculators_independent(self):
        calc1 = OrderCalculator(tax_rate=0.1)
        calc2 = OrderCalculator(tax_rate=0.2)
        calc1.add_item('Item', 100.0)
        calc2.add_item('Item', 100.0)
        total1 = calc1.calculate_total()
        total2 = calc2.calculate_total()
        self.assertAlmostEqual(total1, 110.0)
        self.assertAlmostEqual(total2, 120.0)

    def test_integration_clear_and_reuse(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.clear_order()
        calc.add_item('Banana', 20.0)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 20.0)

    def test_stress_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertAlmostEqual(calc.get_subtotal(), 100.0)

    def test_precision_complex_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 12.345, 3)
        calc.add_item('Item2', 67.89, 2)
        subtotal = calc.get_subtotal()
        expected = 12.345 * 3 + 67.89 * 2
        self.assertAlmostEqual(subtotal, expected, places=2)

    def test_edge_case_special_characters_in_name(self):
        calc = OrderCalculator()
        calc.add_item('Item-1', 5.0)
        calc.add_item('Item_2', 10.0)
        calc.add_item('Item (3)', 15.0)
        items = calc.list_items()
        self.assertIn('Item-1', items)
        self.assertIn('Item_2', items)
        self.assertIn('Item (3)', items)

    def test_edge_case_extreme_price_range(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1)
        calc.add_item('Expensive', 10000.0, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 10000.01, places=2)