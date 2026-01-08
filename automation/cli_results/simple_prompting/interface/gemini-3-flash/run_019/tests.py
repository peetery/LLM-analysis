import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(40), 5.0)
        self.assertEqual(calc.calculate_shipping(60), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertIn('Apple', self.calc.list_items())
        self.assertFalse(self.calc.is_empty())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0', 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -1.0, 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '5')

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_remove_item_typical(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Nonexistent')

    def test_get_subtotal_typical(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_none(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -1.0)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 150.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=10.0), 61.5)

    def test_calculate_total_free_shipping_scenario(self):
        self.calc.add_item('Item', 120.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=10.0), 135.3)

    def test_total_items_typical(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 7)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_typical(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_typical(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())