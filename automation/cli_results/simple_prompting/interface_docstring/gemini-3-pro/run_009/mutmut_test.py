import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_increment_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -1)

    def test_add_item_price_mismatch(self):
        self.calculator.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, '1')

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calculator.apply_discount(0.0, 0.2)
        self.assertEqual(result, 0.0)

    def test_apply_discount_bounds(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_success(self):
        self.calculator.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 123.0)

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.5), 123.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10.0, 3)
        self.calculator.add_item('B', 5.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.assertEqual(self.calculator.list_items(), [])
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 5.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10.0)
        self.assertFalse(self.calculator.is_empty())