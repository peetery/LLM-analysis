import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(10.0), 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_existing_item_update(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, 0)

    def test_remove_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_non_existent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_total_items_aggregation(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 5.0)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 10.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 90.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertEqual(self.calc.calculate_total(), 71.5)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertEqual(self.calc.calculate_total(discount=10.0), 120.7)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertEqual(self.calc.calculate_total(), 246.0)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calc.calculate_total(), 0.0)