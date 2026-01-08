import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.order = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.order.tax_rate, 0.23)
        self.assertEqual(self.order.free_shipping_threshold, 100.0)
        self.assertEqual(self.order.shipping_cost, 10.0)
        self.assertTrue(self.order.is_empty())

    def test_init_custom_config(self):
        custom_order = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_order.tax_rate, 0.1)
        self.assertEqual(custom_order.free_shipping_threshold, 50.0)
        self.assertEqual(custom_order.shipping_cost, 5.0)

    def test_add_item_new(self):
        self.order.add_item('Apple', 1.5, 2)
        self.assertEqual(self.order.total_items(), 2)
        self.assertIn('Apple', self.order.list_items())

    def test_add_item_update_quantity(self):
        self.order.add_item('Apple', 1.5, 1)
        self.order.add_item('Apple', 1.5, 2)
        self.assertEqual(self.order.total_items(), 3)

    def test_add_item_custom_quantity(self):
        self.order.add_item('Banana', 2.0, 10)
        self.assertEqual(self.order.total_items(), 10)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.order.add_item('BadItem', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.order.add_item('BadQtyNegative', 10.0, -1)

    def test_remove_item_normal(self):
        self.order.add_item('Apple', 1.0)
        self.order.remove_item('Apple')
        self.assertTrue(self.order.is_empty())

    def test_clear_order(self):
        self.order.add_item('Apple', 1.0)
        self.order.add_item('Banana', 2.0)
        self.order.clear_order()
        self.assertTrue(self.order.is_empty())
        self.assertEqual(self.order.total_items(), 0)

    def test_is_empty(self):
        self.assertTrue(self.order.is_empty())
        self.order.add_item('Apple', 1.0)
        self.assertFalse(self.order.is_empty())

    def test_total_items(self):
        self.order.add_item('A', 10.0, 2)
        self.order.add_item('B', 5.0, 3)
        self.assertEqual(self.order.total_items(), 5)

    def test_list_items_normal(self):
        self.order.add_item('Apple', 1.0)
        self.order.add_item('Banana', 2.0)
        items = self.order.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        self.assertEqual(self.order.list_items(), [])

    def test_get_subtotal_normal(self):
        self.order.add_item('Item1', 10.0, 2)
        self.order.add_item('Item2', 5.0, 1)
        self.assertEqual(self.order.get_subtotal(), 25.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.order.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_on_threshold(self):
        self.assertEqual(self.order.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.order.calculate_shipping(101.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.order.calculate_tax(100.0), 23.0)

    def test_calculate_total_free_shipping(self):
        self.order.add_item('ExpensiveItem', 100.0)
        self.assertAlmostEqual(self.order.calculate_total(), 123.0)