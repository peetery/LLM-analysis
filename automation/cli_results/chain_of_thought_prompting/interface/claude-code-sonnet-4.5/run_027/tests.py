import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_invalid_type_for_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_duplicate_item_name(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Book', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_with_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Luxury Item', 999999.99)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 20.0, 0)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', -20.0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 20.0, -1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 20.0)

    def test_add_item_with_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 20.0)

    def test_add_item_with_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 20.0)

    def test_add_item_with_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Book', 'twenty')

    def test_add_item_with_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Book', 20.0, 'two')

    def test_add_item_with_fractional_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Book', 20.0, 1.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_remove_item_from_order_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.remove_item('Book')
        self.assertEqual(len(calc.list_items()), 1)
        self.assertIn('Pen', calc.list_items())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Pen')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('Book')

    def test_remove_item_with_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError)):
            calc.remove_item('')

    def test_remove_item_with_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.remove_item('Book')
        calc.remove_item('Pen')
        self.assertTrue(calc.is_empty())

    def test_subtotal_of_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 55.0)

    def test_subtotal_with_item_of_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Book', 15.0, 4)
        self.assertEqual(calc.get_subtotal(), 60.0)

    def test_subtotal_after_adding_and_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.remove_item('Pen')
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_subtotal_with_zero_price_items(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 5)
        calc.add_item('Book', 20.0)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=2)

    def test_apply_percentage_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_absolute_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 25.0)
        self.assertEqual(result, 75.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(50.0, 75.0)
        self.assertLessEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertLessEqual(result, 0.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_very_large_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1000000.0)
        self.assertLessEqual(result, 0.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_at_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_for_zero_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_with_negative_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(-10.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(-100.0)
        self.assertAlmostEqual(tax, -23.0, places=2)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(10.5)
        self.assertAlmostEqual(tax, 2.415, places=2)

    def test_total_with_no_discount_below_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_no_discount_above_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 150.0)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 80.0)
        total = calc.calculate_total(discount=10.0)
        expected = (70.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 150.0)
        total = calc.calculate_total(discount=20.0)
        expected = 130.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_for_empty_order(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0)
        total = calc.calculate_total()
        self.assertGreaterEqual(total, 0.0)

    def test_total_with_zero_discount_parameter(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0)
        total1 = calc.calculate_total(0.0)
        total2 = calc.calculate_total()
        self.assertEqual(total1, total2)

    def test_total_calculation_order(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 80.0)
        total = calc.calculate_total(discount=10.0)
        discounted = 70.0
        with_shipping = 80.0
        expected = with_shipping * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_after_modifying_order(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Pen', 10.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_total_with_all_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 0.0)

    def test_total_with_custom_tax_rate_and_shipping(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Book', 30.0)
        total = calc.calculate_total()
        expected = (30.0 + 5.0) * 1.15
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item_quantity_1(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_quantity_greater_than_1(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 3)
        calc.add_item('Pen', 5.0, 2)
        calc.remove_item('Pen')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_re_add_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.clear_order()
        calc.add_item('Pen', 5.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_list_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Book', items)

    def test_list_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Book', items)
        self.assertIn('Pen', items)

    def test_list_items_order(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.add_item('Notebook', 10.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_modifications(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.add_item('Pen', 5.0)
        calc.remove_item('Book')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Pen', items)

    def test_is_empty_for_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0, 2)
        calc.add_item('Pen', 5.0, 4)
        total = calc.calculate_total(discount=20.0)
        subtotal = 120.0
        discounted = 100.0
        with_shipping = 100.0
        expected = 100.0 * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_modification_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0, 2)
        total1 = calc.calculate_total()
        calc.remove_item('Book')
        calc.add_item('Pen', 30.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_discount_pushing_below_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 110.0)
        total = calc.calculate_total(discount=15.0)
        discounted = 95.0
        with_shipping = 105.0
        expected = 105.0 * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_orders_with_same_calculator_instance(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        total1 = calc.calculate_total()
        calc.clear_order()
        calc.add_item('Pen', 5.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_floating_point_precision_across_calculations(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_very_large_order(self):
        calc = OrderCalculator(tax_rate=0.2)
        calc.add_item('Item1', 1000.0, 100)
        calc.add_item('Item2', 500.0, 50)
        total = calc.calculate_total()
        self.assertGreater(total, 100000.0)

    def test_tax_calculation_base(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 50.0)
        total = calc.calculate_total()
        expected_base = 60.0
        expected_total = 72.0
        self.assertAlmostEqual(total, expected_total, places=2)

    def test_free_shipping_with_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Book', 80.0)
        total_no_discount = calc.calculate_total()
        total_with_discount = calc.calculate_total(discount=5.0)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_duplicate_item_handling(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Book', 20.0, 3)
        self.assertGreaterEqual(calc.total_items(), 2)

    def test_remove_item_that_was_added_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Book', 20.0, 3)
        initial_count = calc.total_items()
        calc.remove_item('Book')
        self.assertLess(calc.total_items(), initial_count)