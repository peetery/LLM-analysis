import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_initialization_defaults(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_initialization_custom(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(custom_calc.is_empty())

    def test_add_item_single(self):
        self.calc.add_item('Apple', 2.5, 1)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 2.5)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Banana', 1.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.0)

    def test_add_item_accumulation(self):
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', -10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('ErrorItem', 10.0, -5)
        with self.assertRaises(TypeError):
            self.calc.add_item('ErrorItem', 'ten', 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Orange', 3.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_get_subtotal(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 10.0
        result = self.calc.apply_discount(subtotal, discount)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_calculate_shipping_below_threshold(self):
        subtotal = 50.0
        shipping = self.calc.calculate_shipping(subtotal)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        subtotal = 150.0
        shipping = self.calc.calculate_shipping(subtotal)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        subtotal = 100.0
        shipping = self.calc.calculate_shipping(subtotal)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        tax = self.calc.calculate_tax(amount)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('ItemA', 50.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('ItemB', 200.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('ItemC', 100.0, 1)
        total = self.calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 120.7)

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1, 5)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 10, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('Apple: 2 x 1.0', items)
        self.assertIn('Banana: 1 x 2.0', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())