import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_value_errors(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_errors(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_add_item_value_errors(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, -1)
        self.calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 15.0, 1)

    def test_add_item_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '10', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_value_errors(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_free_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_free_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_success(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_complex(self):
        self.calc.add_item('Item 1', 40.0, 2)
        total = self.calc.calculate_total(0.1)
        self.assertAlmostEqual(total, 100.86)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item 1', 120.0, 1)
        total = self.calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 147.6)

    def test_calculate_total_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_value_error(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_type_error(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())