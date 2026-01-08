import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom_values(self):
        custom = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom.tax_rate, 0.1)
        self.assertEqual(custom.free_shipping_threshold, 50.0)
        self.assertEqual(custom.shipping_cost, 5.0)

    def test_init_type_errors(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_value_errors(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 2.0)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 8)

    def test_add_item_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '2.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.0, 1.5)

    def test_add_item_value_errors(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, -1)

    def test_add_item_price_mismatch(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0, 1)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Cherry')

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 0.0), 50.0)
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100, '0.1')

    def test_apply_discount_value_errors(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10, 0.1)

    def test_calculate_shipping_logic(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_tax_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_total_integration(self):
        self.calc.add_item('A', 10.0, 4)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 61.5)
        self.calc.clear_order()
        self.calc.add_item('B', 100.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 221.4)

    def test_calculate_total_type_error(self):
        self.calc.add_item('A', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_calculate_total_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.0)

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.items), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())