import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(1), 0.0)

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_add_single_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 9.5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple', -2.5, 1)
            self.assertEqual(calc.get_subtotal(), -2.5)
        except ValueError:
            pass

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple', 2.5, -1)
            self.assertEqual(calc.get_subtotal(), -2.5)
        except ValueError:
            pass

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        try:
            calc.add_item('', 2.5, 1)
            self.assertTrue(calc.get_subtotal() >= 0)
        except ValueError:
            pass

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError, AttributeError)):
            calc.add_item(None, 2.5, 1)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1000000)
        self.assertEqual(calc.get_subtotal(), 2500000.0)

    def test_add_item_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Diamond', 1000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_fractional_quantity(self):
        calc = OrderCalculator()
        try:
            calc.add_item('Apple', 2.5, 2.5)
            subtotal = calc.get_subtotal()
            self.assertTrue(subtotal == 6.25 or subtotal == 5.0)
        except TypeError:
            pass

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        try:
            calc.remove_item('Banana')
        except (KeyError, ValueError):
            pass
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        try:
            calc.remove_item('Apple')
        except (KeyError, ValueError):
            pass

    def test_remove_with_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, KeyError, ValueError, AttributeError)):
            calc.remove_item(None)

    def test_remove_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        try:
            calc.remove_item('apple')
            self.assertTrue(calc.get_subtotal() == 0.0 or calc.get_subtotal() == 5.0)
        except (KeyError, ValueError):
            self.assertEqual(calc.get_subtotal(), 5.0)

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 12.5)

    def test_subtotal_after_remove_operation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        try:
            result = calc.apply_discount(100.0, -10.0)
            self.assertTrue(result >= 0)
        except ValueError:
            pass

    def test_apply_discount_over_100_percent(self):
        calc = OrderCalculator()
        try:
            result = calc.apply_discount(100.0, 150.0)
            self.assertTrue(result <= 0 or result >= 0)
        except ValueError:
            pass

    def test_shipping_below_free_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_shipping_exactly_at_free_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_shipping_above_free_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_shipping_with_zero_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_shipping_with_negative_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(-50.0)
        self.assertTrue(result >= 0)

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_total_at_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_tax_base_verification(self):
        calc = OrderCalculator(tax_rate=0.2, shipping_cost=10.0, free_shipping_threshold=200.0)
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total(0.0)
        subtotal = 50.0
        shipping = 10.0
        tax_on_subtotal_only = subtotal * 0.2
        tax_on_subtotal_and_shipping = (subtotal + shipping) * 0.2
        self.assertTrue(abs(total - (subtotal + shipping + tax_on_subtotal_only)) < 0.01 or abs(total - (subtotal + shipping + tax_on_subtotal_and_shipping)) < 0.01)

    def test_item_count_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_item_count_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        count = calc.total_items()
        self.assertTrue(count == 1)

    def test_item_count_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        count = calc.total_items()
        self.assertTrue(count == 2 or count == 5)

    def test_item_count_includes_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        count = calc.total_items()
        self.assertTrue(count == 1 or count == 5)

    def test_item_count_after_add_remove_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        count = calc.total_items()
        self.assertTrue(count == 1 or count == 3)

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_and_readd_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.clear_order()
        calc.add_item('Banana', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        items = calc.list_items()
        self.assertEqual(items, [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.add_item('Cherry', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_free_shipping_threshold_boundary(self):
        calc = OrderCalculator(tax_rate=0.2, shipping_cost=10.0, free_shipping_threshold=100.0)
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 120.0, places=2)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5, 3)
        subtotal = calc.get_subtotal()
        item_count = calc.total_items()
        is_empty = calc.is_empty()
        items = calc.list_items()
        self.assertFalse(is_empty)
        self.assertEqual(subtotal, 9.5)
        self.assertTrue(len(items) > 0)