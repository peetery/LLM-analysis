import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_negative_values_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_with_quantity_greater_than_one(self):
        self.calculator.add_item('Banana', 0.5, quantity=5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Orange', 1.0, quantity=0)

    def test_add_item_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Orange', 1.0, quantity=-2)

    def test_add_item_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -5.0)

    def test_accumulate_items(self):
        self.calculator.add_item('Apple', 1.0, quantity=2)
        self.calculator.add_item('Apple', 1.0, quantity=3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_remove_existing_item(self):
        self.calculator.add_item('Milk', 2.0)
        self.calculator.remove_item('Milk')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existent_item_raises_error(self):
        self.calculator.add_item('Bread', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_from_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Anything')

    def test_clear_order(self):
        self.calculator.add_item('Eggs', 3.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_clear_empty_order(self):
        try:
            self.calculator.clear_order()
        except Exception:
            self.fail('clear_order() raised Exception unexpectedly on empty order!')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.5, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.5)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 20.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 80.0)

    def test_apply_discount_exceeding_subtotal(self):
        subtotal = 50.0
        discount = 60.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 0.0)

    def test_apply_negative_discount_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(50.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax_normal(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_simple(self):
        self.calculator.add_item('Item1', 50.0)
        expected_total = 50.0 + 10.0 + 50.0 * 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item1', 200.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item1', 200.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=50.0), 184.5)

    def test_calculate_total_discount_triggers_shipping(self):
        self.calculator.add_item('Item1', 120.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=30.0), 120.7)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Something', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items(self):
        self.calculator.add_item('A', 1, 2)
        self.calculator.add_item('B', 1, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 1.0)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)