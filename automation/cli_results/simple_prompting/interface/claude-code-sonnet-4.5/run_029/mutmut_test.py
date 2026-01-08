import unittest
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
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.0)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', '1.0', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 1.0, '1')

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 2.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calculator.get_subtotal(), 4.0)

    def test_get_subtotal_decimal_precision(self):
        self.calculator.add_item('Item', 1.99, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 5.97, places=2)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        shipping = self.calculator.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Apple', 10.0, 2)
        total = self.calculator.calculate_total(0.0)
        expected = (20.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Apple', 10.0, 2)
        total = self.calculator.calculate_total(0.1)
        expected = (18.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Apple', 50.0, 3)
        total = self.calculator.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calculator.add_item('Apple', 60.0, 2)
        total = self.calculator.calculate_total(0.1)
        expected = 108.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_default_discount(self):
        self.calculator.add_item('Apple', 10.0, 1)
        total = self.calculator.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Apple', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_after_remove(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 3)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty(self):
        items = self.calculator.list_items()
        self.assertEqual(items, [])

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 1.0, 2)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertEqual(len(items), 1)

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_after_remove(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 0.5, 3)
        self.calculator.remove_item('Apple')
        items = self.calculator.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_returns_copy(self):
        self.calculator.add_item('Apple', 1.0, 2)
        items = self.calculator.list_items()
        items.append('Banana')
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_integration_full_order_flow(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        subtotal = self.calculator.get_subtotal()
        self.assertEqual(subtotal, 35.0)
        total = self.calculator.calculate_total(0.1)
        expected = (31.5 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_integration_order_modification(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.calculator.remove_item('Apple')
        self.calculator.add_item('Orange', 8.0, 1)
        total = self.calculator.calculate_total(0.0)
        expected = (23.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_edge_case_large_quantity(self):
        self.calculator.add_item('Item', 1.0, 1000)
        self.assertEqual(self.calculator.total_items(), 1000)

    def test_edge_case_small_price(self):
        self.calculator.add_item('Item', 0.01, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.01)

    def test_edge_case_large_price(self):
        self.calculator.add_item('Item', 999999.99, 1)
        self.assertEqual(self.calculator.get_subtotal(), 999999.99)

    def test_edge_case_many_items(self):
        for i in range(100):
            self.calculator.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(self.calculator.total_items(), 100)