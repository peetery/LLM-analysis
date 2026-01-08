import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertAlmostEqual(calc.calculate_shipping(150.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(calc.calculate_shipping(150.0), 20.0)
        self.assertEqual(calc.calculate_shipping(250.0), 0.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 1.5)

    def test_add_item_multiple(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.add_item('Banana', 2.0)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.5)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, -5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existing(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Ghost')

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_is_empty_initially(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding(self):
        self.calculator.add_item('Apple', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items_sum_quantities(self):
        self.calculator.add_item('Apple', 1.0, 3)
        self.calculator.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('Apple', 1.0)
        items = self.calculator.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], str)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.0)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 0.1
        expected = 90.0
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, discount), expected)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_calculation(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_total_no_discount_with_shipping(self):
        self.calculator.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 71.5)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 120.7)

    def test_calculate_total_empty(self):
        self.assertAlmostEqual(self.calculator.calculate_total(), 0.0)