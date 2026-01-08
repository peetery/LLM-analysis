import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_negative_values(self):
        calc = OrderCalculator(tax_rate=-0.1)
        self.assertEqual(calc.calculate_tax(100.0), -10.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.5)

    def test_add_item_multiple_distinct(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Orange', 2.0, 1)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_duplicate(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 2.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, 0)

    def test_remove_existing_item(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existent_item(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Ghost')

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_total_items_count(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item('Item1', 10)
        items = self.calculator.list_items()
        self.assertIsInstance(items, list)
        self.assertTrue(any(('Item1' in s for s in items)))

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Item', 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Item', 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_exceeds_subtotal(self):
        result = self.calculator.apply_discount(50.0, 60.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(50.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_simple(self):
        self.calculator.add_item('Item', 10.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 22.3)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 50.0, 2)
        total = self.calculator.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 120.7)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 200.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_empty(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)