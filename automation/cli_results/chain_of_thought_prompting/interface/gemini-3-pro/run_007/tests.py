import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.oc = OrderCalculator()

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.get_subtotal(), 0.0)
        self.assertTrue(oc.is_empty())

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(oc.is_empty())

    def test_add_single_item(self):
        self.oc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', self.oc.list_items())
        self.assertEqual(self.oc.total_items(), 2)
        self.assertAlmostEqual(self.oc.get_subtotal(), 3.0)

    def test_add_item_default_quantity(self):
        self.oc.add_item('Banana', 0.99)
        self.assertEqual(self.oc.total_items(), 1)
        self.assertAlmostEqual(self.oc.get_subtotal(), 0.99)

    def test_add_multiple_items(self):
        self.oc.add_item('Apple', 1.0, 1)
        self.oc.add_item('Banana', 2.0, 1)
        items = self.oc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_existing_item_updates_quantity(self):
        self.oc.add_item('Apple', 10.0, 1)
        self.oc.add_item('Apple', 10.0, 2)
        self.assertEqual(self.oc.total_items(), 3)
        self.assertAlmostEqual(self.oc.get_subtotal(), 30.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('BadItem', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.oc.add_item('BadItem', 5.0, -1)

    def test_remove_existing_item(self):
        self.oc.add_item('Apple', 1.0, 1)
        self.oc.remove_item('Apple')
        self.assertTrue(self.oc.is_empty())
        self.assertEqual(self.oc.get_subtotal(), 0.0)

    def test_remove_non_existent_item(self):
        with self.assertRaises(KeyError):
            self.oc.remove_item('Ghost')

    def test_subtotal_empty_order(self):
        self.assertAlmostEqual(self.oc.get_subtotal(), 0.0)

    def test_subtotal_calculation(self):
        self.oc.add_item('A', 10.0, 2)
        self.oc.add_item('B', 5.5, 4)
        self.assertAlmostEqual(self.oc.get_subtotal(), 42.0)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        result = self.oc.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        result = self.oc.apply_discount(subtotal, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_invalid_high(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, -0.1)

    def test_shipping_below_threshold(self):
        cost = self.oc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_shipping_above_threshold(self):
        cost = self.oc.calculate_shipping(100.01)
        self.assertAlmostEqual(cost, 0.0)

    def test_shipping_exactly_on_threshold(self):
        cost = self.oc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax(self):
        tax = self.oc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_total_calculation_flow(self):
        self.oc.add_item('Item1', 100.0, 2)
        total = self.oc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_total_empty_order(self):
        total = self.oc.calculate_total()
        self.assertAlmostEqual(total, 0.0)

    def test_total_with_free_shipping_and_discount(self):
        self.oc.add_item('Item', 110.0, 1)
        total = self.oc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 131.77)

    def test_total_items_count(self):
        self.oc.add_item('A', 10, 1)
        self.oc.add_item('B', 10, 2)
        self.oc.add_item('C', 10, 3)
        self.assertEqual(self.oc.total_items(), 6)

    def test_clear_order(self):
        self.oc.add_item('A', 10, 1)
        self.oc.clear_order()
        self.assertTrue(self.oc.is_empty())
        self.assertEqual(self.oc.get_subtotal(), 0.0)

    def test_list_items(self):
        self.oc.add_item('A', 10)
        self.oc.add_item('B', 20)
        items = self.oc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty(self):
        self.assertTrue(self.oc.is_empty())
        self.oc.add_item('A', 1)
        self.assertFalse(self.oc.is_empty())