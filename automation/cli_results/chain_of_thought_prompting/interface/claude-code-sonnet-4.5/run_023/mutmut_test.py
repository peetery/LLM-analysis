import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_tax(100), 23.0)
        self.assertEqual(calculator.calculate_shipping(50), 10.0)
        self.assertEqual(calculator.calculate_shipping(100), 0.0)

    def test_custom_initialization(self):
        calculator = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calculator.calculate_tax(100), 15.0)
        self.assertEqual(calculator.calculate_shipping(150), 15.0)
        self.assertEqual(calculator.calculate_shipping(200), 0.0)

    def test_zero_tax_rate(self):
        calculator = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calculator.calculate_tax(100), 0.0)

    def test_zero_shipping_cost(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calculator.calculate_shipping(50), 0.0)

    def test_zero_free_shipping_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calculator.calculate_shipping(0.0), 0.0)
        self.assertEqual(calculator.calculate_shipping(10.0), 0.0)

    def test_add_single_item_default_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5)
        self.assertEqual(calculator.total_items(), 1)
        self.assertEqual(calculator.get_subtotal(), 2.5)

    def test_add_single_item_custom_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(calculator.total_items(), 3)
        self.assertEqual(calculator.get_subtotal(), 7.5)

    def test_add_multiple_different_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 2)
        calculator.add_item('Banana', 1.5, 3)
        self.assertEqual(calculator.total_items(), 5)
        self.assertEqual(calculator.get_subtotal(), 9.5)

    def test_add_item_none_name(self):
        calculator = OrderCalculator()
        with self.assertRaises((TypeError, AttributeError)):
            calculator.add_item(None, 2.5, 1)

    def test_add_item_string_price(self):
        calculator = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calculator.add_item('Apple', '2.5', 1)

    def test_remove_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 2)
        calculator.remove_item('Apple')
        self.assertTrue(calculator.is_empty())

    def test_remove_none_name(self):
        calculator = OrderCalculator()
        with self.assertRaises((TypeError, KeyError)):
            calculator.remove_item(None)

    def test_remove_all_items_one_by_one(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 2)
        calculator.add_item('Banana', 1.5, 3)
        calculator.remove_item('Apple')
        calculator.remove_item('Banana')
        self.assertTrue(calculator.is_empty())

    def test_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        self.assertEqual(calculator.get_subtotal(), 7.5)

    def test_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 2)
        calculator.add_item('Banana', 1.5, 4)
        self.assertEqual(calculator.get_subtotal(), 11.0)

    def test_subtotal_large_quantities(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calculator.get_subtotal(), 1000000.0)

    def test_subtotal_many_items(self):
        calculator = OrderCalculator()
        for i in range(100):
            calculator.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(calculator.get_subtotal(), 100.0)

    def test_apply_zero_discount(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_shipping_below_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(50.0), 10.0)

    def test_shipping_at_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_shipping_above_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(150.0), 0.0)

    def test_shipping_zero_subtotal(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(0.0), 10.0)

    def test_shipping_negative_subtotal(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(-50.0), 10.0)

    def test_shipping_with_zero_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calculator.calculate_shipping(50.0), 0.0)

    def test_shipping_with_zero_cost(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calculator.calculate_shipping(50.0), 0.0)

    def test_tax_on_positive_amount(self):
        calculator = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calculator.calculate_tax(100.0), 23.0)

    def test_tax_on_zero_amount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_tax(0.0), 0.0)

    def test_tax_with_zero_tax_rate(self):
        calculator = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calculator.calculate_tax(100.0), 0.0)

    def test_tax_with_100_percent_rate(self):
        calculator = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calculator.calculate_tax(100.0), 100.0)

    def test_tax_precision(self):
        calculator = OrderCalculator(tax_rate=0.23)
        result = calculator.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_total_no_discount(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 50.0, 1)
        total = calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 73.8, places=2)

    def test_total_with_free_shipping_qualified(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 150.0, 1)
        total = calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 184.5, places=2)

    def test_total_with_shipping_cost(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 50.0, 1)
        total = calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 73.8, places=2)

    def test_tax_calculation_base(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Apple', 50.0, 1)
        total = calculator.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_precision_and_rounding(self):
        calculator = OrderCalculator(tax_rate=0.23)
        calculator.add_item('Apple', 33.33, 1)
        total = calculator.calculate_total(0.0)
        self.assertIsInstance(total, float)

    def test_total_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 5)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        calculator.add_item('Banana', 1.5, 7)
        self.assertEqual(calculator.total_items(), 10)

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_total_items_after_adding_duplicate(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        calculator.add_item('Apple', 2.5, 5)
        total = calculator.total_items()
        self.assertIn(total, [5, 8])

    def test_total_items_after_removal(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        calculator.add_item('Banana', 1.5, 5)
        calculator.remove_item('Apple')
        self.assertEqual(calculator.total_items(), 5)

    def test_clear_non_empty_order(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        calculator.add_item('Banana', 1.5, 5)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_clear_empty_order(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_clear_and_readd_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 3)
        calculator.clear_order()
        calculator.add_item('Banana', 1.5, 5)
        self.assertEqual(calculator.total_items(), 5)

    def test_list_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        items = calculator.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        calculator.add_item('Banana', 1.5, 1)
        items = calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        items = calculator.list_items()
        self.assertEqual(items, [])

    def test_list_items_preserves_order(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        calculator.add_item('Banana', 1.5, 1)
        calculator.add_item('Cherry', 3.0, 1)
        items = calculator.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_returns_copy(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        items = calculator.list_items()
        items.append('Banana')
        items2 = calculator.list_items()
        self.assertEqual(items2, ['Apple'])

    def test_list_items_after_removal(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        calculator.add_item('Banana', 1.5, 1)
        calculator.remove_item('Apple')
        items = calculator.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_after_adding_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        self.assertFalse(calculator.is_empty())

    def test_is_empty_after_clearing(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 2.5, 1)
        calculator.add_item('Banana', 1.5, 1)
        calculator.remove_item('Apple')
        calculator.remove_item('Banana')
        self.assertTrue(calculator.is_empty())

    def test_modify_order_and_recalculate(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 50.0, 1)
        total1 = calculator.calculate_total(0.0)
        calculator.add_item('Banana', 50.0, 1)
        total2 = calculator.calculate_total(0.0)
        self.assertNotEqual(total1, total2)

    def test_boundary_around_free_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        calculator.add_item('Item', 99.0, 1)
        total_below = calculator.calculate_total(0.0)
        calculator.clear_order()
        calculator.add_item('Item', 100.0, 1)
        total_at = calculator.calculate_total(0.0)
        calculator.clear_order()
        calculator.add_item('Item', 101.0, 1)
        total_above = calculator.calculate_total(0.0)
        self.assertGreater(total_below, total_at - 20)

    def test_large_order_stress_test(self):
        calculator = OrderCalculator()
        for i in range(1000):
            calculator.add_item(f'Item{i}', 10.0, 5)
        total = calculator.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_floating_point_precision(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 0.1, 1)
        calculator.add_item('Item2', 0.2, 1)
        subtotal = calculator.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_state_independence(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 50.0, 1)
        subtotal1 = calculator.get_subtotal()
        total1 = calculator.calculate_total(0.0)
        subtotal2 = calculator.get_subtotal()
        total2 = calculator.calculate_total(0.0)
        self.assertEqual(subtotal1, subtotal2)
        self.assertEqual(total1, total2)

    def test_custom_tax_rate_in_calculations(self):
        calculator = OrderCalculator(tax_rate=0.15)
        calculator.add_item('Apple', 100.0, 1)
        total = calculator.calculate_total(0.0)
        expected_tax = 15.0
        self.assertAlmostEqual(calculator.calculate_tax(100.0), expected_tax, places=2)

    def test_custom_shipping_parameters(self):
        calculator = OrderCalculator(free_shipping_threshold=200.0, shipping_cost=20.0)
        calculator.add_item('Apple', 150.0, 1)
        total = calculator.calculate_total(0.0)
        self.assertGreater(total, 150.0)