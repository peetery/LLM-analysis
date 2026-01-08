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

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_high_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=10000.0)
        self.assertEqual(calc.calculate_shipping(5000), 10.0)
        self.assertEqual(calc.calculate_shipping(10000), 0.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.get_subtotal(), 5.25)

    def test_add_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_with_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 999999.99, 1)
        self.assertEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Grain', 0.01, 100000)
        self.assertEqual(calc.get_subtotal(), 1000.0)

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_subtotal_after_item_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 4)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_apply_percentage_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_100_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_100_percent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_shipping_for_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_shipping_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_tax_with_high_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.5)
        self.assertEqual(calc.calculate_tax(100.0), 50.0)

    def test_total_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_below_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 50.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_above_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 110.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 88.0
        expected = 88.0 + 10.0 + 98.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_100_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_calculation_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 100.0
        after_discount = 90.0
        shipping = 10.0
        before_tax = 100.0
        tax = 23.0
        expected = 123.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.get_subtotal(), 2.25)

    def test_list_items_in_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', calc.list_items())
        self.assertEqual(len(calc.list_items()), 1)

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.75, 3)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_flow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        calc.add_item('Banana', 25.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 125.0)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = 123.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_free_shipping_boundary(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Apple', 99.99, 1)
        total_below = calc.calculate_total()
        self.assertGreater(total_below, 99.99)
        calc.clear_order()
        calc.add_item('Apple', 100.0, 1)
        total_at = calc.calculate_total()
        expected_at = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total_at, expected_at, places=2)

    def test_multiple_operations_sequence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.total_items(), 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())

    def test_discount_impact_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 110.0, 1)
        total_no_discount = calc.calculate_total(0.0)
        shipping_no_discount = calc.calculate_shipping(110.0)
        self.assertEqual(shipping_no_discount, 0.0)
        total_with_discount = calc.calculate_total(0.2)
        discounted_subtotal = 88.0
        shipping_with_discount = calc.calculate_shipping(88.0)
        self.assertEqual(shipping_with_discount, 10.0)

    def test_tax_calculation_on_final_amount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 100.0
        after_discount = 90.0
        shipping = 10.0
        before_tax = 100.0
        tax = calc.calculate_tax(before_tax)
        self.assertEqual(tax, 23.0)
        expected_total = before_tax + tax
        self.assertAlmostEqual(total, expected_total, places=2)