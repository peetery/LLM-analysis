import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 10.0, 0)

    def test_add_item_conflicting_price(self):
        self.calculator.add_item('Product', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 15.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product', '10.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Bread', 5.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_basic(self):
        self.calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(0.5), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 1.0, 2)
        self.calculator.add_item('B', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_unique(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.add_item('B', 2.0, 1)
        self.calculator.add_item('A', 1.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())