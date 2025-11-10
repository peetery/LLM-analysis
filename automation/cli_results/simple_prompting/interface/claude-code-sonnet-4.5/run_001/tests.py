import unittest
from order_calculator import OrderCalculator, Item

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
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple_different(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_same_name_accumulates(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_zero_quantity(self):
        self.calc.add_item('Apple', 1.0, 0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)

    def test_add_item_zero_price(self):
        self.calc.add_item('Apple', 0.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_add_item_invalid_type_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_type_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'invalid', 1)

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, 'invalid')

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Apple')

    def test_remove_item_empty_name(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
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

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 10.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_amount(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_total_empty_order(self):
        result = self.calc.calculate_total()
        self.assertEqual(result, 0.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Apple', 10.0, 2)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, (20.0 + 10.0) * 1.23, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 150.0 * 1.23, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        self.calc.add_item('Apple', 10.0, 2)
        result = self.calc.calculate_total(discount=5.0)
        self.assertAlmostEqual(result, (15.0 + 10.0) * 1.23, places=2)

    def test_calculate_total_with_discount_above_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        result = self.calc.calculate_total(discount=30.0)
        self.assertAlmostEqual(result, 120.0 * 1.23, places=2)

    def test_calculate_total_discount_crosses_threshold(self):
        self.calc.add_item('Apple', 60.0, 2)
        result = self.calc.calculate_total(discount=25.0)
        self.assertAlmostEqual(result, (95.0 + 10.0) * 1.23, places=2)

    def test_calculate_total_negative_discount(self):
        self.calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-5.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 3)
        self.calc.add_item('Banana', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items_empty(self):
        result = self.calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single(self):
        self.calc.add_item('Apple', 1.0, 1)
        result = self.calc.list_items()
        self.assertIn('Apple', result)

    def test_list_items_multiple(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        result = self.calc.list_items()
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertEqual(len(result), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_large_quantity(self):
        self.calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(self.calc.total_items(), 1000000)

    def test_large_price(self):
        self.calc.add_item('Diamond', 1000000.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 1000000.0)

    def test_float_price_precision(self):
        self.calc.add_item('Apple', 1.99, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.99, places=2)

    def test_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        calc.add_item('Apple', 100.0, 1)
        result = calc.calculate_total()
        self.assertAlmostEqual(result, 110.0, places=2)

    def test_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('Apple', 60.0, 1)
        result = calc.calculate_total()
        self.assertAlmostEqual(result, 60.0 * 1.23, places=2)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('Apple', 10.0, 1)
        result = calc.calculate_total()
        self.assertAlmostEqual(result, (10.0 + 15.0) * 1.23, places=2)