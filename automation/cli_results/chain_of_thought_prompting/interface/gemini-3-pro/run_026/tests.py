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

    def test_init_custom(self):
        custom_order = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_order.tax_rate, 0.1)
        self.assertEqual(custom_order.free_shipping_threshold, 50.0)
        self.assertEqual(custom_order.shipping_cost, 5.0)

    def test_add_item_normal(self):
        self.order.add_item('Apple', 1.5)
        self.assertEqual(self.order.total_items(), 1)
        self.assertFalse(self.order.is_empty())

    def test_add_item_specific_quantity(self):
        self.order.add_item('Banana', 0.5, quantity=5)
        self.assertEqual(self.order.total_items(), 5)

    def test_add_item_aggregation(self):
        self.order.add_item('Apple', 1.5, quantity=2)
        self.order.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.order.total_items(), 5)
        self.assertEqual(self.order.get_subtotal(), 1.5 * 5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.order.add_item('Invalid Item', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_item('Invalid Item', 10.0, quantity=0)
        with self.assertRaises(ValueError):
            self.order.add_item('Invalid Item', 10.0, quantity=-1)

    def test_remove_item_normal(self):
        self.order.add_item('Apple', 1.5)
        self.order.remove_item('Apple')
        self.assertTrue(self.order.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.order.remove_item('Ghost')

    def test_clear_order(self):
        self.order.add_item('Apple', 1.5)
        self.order.add_item('Banana', 0.5)
        self.order.clear_order()
        self.assertTrue(self.order.is_empty())
        self.assertEqual(self.order.total_items(), 0)

    def test_is_empty_new(self):
        self.assertTrue(self.order.is_empty())

    def test_is_empty_after_populate(self):
        self.order.add_item('Item', 1.0)
        self.assertFalse(self.order.is_empty())

    def test_total_items_sum(self):
        self.order.add_item('A', 10.0, quantity=2)
        self.order.add_item('B', 20.0, quantity=3)
        self.assertEqual(self.order.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.order.total_items(), 0)

    def test_list_items(self):
        self.order.add_item('TestItem', 10.0)
        items = self.order.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIn('TestItem', items[0])

    def test_get_subtotal(self):
        self.order.add_item('Item1', 10.0, quantity=2)
        self.order.add_item('Item2', 5.0, quantity=1)
        self.assertEqual(self.order.get_subtotal(), 25.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 10.0
        self.assertEqual(self.order.apply_discount(subtotal, discount), 90.0)

    def test_apply_discount_excessive(self):
        subtotal = 50.0
        discount = 60.0
        self.assertEqual(self.order.apply_discount(subtotal, discount), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.order.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.order.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.order.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.order.calculate_tax(amount), 23.0)

    def test_calculate_total_standard(self):
        self.order.add_item('Item', 50.0)
        self.assertAlmostEqual(self.order.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        self.order.add_item('Expensive Item', 200.0)
        self.assertAlmostEqual(self.order.calculate_total(), 246.0)

    def test_calculate_total_empty(self):
        self.assertEqual(self.order.calculate_total(), 0.0)