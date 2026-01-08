import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        c = OrderCalculator()
        self.assertTrue(c.is_empty())

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.0)

    def test_add_item_cumulative_quantity(self):
        self.calc.add_item('Orange', 1.5, 2)
        self.calc.add_item('Orange', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_update_price(self):
        self.calc.add_item('Book', 10.0, 1)
        self.calc.add_item('Book', 10.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Ghost', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Ghost', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Ghost', 5.0, -1)
        with self.assertRaises(ValueError):
            self.calc.add_item('', 5.0, 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Tablet', 300.0, 1)
        self.calc.remove_item('Tablet')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existing(self):
        try:
            self.calc.remove_item('NonExistent')
        except KeyError:
            self.fail('remove_item raised KeyError unexpectedly')

    def test_get_subtotal(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount(self):
        subtotal = 100.0
        result = self.calc.apply_discount(subtotal, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        val = 99.99
        self.assertEqual(self.calc.calculate_shipping(val), 10.0)

    def test_calculate_shipping_at_threshold(self):
        val = 100.0
        self.assertEqual(self.calc.calculate_shipping(val), 0.0)

    def test_calculate_shipping_above_threshold(self):
        val = 150.0
        self.assertEqual(self.calc.calculate_shipping(val), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calc.calculate_tax(amount), 23.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item1', 50.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 120.7)

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 10, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertTrue(any(('Apple' in s for s in items)))
        self.assertTrue(any(('Banana' in s for s in items)))

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())