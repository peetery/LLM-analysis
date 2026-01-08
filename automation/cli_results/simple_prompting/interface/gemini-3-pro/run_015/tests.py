import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_initial_state(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.list_items(), [])

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 5.0)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_accumulate_quantity(self):
        self.calc.add_item('Banana', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQtyNegative', 5.0, -1)

    def test_remove_item(self):
        self.calc.add_item('Orange', 3.0, 2)
        self.calc.remove_item('Orange')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_nonexistent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_get_subtotal(self):
        self.calc.add_item('Item1', 10.0, 1)
        self.calc.add_item('Item2', 20.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 0.1
        expected = 90.0
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, discount), expected)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        subtotal = 50.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 10.0)

    def test_calculate_shipping_above_threshold(self):
        subtotal = 150.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        subtotal = 100.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calc.calculate_tax(amount), 20.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 70.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 216.0)

    def test_calculate_total_shipping_logic_boundary(self):
        self.calc.add_item('Item', 105.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 123.4)

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items(self):
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 20)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())