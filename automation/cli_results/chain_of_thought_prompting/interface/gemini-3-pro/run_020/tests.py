import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 2)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_accumulates_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 7.5)

    def test_add_item_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -1.0, 1)

    def test_add_item_invalid_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, -5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent_raises_error(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('NonExistent')

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item('Apple', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items_sum_quantities(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_returns_names(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 10)
        items = self.calculator.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_clear_order_resets_state(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_empty_order(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.0)

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_exceeds_subtotal(self):
        result = self.calculator.apply_discount(50.0, 60.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax_normal(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_integration(self):
        self.calculator.add_item('Item', 50.0, 1)
        total = self.calculator.calculate_total(discount=10.0)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('ExpensiveItem', 200.0, 1)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_empty_order(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)

    def test_floating_point_precision(self):
        self.calculator.add_item('A', 0.1, 1)
        self.calculator.add_item('B', 0.2, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3)