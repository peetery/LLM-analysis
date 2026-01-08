import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.order = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.order.tax_rate, 0.23)
        self.assertEqual(self.order.free_shipping_threshold, 100.0)
        self.assertEqual(self.order.shipping_cost, 10.0)

    def test_init_custom_values(self):
        custom_order = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_order.tax_rate, 0.1)
        self.assertEqual(custom_order.free_shipping_threshold, 50.0)
        self.assertEqual(custom_order.shipping_cost, 5.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.order.add_item('Laptop', 1000.0, 1)
        self.assertFalse(self.order.is_empty())
        self.assertEqual(self.order.total_items(), 1)

    def test_add_item_default_quantity(self):
        self.order.add_item('Mouse', 25.0)
        self.assertEqual(self.order.total_items(), 1)
        self.assertIn('Mouse', self.order.list_items())

    def test_add_multiple_items(self):
        self.order.add_item('Laptop', 1000.0, 1)
        self.order.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.order.total_items(), 3)
        self.assertEqual(len(self.order.list_items()), 2)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.order.add_item('Bad Price', -10.0, 1)
        with self.assertRaises(ValueError):
            self.order.add_item('Zero Price', 0.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.order.add_item('Bad Qty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.order.add_item('Negative Qty', 10.0, -1)

    def test_remove_item_existing(self):
        self.order.add_item('Laptop', 1000.0, 1)
        self.order.remove_item('Laptop')
        self.assertTrue(self.order.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.order.remove_item('Ghost Item')

    def test_remove_from_empty_order(self):
        with self.assertRaises(KeyError):
            self.order.remove_item('Nothing')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.order.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.order.add_item('Item 1', 10.0, 2)
        self.order.add_item('Item 2', 30.0, 1)
        self.assertEqual(self.order.get_subtotal(), 50.0)

    def test_apply_discount_valid(self):
        result = self.order.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_greater_than_subtotal(self):
        result = self.order.apply_discount(50.0, 60.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero(self):
        result = self.order.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.order.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.order.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.order.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.order.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        cost = self.order.calculate_shipping(0.0)
        self.assertTrue(cost >= 0.0)

    def test_calculate_tax_positive(self):
        tax = self.order.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.order.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_no_discount(self):
        self.order.add_item('Item', 50.0, 1)
        total = self.order.calculate_total()
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_with_discount(self):
        self.order.add_item('Item', 120.0, 1)
        total = self.order.calculate_total(discount=30.0)
        self.assertAlmostEqual(total, 120.7)

    def test_calculate_total_free_shipping(self):
        self.order.add_item('Expensive Item', 200.0, 1)
        total = self.order.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_discount_triggers_shipping(self):
        self.order.add_item('Item', 110.0, 1)
        total = self.order.calculate_total(discount=20.0)
        self.assertAlmostEqual(total, 120.7)

    def test_total_items_sum(self):
        self.order.add_item('A', 10.0, 5)
        self.order.add_item('B', 20.0, 3)
        self.assertEqual(self.order.total_items(), 8)

    def test_clear_order(self):
        self.order.add_item('A', 10.0)
        self.order.clear_order()
        self.assertTrue(self.order.is_empty())
        self.assertEqual(self.order.get_subtotal(), 0.0)

    def test_list_items(self):
        self.order.add_item('Apple', 1.0)
        self.order.add_item('Banana', 2.0)
        items = self.order.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_initial(self):
        self.assertTrue(self.order.is_empty())

    def test_is_empty_after_add(self):
        self.order.add_item('Item', 1.0)
        self.assertFalse(self.order.is_empty())