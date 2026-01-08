import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(len(self.calc.list_items()), 0)

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Bread', 3.0, 1)
        self.calc.add_item('Bread', 3.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, -1)

    def test_add_item_price_conflict(self):
        self.calc.add_item('Milk', 3.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Milk', 3.5, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '1.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 1.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Orange', 1.5, 1)
        self.calc.remove_item('Orange')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_missing(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(50.0, 0.0), 50.0)
        self.assertEqual(self.calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-1.0, 0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.01)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.01)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '20%')

    def test_calculate_shipping_logic(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_logic(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('amount')

    def test_calculate_total_typical(self):
        self.calc.add_item('Widget', 20.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 61.5)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Gadget', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 123.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Premium', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(None)

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_uniqueness(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertCountEqual(items, ['A', 'B'])

    def test_is_empty_logic(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())