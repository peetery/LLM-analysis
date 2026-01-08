import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_custom_values(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(60.0), 0.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_normal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Banana', 0.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_duplicate(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Zero', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', 10.0, -1)

    def test_remove_item_normal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.list_items()), 0)

    def test_get_subtotal_populated(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_total_items_count(self):
        self.calc.add_item('A', 10.0, 5)
        self.calc.add_item('B', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_list_items_names(self):
        items = ['Apple', 'Banana', 'Cherry']
        for item in items:
            self.calc.add_item(item, 1.0, 1)
        self.assertCountEqual(self.calc.list_items(), items)

    def test_is_empty_state_transitions(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())

    def test_apply_discount_zero(self):
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.0)
        self.assertAlmostEqual(discounted, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.0), expected)

    def test_precision_floating_point(self):
        self.calc.add_item('Small', 0.1, 3)
        self.calc.add_item('Pricey', 19.99, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 20.29, places=7)