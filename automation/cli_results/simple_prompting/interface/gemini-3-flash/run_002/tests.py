import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(99), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_add_item_valid(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1000.0)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, -1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Valid', '10.0', 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Banana')
        self.assertEqual(self.calc.total_items(), 1)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multi_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 10.0), 90.0)

    def test_apply_discount_more_than_subtotal(self):
        self.assertEqual(self.calc.apply_discount(50.0, 100.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 70.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Item', 150.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=50.0), 120.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_populated(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_populated(self):
        self.calc.add_item('Apple', 1, 1)
        self.calc.add_item('Banana', 1, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1, 1)
        self.assertFalse(self.calc.is_empty())