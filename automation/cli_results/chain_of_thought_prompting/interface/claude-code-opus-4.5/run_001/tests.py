import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_init_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calc.free_shipping_threshold, 0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0)
        self.assertEqual(calc.shipping_cost, 0)

    def test_init_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.tax_rate, -0.1)

    def test_init_negative_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-50.0)
        self.assertEqual(calc.free_shipping_threshold, -50.0)

    def test_init_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-10.0)
        self.assertEqual(calc.shipping_cost, -10.0)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 2.0, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('InvalidItem', -5.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 1000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Apple', 1.5, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Apple')

    def test_remove_item_updates_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('apple')

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_get_subtotal_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.remove_item('Banana')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(-100.0, 10.0)
        self.assertEqual(result, -90.0)

    def test_apply_discount_floating_point(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 15.5)
        self.assertAlmostEqual(result, 84.49155, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(-50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(-100.0)
        self.assertEqual(result, -23.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(200.0)
        self.assertEqual(result, 46.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 25.0, 2)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 60.0, 2)
        total = calc.calculate_total(0.0)
        expected = 120.0 + 0.0 + 120.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(10.0)
        discounted = 90.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total(0.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total(100.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 4)
        total = calc.calculate_total(50.0)
        discounted = 100.0
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_integration(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 4)
        total = calc.calculate_total(10.0)
        subtotal = 30.0 + 20.0
        discounted = 45.0
        shipping = 5.0
        tax = (discounted + shipping) * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 4)
        self.assertEqual(calc.total_items(), 9)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_state_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_preserves_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(items, ['Apple', 'Banana', 'Orange'])

    def test_list_items_returns_copy(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        items = calc.list_items()
        items.append('Fake')
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_purchase_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 500.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        calc.add_item('Keyboard', 75.0, 1)
        self.assertEqual(calc.get_subtotal(), 625.0)
        self.assertEqual(calc.total_items(), 4)
        total = calc.calculate_total(10.0)
        discounted = 562.5
        shipping = 0.0
        tax = discounted * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_modify_order_and_recalculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 4)
        self.assertEqual(calc.get_subtotal(), 40.0)
        calc.remove_item('Banana')
        self.assertEqual(calc.get_subtotal(), 20.0)
        calc.add_item('Orange', 8.0, 3)
        self.assertEqual(calc.get_subtotal(), 44.0)

    def test_multiple_discounts_in_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(10.0)
        total2 = calc.calculate_total(20.0)
        total3 = calc.calculate_total(0.0)
        self.assertGreater(total3, total1)
        self.assertGreater(total1, total2)

    def test_order_state_persistence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 2)
        calc.calculate_total(5.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(calc.get_subtotal(), 20.0)