import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_init_custom(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.calculate_tax(100.0), 10.0)
        self.assertEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(custom_calc.calculate_shipping(60.0), 0.0)

    def test_add_item_single(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_multiple_distinct(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Apple', 10.0, 1)
        self.calc.add_item('Apple', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 30.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -5.0, 1)

    def test_add_item_zero_or_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Ghost')

    def test_clear_order_populated(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_empty(self):
        try:
            self.calc.clear_order()
        except Exception as e:
            self.fail(f'clear_order() raised {e} unexpectedly on empty order')

    def test_total_items_sum(self):
        self.calc.add_item('A', 5.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_zero(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('X', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_get_subtotal_valid(self):
        self.calc.add_item('Item1', 10.5, 2)
        self.calc.add_item('Item2', 5.25, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 42.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 20.0
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, discount), 80.0)

    def test_apply_discount_exceeds_subtotal(self):
        subtotal = 50.0
        discount = 60.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_flow(self):
        self.calc.add_item('Item1', 40.0, 2)
        total = self.calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 96.1)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calc.calculate_total(), 0.0)

    def test_calculate_total_high_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=100.0), 10.0)