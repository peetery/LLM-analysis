import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 60.0, 1)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_existing_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 2.0, 1)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_clear_order(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 3.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Banana', 3.0, 1)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -1.0)

    def test_apply_discount_over_hundred(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 101.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_valid(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_integration(self):
        self.calculator.add_item('Item1', 50.0, 2)
        total = self.calculator.calculate_total(discount=10.0)
        self.assertEqual(total, 123.0)

    def test_calculate_total_empty_order(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 12.3)

    def test_calculation_returns_float(self):
        self.calculator.add_item('A', 10, 1)
        self.assertIsInstance(self.calculator.get_subtotal(), float)
        self.assertIsInstance(self.calculator.calculate_total(), float)

    def test_list_items_returns_list(self):
        self.assertIsInstance(self.calculator.list_items(), list)