import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertAlmostEqual(self.calc.tax_rate, 0.23)
        self.assertAlmostEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.tax_rate, 0.1)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_success(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_invalid_inputs(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_same_name_diff_price(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_calculate_shipping(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.9), 10.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('99.9')

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_below_free_shipping(self):
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_above_free_shipping(self):
        self.calc.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.2), 110.7)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10.0, 5)
        self.calc.add_item('B', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 20.0)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())