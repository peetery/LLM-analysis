import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        c = OrderCalculator()
        self.assertEqual(c.calculate_shipping(1.0), 10.0)

    def test_init_custom_values(self):
        c = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(c.calculate_shipping(40.0), 5.0)
        self.assertEqual(c.calculate_shipping(60.0), 0.0)

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Ghost', 10.0, 0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, -1)

    def test_add_duplicate_item(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Apple', 2.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 4.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 10.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_subtotal_single_item(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Item1', 10.0, 1)
        self.calc.add_item('Item2', 5.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        self.assertTrue(total > 50.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 150.0)
        expected_tax = 150.0 * 0.23
        self.assertAlmostEqual(self.calc.calculate_total(), 150.0 + expected_tax)

    def test_total_items(self):
        self.calc.add_item('A', 1, 2)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1)
        self.assertFalse(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item('A', 1)
        self.assertIn('A', self.calc.list_items())