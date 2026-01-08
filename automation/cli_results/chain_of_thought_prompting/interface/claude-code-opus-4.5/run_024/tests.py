import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(100), 10.0)

    def test_init_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)
        self.assertEqual(calc.calculate_shipping(49), 10.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(50), 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(49), 5.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calc.calculate_shipping(0), 0.0)
        self.assertEqual(calc.calculate_shipping(0.01), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_negative_tax_rate(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.calculate_tax(100), -10.0)

    def test_init_negative_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=-10)
        self.assertEqual(calc.calculate_shipping(0), 0.0)

    def test_init_negative_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=-5)
        self.assertEqual(calc.calculate_shipping(50), -5.0)

    def test_add_item_single_with_defaults(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_add_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_same_name_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('FreeItem', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadItem', -5.0)

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
            calc.add_item('', 1.5)

    def test_add_item_whitespace_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999999.99)
        self.assertEqual(calc.get_subtotal(), 999999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, TypeError)):
            calc.add_item(123, 1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_remove_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('')

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertNotIn('Banana', items)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(calc.get_subtotal(), 6.5)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1)
        calc.add_item('Item2', 0.2)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_ten_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10)
        self.assertEqual(result, 90.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 50)
        self.assertEqual(result, 0.0)

    def test_apply_discount_small_decimal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 5.5)
        self.assertAlmostEqual(result, 94.5, places=2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.calculate_shipping(49.0), 10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(-100.0), -23.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(200.0), 46.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.08)
        self.assertEqual(calc.calculate_tax(100.0), 8.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(discount=10)
        expected = (90.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_paid_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=100)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        total = calc.calculate_total(discount=10)
        discounted = 80.0 * 0.9
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 40.0)
        total = calc.calculate_total(discount=10)
        discounted = 40.0 * 0.9
        shipping = 5.0
        expected = (discounted + shipping) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_qty_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_qty_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)
        self.assertEqual(len(items), 3)

    def test_list_items_order_preservation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(items[0], 'Apple')
        self.assertEqual(items[1], 'Banana')
        self.assertEqual(items[2], 'Cherry')

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())

    def test_is_empty_on_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 500.0)
        calc.add_item('Mouse', 25.0)
        calc.add_item('Keyboard', 75.0, 2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 675.0)
        discounted = calc.apply_discount(subtotal, 10)
        self.assertEqual(discounted, 607.5)
        shipping = calc.calculate_shipping(discounted)
        self.assertEqual(shipping, 0.0)
        total = calc.calculate_total(discount=10)
        expected = 607.5 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_and_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_multiple_discounts_not_compound(self):
        calc = OrderCalculator()
        subtotal = 100.0
        discounted1 = calc.apply_discount(subtotal, 10)
        discounted2 = calc.apply_discount(subtotal, 10)
        self.assertEqual(discounted1, discounted2)
        self.assertEqual(discounted1, 90.0)

    def test_recalculate_after_modification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 60.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)
        self.assertGreater(total2, total1)

    def test_threshold_boundary_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0)
        shipping_before = calc.calculate_shipping(110.0)
        self.assertEqual(shipping_before, 0.0)
        discounted = calc.apply_discount(110.0, 20)
        self.assertEqual(discounted, 88.0)
        shipping_after = calc.calculate_shipping(discounted)
        self.assertEqual(shipping_after, 10.0)