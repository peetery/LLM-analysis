import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertTrue(calc.is_empty())

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=150.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100.0), 15.0)
        self.assertEqual(calc.calculate_shipping(100.0), 15.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_edge_case_initialization_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_invalid_initialization_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_invalid_initialization_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_invalid_initialization_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100.0)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        calc.add_item('Cherry', 7.0, 1)
        self.assertEqual(len(calc.list_items()), 3)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_add_item_with_fractional_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 9.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 9.99, places=2)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99, places=2)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1000)
        self.assertEqual(calc.get_subtotal(), 10000.0)
        self.assertEqual(calc.total_items(), 1000)

    def test_invalid_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_invalid_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item(None, 10.0, 1)

    def test_invalid_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -10.0, 1)

    def test_invalid_add_item_none_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', None, 1)

    def test_invalid_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -5)

    def test_invalid_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_invalid_add_item_none_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, None)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.add_item('Cherry', 7.0)
        calc.remove_item('Banana')
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Cherry', items)
        self.assertNotIn('Banana', items)

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Apple')

    def test_remove_already_removed_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.remove_item('Apple')
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Apple')

    def test_invalid_remove_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_invalid_remove_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.remove_item(None)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('apple')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 3)
        calc.add_item('Item3', 7.0, 1)
        self.assertEqual(calc.get_subtotal(), 42.0)

    def test_get_subtotal_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 3)
        calc.remove_item('Item2')
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_with_fractional_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 9.99, 1)
        calc.add_item('Item2', 3.49, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 13.48, places=2)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_invalid_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_invalid_apply_discount_over_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_discount_on_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 10.0)

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

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 15.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_calculate_tax_fractional_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(9.99)
        self.assertAlmostEqual(result, 2.2977, places=4)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
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

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 3)
        calc.add_item('Item3', 7.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 5)
        calc.add_item('Item2', 5.0, 3)
        calc.remove_item('Item2')
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_populated(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_resets_item_list(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 5.0)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_clear_order_resets_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 10)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_preserves_configuration(self):
        calc = OrderCalculator(tax_rate=0.15, shipping_cost=15.0)
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertEqual(calc.calculate_tax(100.0), 15.0)
        self.assertEqual(calc.calculate_shipping(50.0), 15.0)

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
        calc.add_item('Cherry', 7.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertTrue(all((isinstance(item, str) for item in items)))

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        calc.add_item('Banana', 3.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(items, ['Banana'])

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_and_removing_all(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_very_large_order(self):
        calc = OrderCalculator()
        for i in range(1000):
            calc.add_item(f'Item{i}', 10.0, 1)
        self.assertEqual(calc.total_items(), 1000)
        self.assertEqual(calc.get_subtotal(), 10000.0)

    def test_alternating_add_remove_operations(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.add_item('Item2', 20.0)
        calc.remove_item('Item1')
        calc.add_item('Item3', 30.0)
        calc.remove_item('Item2')
        self.assertEqual(len(calc.list_items()), 1)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_type_validation_price_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0', 1)

    def test_type_validation_quantity_as_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 1.5)

    def test_type_validation_discount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '10')