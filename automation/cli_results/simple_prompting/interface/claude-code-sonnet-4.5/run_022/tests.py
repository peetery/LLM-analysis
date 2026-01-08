import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

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
        self.calc.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 2.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Banana', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 7)

    def test_add_item_zero_quantity(self):
        self.calc.add_item('Apple', 2.5, 0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -2.5, 1)

    def test_add_item_zero_price(self):
        self.calc.add_item('Apple', 0.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 2.5, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.5, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '2.5', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.5, '1')

    def test_remove_item_exists(self):
        self.calc.add_item('Apple', 2.5, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_item_not_exists(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Apple')

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Banana', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.5)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100.0', 10.0)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '10.0')

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50.0')

    def test_calculate_tax_zero(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_positive(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100.0')

    def test_calculate_total_no_discount_no_shipping(self):
        self.calc.add_item('Apple', 100.0, 1)
        total = self.calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Apple', 100.0, 1)
        total = self.calc.calculate_total(10.0)
        self.assertAlmostEqual(total, 110.7)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Apple', 50.0, 1)
        total = self.calc.calculate_total(0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_empty_order(self):
        total = self.calc.calculate_total(0.0)
        self.assertEqual(total, 0.0)

    def test_calculate_total_negative_discount(self):
        self.calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-10.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('10.0')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single(self):
        self.calc.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_multiple(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Banana', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 2.5, 3)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items_empty(self):
        result = self.calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single(self):
        self.calc.add_item('Apple', 2.5, 3)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('Apple', result)

    def test_list_items_multiple(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Banana', 1.5, 3)
        result = self.calc.list_items()
        self.assertEqual(len(result), 2)
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Apple', 2.5, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 2.5, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove(self):
        self.calc.add_item('Apple', 2.5, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())