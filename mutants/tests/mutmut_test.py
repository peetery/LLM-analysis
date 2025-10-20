import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.5, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, '1')

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 150.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100.0', 10.0)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10.0')

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_zero(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_positive(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100.0')

    def test_calculate_total_single_item_no_discount(self):
        self.calculator.add_item('Apple', 100.0, 1)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 123.0)

    def test_calculate_total_below_shipping_threshold(self):
        self.calculator.add_item('Apple', 50.0, 1)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 73.8)

    def test_calculate_total_multiple_items(self):
        self.calculator.add_item('Apple', 50.0, 2)
        self.calculator.add_item('Banana', 25.0, 2)
        result = self.calculator.calculate_total()
        self.assertEqual(result, 184.5)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-10.0)

    def test_calculate_total_discount_exceeds_subtotal(self):
        self.calculator.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(100.0)

    def test_calculate_total_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('10.0')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty(self):
        result = self.calculator.list_items()
        self.assertEqual(result, [])

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 1.5, 2)
        result = self.calculator.list_items()
        self.assertEqual(result, ['Apple'])

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        result = self.calculator.list_items()
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertEqual(len(result), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
if __name__ == '__main__':
    unittest.main()