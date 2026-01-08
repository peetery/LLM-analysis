import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Laptop')

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Mouse', 20.0, 1)
        self.calculator.add_item('Mouse', 20.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_different_price_error(self):
        self.calculator.add_item('Mouse', 20.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Mouse', 25.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', '10.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 10.0, '1')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -5.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, -1)

    def test_remove_item_success(self):
        self.calculator.add_item('Laptop', 1000.0)
        self.calculator.remove_item('Laptop')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_success(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_and_full(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_and_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_total_basic(self):
        self.calculator.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 123.0)

    def test_calculate_total_with_shipping_and_discount(self):
        self.calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(0.1), 67.65)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_type(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.1')

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 10.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 20.0)
        self.calculator.add_item('A', 10.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10.0)
        self.assertFalse(self.calculator.is_empty())