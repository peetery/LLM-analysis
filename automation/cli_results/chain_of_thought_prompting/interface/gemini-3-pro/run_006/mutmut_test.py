import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)

    def test_add_item_multiple_distinct(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 7)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertIn('Banana', self.calculator.list_items())

    def test_add_item_accumulate_quantity(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(self.calculator.get_subtotal(), 8.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 5.0, -1)

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_calculation(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.5, 4)
        self.assertEqual(self.calculator.get_subtotal(), 42.0)

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_total_standard_flow(self):
        self.calculator.add_item('Item', 50.0, 1)
        total = self.calculator.calculate_total()
        self.assertGreater(total, 50.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('ExpensiveItem', 200.0, 1)
        total = self.calculator.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0)