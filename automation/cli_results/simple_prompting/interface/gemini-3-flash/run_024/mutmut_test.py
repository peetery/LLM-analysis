import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

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
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1200.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Mouse', 25.0, 1)
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_different_price_error(self):
        self.calc.add_item('Mouse', 25.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Mouse', 30.0, 1)

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -5.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 'price', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, 1.5)

    def test_remove_item_typical(self):
        self.calc.add_item('Item A', 10.0, 1)
        self.calc.add_item('Item B', 20.0, 1)
        self.calc.remove_item('Item A')
        self.assertEqual(self.calc.total_items(), 1)
        self.assertNotIn('Item A', self.calc.list_items())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_typical(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_typical(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_boundaries(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_logic(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 60.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 78.72)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 7)

    def test_clear_order(self):
        self.calc.add_item('Item', 10.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_uniqueness(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_is_empty_logic(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0, 1)
        self.assertFalse(self.calc.is_empty())