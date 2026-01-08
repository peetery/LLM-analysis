import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_valid_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_valid_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 10.0, -1)

    def test_add_item_different_price_exists(self):
        self.calculator.add_item('Product', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product', 15.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product', '10.0', 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product', 10.0, 1.5)

    def test_remove_item_valid(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100, '0.1')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax(None)

    def test_calculate_total_valid(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.1), 66.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_calculate_total_invalid_type(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.1')

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 1.0, 2)
        self.calculator.add_item('B', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_unique(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 2.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())