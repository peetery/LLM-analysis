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

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item', 100.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        calc.add_item('Item', 10.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Item', 10.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.add_item('Orange', 4.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0)

    def test_add_item_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 5.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('FreeItem', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 5.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 5.0, -1)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 5.0, 2.5)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_special_characters_in_name(self):
        calc = OrderCalculator()
        calc.add_item('Ăśpfel™', 5.0)
        self.assertIn('Ăśpfel™', calc.list_items())

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.remove_item('Apple')
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        with self.assertRaises(KeyError):
            calc.remove_item('apple')

    def test_remove_item_then_readd(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.remove_item('Apple')
        calc.add_item('Apple', 6.0)
        self.assertIn('Apple', calc.list_items())

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 4)
        self.assertEqual(calc.get_subtotal(), 22.0)

    def test_get_subtotal_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 4)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 12.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        calc.add_item('Item2', 0.2, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.9, places=10)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_valid_percentage(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 10.0), 90.0)
        self.assertEqual(calc.apply_discount(100.0, 25.0), 75.0)
        self.assertEqual(calc.apply_discount(100.0, 50.0), 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 110.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 10.0)

    def test_apply_discount_floating_point(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 12.5)
        self.assertEqual(result, 87.5)

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

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        result = calc.calculate_total()
        self.assertEqual(result, 10.0)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        result = calc.calculate_total()
        expected = 50.0 + 50.0 * 0.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_multiple_items_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0)
        calc.add_item('Item2', 40.0)
        result = calc.calculate_total()
        subtotal = 70.0
        expected = subtotal + subtotal * 0.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        result = calc.calculate_total(discount=20.0)
        discounted = 64.0
        expected = discounted + discounted * 0.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0)
        result = calc.calculate_total(discount=10.0)
        discounted = 135.0
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_discount_pushes_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 110.0)
        result = calc.calculate_total(discount=20.0)
        discounted = 88.0
        expected = discounted + discounted * 0.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        result = calc.calculate_total(discount=100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_total_invalid_discount_negative(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 5.0, 2)
        calc.add_item('Item2', 3.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 5.0, 2)
        calc.add_item('Item2', 3.0, 3)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 5.0)
        calc.add_item('Item2', 3.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_state_after(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.add_item('Orange', 4.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.add_item('Orange', 4.0)
        items = calc.list_items()
        self.assertEqual(items, ['Apple', 'Banana', 'Orange'])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 500.0, 1)
        calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(calc.get_subtotal(), 550.0)
        total = calc.calculate_total(discount=10.0)
        discounted = 495.0
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_add_and_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        self.assertFalse(calc.is_empty())
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())
        calc.add_item('Item', 15.0)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_integration_multiple_discount_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        subtotal = calc.get_subtotal()
        discounted1 = calc.apply_discount(subtotal, 10.0)
        discounted2 = calc.apply_discount(subtotal, 20.0)
        self.assertEqual(discounted1, 90.0)
        self.assertEqual(discounted2, 80.0)

    def test_integration_threshold_boundary_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)
        discounted = calc.apply_discount(125.0, 20.0)
        self.assertEqual(discounted, 100.0)
        self.assertEqual(calc.calculate_shipping(discounted), 0.0)

    def test_integration_order_state_persistence(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 20.0, 1)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 40.0)
        calc.remove_item('A')
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 20.0)
        calc.add_item('C', 30.0, 3)
        self.assertEqual(calc.total_items(), 4)
        self.assertEqual(calc.get_subtotal(), 110.0)

    def test_integration_concurrent_like_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        calc.add_item('Item2', 20.0, 3)
        calc.add_item('Item3', 15.0, 2)
        calc.remove_item('Item2')
        total1 = calc.calculate_total(discount=5.0)
        calc.add_item('Item4', 25.0, 1)
        total2 = calc.calculate_total(discount=5.0)
        self.assertGreater(total2, total1)