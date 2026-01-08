import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_init_custom_free_shipping_threshold(self):
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
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_single_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Luxury Item', 10000.0)
        self.assertEqual(calc.get_subtotal(), 10000.0)

    def test_add_item_high_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, 1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_quantity_one_explicit(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01)
        self.assertEqual(calc.get_subtotal(), 0.01)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Free Item', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Negative Item', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'expensive')

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_verify_order_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_remove_item_from_single_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_remove_item_from_multi_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.list_items()), 2)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.get_subtotal(), 3.5)

    def test_get_subtotal_items_with_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 2.0, 2)
        self.assertEqual(calc.get_subtotal(), 8.5)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_get_subtotal_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=25.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 25.0)

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_default_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(200.0)
        self.assertEqual(result, 46.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_floating_point_precision(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Expensive Item', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_not_qualifying_for_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Cheap Item', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_exact_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_calculate_total_discount_exceeding_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=100.0)

    def test_calculate_total_all_custom_params(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 40.0)
        total = calc.calculate_total()
        expected = (40.0 + 5.0) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_single_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 2.0, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_populated_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertTrue(all((isinstance(item, str) for item in items)))

    def test_list_items_after_removing_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
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
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_integration_add_remove_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.add_item('Banana', 5.0, 10)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_clear_and_add_new(self):
        calc = OrderCalculator()
        calc.add_item('OldItem', 100.0)
        calc.clear_order()
        calc.add_item('NewItem', 200.0)
        self.assertEqual(calc.get_subtotal(), 200.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('NewItem', calc.list_items())

    def test_integration_multiple_operations_consistent_state(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 120.0)
        calc.remove_item('Item1')
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 60.0)
        calc.add_item('Item3', 50.0)
        self.assertEqual(calc.total_items(), 4)
        self.assertEqual(calc.get_subtotal(), 110.0)

    def test_integration_many_items_stress_test(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)