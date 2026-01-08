import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_defaults(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_price_conflict(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_remove_item_valid(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.2)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_with_discount_and_shipping(self):
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.2), 110.7)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('A', 1)
        self.calc.add_item('B', 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1)
        self.assertFalse(self.calc.is_empty())