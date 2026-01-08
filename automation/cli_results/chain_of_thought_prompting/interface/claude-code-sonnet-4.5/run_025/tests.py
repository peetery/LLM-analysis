import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100.0), 15.0)
        self.assertEqual(calc.calculate_shipping(150.0), 15.0)
        self.assertEqual(calc.calculate_shipping(200.0), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100.0)

    def test_add_item_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 1.0)

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_add_item_same_name_accumulates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item(None, 1.0)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_floating_point_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 19.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99, places=2)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01, places=2)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('NonExistent')

    def test_remove_item_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_partial_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(KeyError):
            calc.remove_item('apple')

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 7.5, places=2)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 8.0, places=2)

    def test_get_subtotal_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertAlmostEqual(calc.get_subtotal(), 6.0, places=2)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_percentage(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(result, 90.0, places=2)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0, places=2)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_apply_discount_over_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 0.15)
        self.assertAlmostEqual(result, 84.9915, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_normal(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 10.0, places=2)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.1)
        discounted = 90.0
        shipping = 0.0
        tax = 90.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_qualified(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        shipping = 0.0
        tax = 150.0 * 0.23
        expected = 150.0 + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        shipping = 10.0
        tax = 60.0 * 0.23
        expected = 50.0 + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_integration(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 80.0
        discounted = 72.0
        shipping = 10.0
        tax = 82.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(1.0)
        shipping = 10.0
        tax = 10.0 * 0.23
        expected = 0.0 + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_calls_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.1)
        self.assertEqual(total1, total2)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 2.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_subtotal_reset(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_order_total_reset(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.clear_order()
        self.assertEqual(calc.calculate_total(), 0.0)

    def test_clear_order_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_add_and_remove_same(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_order_flow(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 800.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 850.0
        discounted = 765.0
        shipping = 0.0
        tax = 765.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_modify_order_recalculate(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        total1 = calc.calculate_total()
        calc.add_item('Item2', 60.0, 1)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)
        self.assertGreater(total2, total1)

    def test_shipping_threshold_boundary_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        shipping = 10.0
        tax = 106.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_calculation_includes_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        shipping = 10.0
        base = 50.0 + shipping
        tax = base * 0.23
        expected = base + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_precision_across_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 33.33, 3)
        calc.add_item('Item2', 66.66, 2)
        total = calc.calculate_total(0.15)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)