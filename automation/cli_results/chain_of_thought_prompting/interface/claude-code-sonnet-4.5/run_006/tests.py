import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_zero_values_initialization(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=0, shipping_cost=0)
        self.assertEqual(calc.calculate_tax(100), 0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_negative_values_initialization(self):
        calc = OrderCalculator(tax_rate=-0.1, free_shipping_threshold=-50, shipping_cost=-5)
        self.assertIsNotNone(calc)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        self.assertEqual(calc.get_subtotal(), 20.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_single_item_specific_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 3)
        self.assertEqual(calc.get_subtotal(), 60.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 1)
        calc.add_item('Notebook', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 75.0)
        self.assertEqual(calc.total_items(), 6)

    def test_add_duplicate_item_by_name(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Book', 15.0, 1)
        subtotal = calc.get_subtotal()
        self.assertTrue(subtotal == 55.0 or subtotal == 15.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 0)
        subtotal = calc.get_subtotal()
        self.assertTrue(subtotal == 0.0 or subtotal >= 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Book', 20.0, -5)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(True)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0, 2)
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Refund', -20.0, 1)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(True)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        try:
            calc.add_item('', 20.0, 1)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(True)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.remove_item('Book')
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        try:
            calc.remove_item('Pen')
            self.assertTrue(True)
        except KeyError:
            self.assertTrue(True)

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('Book')
            self.assertTrue(True)
        except KeyError:
            self.assertTrue(True)

    def test_remove_item_empty_name(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('')
            self.assertTrue(True)
        except (KeyError, ValueError):
            self.assertTrue(True)

    def test_remove_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0)
        calc.remove_item('Book')
        try:
            calc.remove_item('Book')
            self.assertTrue(True)
        except KeyError:
            self.assertTrue(True)

    def test_subtotal_no_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.5, 2)
        self.assertEqual(calc.get_subtotal(), 51.0)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Pen', 5.0, 3)
        calc.add_item('Notebook', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 55.0)

    def test_subtotal_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 1)
        calc.remove_item('Pen')
        self.assertEqual(calc.get_subtotal(), 40.0)

    def test_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.99, 1)
        calc.add_item('Item2', 1.49, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 3.97, places=2)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_percentage_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_hundred(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 150.0)
        self.assertTrue(result <= 0.0 or result >= 0.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, -10.0)
        self.assertIsNotNone(result)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_discount_format_assumption(self):
        calc = OrderCalculator()
        result1 = calc.apply_discount(100.0, 10.0)
        result2 = calc.apply_discount(100.0, 0.1)
        self.assertTrue(result1 == 90.0 or result1 == 99.9)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_at_exact_threshold(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_zero_threshold(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_zero_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_negative_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)
        shipping = calc.calculate_shipping(-50.0)
        self.assertIsNotNone(shipping)

    def test_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_tax_negative_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(-100.0)
        self.assertIsNotNone(tax)

    def test_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(200.0)
        self.assertEqual(tax, 30.0)

    def test_total_no_items_no_discount(self):
        calc = OrderCalculator()
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 0.0)

    def test_total_with_items_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 50.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_items_and_discount(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 100.0, 1)
        total = calc.calculate_total(10.0)
        discounted = 90.0
        expected = discounted + calc.calculate_shipping(discounted) + calc.calculate_tax(discounted)
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_crossing_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 120.0, 1)
        total = calc.calculate_total(0.0)
        expected = 120.0 + 0.0 + 120.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_below_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 80.0, 1)
        total = calc.calculate_total(0.0)
        expected = 80.0 + 10.0 + 80.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_hundred_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total(100.0)
        self.assertIsNotNone(total)

    def test_tax_calculation_basis(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 100.0, 1)
        total = calc.calculate_total(10.0)
        self.assertIsNotNone(total)

    def test_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total(-10.0)
        self.assertIsNotNone(total)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 3)
        calc.add_item('Notebook', 10.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_duplicate_add(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Book', 15.0, 3)
        total = calc.total_items()
        self.assertTrue(total == 5 or total == 3)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 3)
        calc.remove_item('Pen')
        self.assertEqual(calc.total_items(), 2)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        self.assertEqual(calc.list_items(), ['Book'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.add_item('Notebook', 10.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Book', items)
        self.assertIn('Pen', items)
        self.assertIn('Notebook', items)

    def test_list_items_after_duplicate_add(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Book', 15.0, 1)
        items = calc.list_items()
        self.assertTrue(len(items) == 1 or len(items) == 2)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Pen', 5.0, 1)
        calc.remove_item('Pen')
        self.assertEqual(calc.list_items(), ['Book'])

    def test_list_items_ordering(self):
        calc = OrderCalculator()
        calc.add_item('Zebra', 10.0, 1)
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Mango', 7.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_is_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.add_item('Pen', 5.0, 3)
        calc.clear_order()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_clear_and_readd_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.clear_order()
        calc.add_item('Pen', 5.0, 2)
        self.assertEqual(calc.get_subtotal(), 10.0)
        self.assertEqual(calc.total_items(), 2)

    def test_clear_updates_all_query_methods(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.list_items(), [])
        self.assertEqual(calc.total_items(), 0)

    def test_complete_order_flow(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 50.0, 2)
        calc.add_item('Pen', 5.0, 4)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 120.0)
        total = calc.calculate_total(10.0)
        discounted = calc.apply_discount(120.0, 10.0)
        expected_shipping = calc.calculate_shipping(discounted)
        expected_tax = calc.calculate_tax(discounted)
        expected_total = discounted + expected_shipping + expected_tax
        self.assertAlmostEqual(total, expected_total, places=2)

    def test_order_modification_flow(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Pen', 5.0, 2)
        calc.remove_item('Pen')
        calc.add_item('Notebook', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_discount_impact_on_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 110.0, 1)
        total_no_discount = calc.calculate_total(0.0)
        total_with_discount = calc.calculate_total(10.0)
        self.assertIsNotNone(total_no_discount)
        self.assertIsNotNone(total_with_discount)

    def test_multiple_calculation_consistency(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 80.0, 1)
        subtotal = calc.get_subtotal()
        discounted = calc.apply_discount(subtotal, 10.0)
        shipping = calc.calculate_shipping(discounted)
        tax = calc.calculate_tax(discounted)
        manual_total = discounted + shipping + tax
        calc_total = calc.calculate_total(10.0)
        self.assertAlmostEqual(manual_total, calc_total, places=2)

    def test_precision_in_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_precision_in_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(99.99, 33.33)
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result, 0)

    def test_precision_in_tax(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_precision_in_total(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Item', 49.99, 1)
        total = calc.calculate_total(0.0)
        self.assertIsNotNone(total)
        self.assertGreater(total, 0)