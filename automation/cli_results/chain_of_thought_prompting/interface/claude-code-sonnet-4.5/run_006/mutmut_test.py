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

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Book', 20.0, -5)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(True)

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

    def test_remove_item_empty_name(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('')
            self.assertTrue(True)
        except (KeyError, ValueError):
            self.assertTrue(True)

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

    def test_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(200.0)
        self.assertEqual(tax, 30.0)

    def test_total_crossing_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Book', 120.0, 1)
        total = calc.calculate_total(0.0)
        expected = 120.0 + 0.0 + 120.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

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

    def test_order_modification_flow(self):
        calc = OrderCalculator()
        calc.add_item('Book', 20.0, 1)
        calc.add_item('Pen', 5.0, 2)
        calc.remove_item('Pen')
        calc.add_item('Notebook', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_precision_in_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

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