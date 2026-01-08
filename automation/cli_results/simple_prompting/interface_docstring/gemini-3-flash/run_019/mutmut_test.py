import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_errors(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertAlmostEqual(self.calc.get_subtotal(), 16.0)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('A', 0.0, 1)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('A', -1.0, 1)

    def test_add_item_invalid_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('A', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('A', 10.0, -5)

    def test_add_item_conflicting_price(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, 1)

    def test_add_item_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 2.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'free', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 1)
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Orange')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_calculation(self):
        self.calc.add_item('A', 1.5, 2)
        self.calc.add_item('B', 10.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 13.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.25), 75.0)
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 0.0), 50.0)
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.01)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.01)

    def test_apply_discount_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_logic(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.9), 10.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(1000.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_tax(200.0), 46.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-0.01)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('amount')

    def test_calculate_total_basic(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Premium', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.0)

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('A', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.5)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_type_error(self):
        self.calc.add_item('A', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total([])

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('X', 10.0, 10)
        self.calc.add_item('Y', 5.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('B', 1.0, 1)
        self.calc.add_item('A', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())