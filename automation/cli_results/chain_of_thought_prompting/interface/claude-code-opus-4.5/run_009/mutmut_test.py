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
        calc.add_item('item', 100.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
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

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('apple', calc.list_items())

    def test_add_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.add_item('cherry', 2.0)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 2)
        calc.add_item('apple', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('item', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('item', 5.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('item', 5.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('expensive', 10000000000.0)
        self.assertEqual(calc.get_subtotal(), 10000000000.0)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('many', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.remove_item('apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        with self.assertRaises(ValueError):
            calc.remove_item('banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_then_readd(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.remove_item('apple')
        calc.add_item('apple', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.remove_item('apple')
        self.assertNotIn('apple', calc.list_items())
        self.assertIn('banana', calc.list_items())

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 2)
        calc.add_item('banana', 3.0, 3)
        self.assertEqual(calc.get_subtotal(), 19.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('item1', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=10)

    def test_get_subtotal_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.remove_item('apple')
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 110.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(-50.0), 10.0)

    def test_calculate_shipping_custom_threshold_below(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(30.0), 5.0)

    def test_calculate_shipping_custom_threshold_above(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('item', 50.0)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('item', 150.0)
        total = calc.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_invalid_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10.0)

    def test_calculate_total_invalid_over_hundred_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(110.0)

    def test_calculate_total_precision(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('item', 33.33)
        total = calc.calculate_total(0.0)
        expected = (33.33 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 2)
        calc.add_item('banana', 3.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 2)
        calc.add_item('banana', 3.0, 3)
        calc.remove_item('apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_then_add_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.clear_order()
        calc.add_item('banana', 3.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('banana', calc.list_items())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        self.assertEqual(calc.list_items(), ['apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.add_item('cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('apple', items)
        self.assertIn('banana', items)
        self.assertIn('cherry', items)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.remove_item('apple')
        self.assertNotIn('apple', calc.list_items())

    def test_list_items_returns_copy(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        items = calc.list_items()
        items.append('banana')
        self.assertNotIn('banana', calc.list_items())

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0)
        calc.add_item('banana', 3.0)
        calc.remove_item('apple')
        calc.remove_item('banana')
        self.assertTrue(calc.is_empty())

    def test_order_modification_workflow(self):
        calc = OrderCalculator()
        calc.add_item('apple', 5.0, 3)
        calc.add_item('banana', 3.0, 2)
        self.assertEqual(calc.get_subtotal(), 21.0)
        calc.remove_item('apple')
        self.assertEqual(calc.get_subtotal(), 6.0)
        calc.add_item('cherry', 4.0, 2)
        self.assertEqual(calc.get_subtotal(), 14.0)

    def test_multiple_orders_independence(self):
        calc1 = OrderCalculator(tax_rate=0.1)
        calc2 = OrderCalculator(tax_rate=0.2)
        calc1.add_item('item1', 100.0)
        calc2.add_item('item2', 200.0)
        self.assertEqual(calc1.get_subtotal(), 100.0)
        self.assertEqual(calc2.get_subtotal(), 200.0)
        self.assertEqual(calc1.calculate_tax(100.0), 10.0)
        self.assertEqual(calc2.calculate_tax(100.0), 20.0)

    def test_recalculation_after_modification(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('item', 50.0)
        total1 = calc.calculate_total(0.0)
        calc.add_item('item2', 60.0)
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)
        expected1 = (50.0 + 10.0) * 1.23
        expected2 = 110.0 * 1.23
        self.assertAlmostEqual(total1, expected1, places=2)
        self.assertAlmostEqual(total2, expected2, places=2)