import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_add_item_defaults(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_custom_quantity(self):
        self.calculator.add_item('Banana', 0.5, quantity=5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_update_existing(self):
        self.calculator.add_item('Apple', 1.5, quantity=2)
        self.calculator.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Item', -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Item', 10.0, quantity=0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Item', 10.0, quantity=-1)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_mixed_items(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.5, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.5)

    def test_get_subtotal_precision(self):
        self.calculator.add_item('ItemA', 10.1)
        self.calculator.add_item('ItemB', 20.2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 30.3)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_exact_boundary(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Expensive Item', 200.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_total_items_sum(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 10, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item('Banana', 1.0)
        self.calculator.add_item('Apple', 1.0)
        items = self.calculator.list_items()
        self.assertIn('Banana', items)
        self.assertIn('Apple', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Item', 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())