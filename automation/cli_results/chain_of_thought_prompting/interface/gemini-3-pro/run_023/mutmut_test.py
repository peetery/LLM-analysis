import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_init_custom_values(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(60.0), 0.0)

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_existing_update_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_multiple_distinct(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_item_custom_quantity(self):
        self.calc.add_item('Orange', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 10)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Apple', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_sum_quantities(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 20.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(set(items), {'A', 'B'})

    def test_get_subtotal_mixed_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 40.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 0.0), 100.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calc.calculate_tax(amount), 23.0)

    def test_calculate_total_no_discount_shipping_apply(self):
        self.calc.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -10.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', 10.0, -1)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_total(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, 60.0)

    def test_init_negative_config(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)