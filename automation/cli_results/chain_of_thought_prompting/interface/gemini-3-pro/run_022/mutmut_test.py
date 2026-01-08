import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.order = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.order.calculate_tax(100.0), 23.0)
        self.assertEqual(self.order.calculate_shipping(99.0), 10.0)
        self.assertEqual(self.order.calculate_shipping(100.0), 0.0)

    def test_init_custom_values(self):
        custom_order = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_order.calculate_tax(100.0), 10.0)
        self.assertEqual(custom_order.calculate_shipping(49.0), 5.0)
        self.assertEqual(custom_order.calculate_shipping(50.0), 0.0)

    def test_add_single_item(self):
        self.order.add_item('Apple', 1.5, 10)
        self.assertEqual(self.order.total_items(), 10)
        self.assertEqual(self.order.get_subtotal(), 15.0)

    def test_add_multiple_items(self):
        self.order.add_item('Apple', 1.5, 2)
        self.order.add_item('Banana', 2.0, 3)
        self.assertEqual(self.order.total_items(), 5)
        self.assertEqual(self.order.get_subtotal(), 9.0)

    def test_add_existing_item_accumulates_quantity(self):
        self.order.add_item('Apple', 1.0, 5)
        self.order.add_item('Apple', 1.0, 3)
        self.assertEqual(self.order.total_items(), 8)
        self.assertEqual(self.order.get_subtotal(), 8.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.order.add_item('BadItem', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.order.add_item('BadItem', 5.0, -1)

    def test_remove_non_existent_item(self):
        with self.assertRaises((ValueError, KeyError)):
            self.order.remove_item('NonExistentItem')

    def test_clear_order(self):
        self.order.add_item('Apple', 1.0)
        self.order.clear_order()
        self.assertTrue(self.order.is_empty())
        self.assertEqual(self.order.total_items(), 0)

    def test_is_empty_initially(self):
        self.assertTrue(self.order.is_empty())

    def test_is_empty_after_add(self):
        self.order.add_item('Apple', 1.0)
        self.assertFalse(self.order.is_empty())

    def test_total_items_calculation(self):
        self.order.add_item('A', 10.0, 2)
        self.order.add_item('B', 5.0, 3)
        self.assertEqual(self.order.total_items(), 5)

    def test_list_items_format(self):
        self.order.add_item('Apple', 1.5, 2)
        items = self.order.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_get_subtotal_mixed_items(self):
        self.order.add_item('A', 10.0, 2)
        self.order.add_item('B', 5.5, 2)
        self.assertEqual(self.order.get_subtotal(), 31.0)

    def test_apply_discount_valid(self):
        self.assertEqual(self.order.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.order.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.order.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.order.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.order.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.order.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(self.order.calculate_tax(100.0), 23.0)

    def test_calculate_total_with_discount(self):
        self.order.add_item('X', 100.0, 2)
        self.assertEqual(self.order.calculate_total(discount=0.5), 123.0)