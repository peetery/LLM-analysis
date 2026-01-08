import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_with_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_subtotal_with_fractional_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 19.99, 1)
        calc.add_item('Item2', 5.5, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 30.99, places=2)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_greater_than_hundred_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 150.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_with_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_total_with_free_shipping_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 184.5, places=2)

    def test_total_with_free_shipping_at_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_total_with_discount_exceeding_hundred_percent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=150.0)

    def test_total_with_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_tax_calculation_base(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected_tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(expected_tax, 23.0, places=2)

    def test_item_count_with_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_item_count_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_item_count_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_item_count_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_list_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        items = calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_after_modifications(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(items, ['Banana'])

    def test_list_return_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        items = calc.list_items()
        self.assertIsInstance(items, list)

    def test_empty_order_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_not_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertFalse(calc.is_empty())

    def test_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_precision_and_rounding(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_very_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_string_instead_of_float_for_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'expensive', 1)

    def test_string_instead_of_int_for_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 'two')

    def test_none_values(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.0, 1)