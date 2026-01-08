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
        self.calculator.add_item('Product A', 10.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Product A', 10.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Product A', 10.0)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_same_name_updates(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product A', 15.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_zero_quantity(self):
        self.calculator.add_item('Product A', 10.0, 0)
        self.assertEqual(self.calculator.total_items(), 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product A', 10.0, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Product A', -10.0, 1)

    def test_add_item_zero_price(self):
        self.calculator.add_item('Product A', 0.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product A', 'invalid', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product A', 10.0, 'invalid')

    def test_remove_item_existing(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.remove_item('Product A')
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Nonexistent')

    def test_remove_item_from_multiple(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product B', 20.0, 3)
        self.calculator.remove_item('Product A')
        self.assertEqual(self.calculator.total_items(), 3)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product B', 15.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 65.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 150.0)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, 'invalid')

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_amount(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Product A', 10.0, 5)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 73.8)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calculator.add_item('Product A', 50.0, 3)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 184.5)

    def test_calculate_total_with_discount_below_threshold(self):
        self.calculator.add_item('Product A', 50.0, 1)
        total = self.calculator.calculate_total(discount=10.0)
        self.assertEqual(total, 61.2)

    def test_calculate_total_with_discount_above_threshold(self):
        self.calculator.add_item('Product A', 100.0, 2)
        total = self.calculator.calculate_total(discount=50.0)
        self.assertEqual(total, 184.5)

    def test_calculate_total_empty_order(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_full_discount(self):
        self.calculator.add_item('Product A', 50.0, 1)
        total = self.calculator.calculate_total(discount=50.0)
        self.assertEqual(total, 0.0)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('Product A', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-10.0)

    def test_calculate_total_excessive_discount(self):
        self.calculator.add_item('Product A', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=100.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('Product A', 10.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Product A', 10.0, 5)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_resets_subtotal(self):
        self.calculator.add_item('Product A', 10.0, 5)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_list_items_empty(self):
        result = self.calculator.list_items()
        self.assertEqual(result, [])

    def test_list_items_single_item(self):
        self.calculator.add_item('Product A', 10.0, 2)
        result = self.calculator.list_items()
        self.assertIn('Product A', result)
        self.assertEqual(len(result), 1)

    def test_list_items_multiple_items(self):
        self.calculator.add_item('Product A', 10.0, 2)
        self.calculator.add_item('Product B', 20.0, 3)
        result = self.calculator.list_items()
        self.assertIn('Product A', result)
        self.assertIn('Product B', result)
        self.assertEqual(len(result), 2)

    def test_is_empty_initially(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item('Product A', 10.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clearing(self):
        self.calculator.add_item('Product A', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calculator.add_item('Product A', 10.0, 1)
        self.calculator.remove_item('Product A')
        self.assertTrue(self.calculator.is_empty())

    def test_add_item_float_quantity_invalid(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Product A', 10.0, 2.5)

    def test_add_item_large_quantity(self):
        self.calculator.add_item('Product A', 10.0, 1000000)
        self.assertEqual(self.calculator.total_items(), 1000000)

    def test_add_item_large_price(self):
        self.calculator.add_item('Product A', 1000000.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1000000.0)

    def test_calculate_total_precision(self):
        self.calculator.add_item('Product A', 10.99, 3)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 52.7577, places=2)

    def test_apply_discount_precision(self):
        result = self.calculator.apply_discount(99.99, 33.33)
        self.assertAlmostEqual(result, 66.66, places=2)

    def test_calculate_tax_precision(self):
        result = self.calculator.calculate_tax(123.45)
        self.assertAlmostEqual(result, 28.3935, places=2)

    def test_shipping_threshold_boundary(self):
        result1 = self.calculator.calculate_shipping(99.99)
        result2 = self.calculator.calculate_shipping(100.01)
        self.assertEqual(result1, 10.0)
        self.assertEqual(result2, 0.0)