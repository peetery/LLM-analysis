import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_with_zero_values(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=0, shipping_cost=0)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 0)
        self.assertEqual(calc.shipping_cost, 0)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_specified_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Orange', 1.5, 1)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_duplicate_item_same_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_add_item_with_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.0, 1)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_with_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01, places=2)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_remove_item_then_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertIn('Apple', calc.list_items())
        self.assertEqual(calc.total_items(), 3)

    def test_remove_with_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, TypeError)):
            calc.remove_item(None)

    def test_get_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_get_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 8.5)

    def test_get_subtotal_with_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 3.0, 4)
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_get_subtotal_with_floating_point_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 10.0, places=2)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_ten_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_very_small(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0001)
        self.assertAlmostEqual(result, 99.99, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_exact_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_for_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_with_negative_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(-50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 15.0)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_on_very_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(1000000.0)
        self.assertEqual(tax, 230000.0)

    def test_calculate_total_no_discount_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 30.0, 2)
        calc.add_item('Banana', 20.0, 1)
        total = calc.calculate_total()
        subtotal = 80.0
        shipping = 10.0
        taxable = 90.0
        tax = 90.0 * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 120.0, 1)
        total = calc.calculate_total()
        subtotal = 120.0
        shipping = 0.0
        tax = 120.0 * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_paid_shipping_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Cheap Item', 50.0, 1)
        total = calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        taxable = 60.0
        tax = 60.0 * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(discount=1.0)
        subtotal = 0.0
        shipping = 10.0
        taxable = 10.0
        tax = 10.0 * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_free_shipping_boundary_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total = calc.calculate_total(discount=0.1)
        subtotal = 110.0
        discounted = 99.0
        shipping = 10.0
        taxable = 109.0
        tax = 109.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_very_small_amounts(self):
        calc = OrderCalculator()
        calc.add_item('Tiny Item', 0.01, 1)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_total_items_with_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Orange', 1.5, 4)
        self.assertEqual(calc.total_items(), 9)

    def test_total_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_add_then_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_add_new_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        calc.add_item('Banana', 0.5, 3)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 3)

    def test_list_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 2)
        calc.add_item('Orange', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_from_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 2)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_on_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_complete_checkout_flow(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 1)
        total = calc.calculate_total(discount=0.1)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    def test_integration_discount_affecting_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0, 1)
        total = calc.calculate_total(discount=0.15)
        subtotal = 110.0
        discounted = 93.5
        shipping = 10.0
        self.assertGreater(total, discounted)

    def test_integration_multiple_add_remove_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 2)
        calc.add_item('Item3', 30.0, 1)
        calc.remove_item('Item2')
        calc.add_item('Item4', 15.0, 3)
        calc.add_item('Item5', 25.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 4)
        self.assertIn('Item1', items)
        self.assertNotIn('Item2', items)

    def test_integration_floating_point_precision_in_complex_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 3)
        calc.add_item('Item2', 0.01, 5)
        calc.add_item('Item3', 19.95, 2)
        total = calc.calculate_total(discount=0.05)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)