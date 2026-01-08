import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_total(), 0.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        calc.add_item('Item', 100.0)
        self.assertAlmostEqual(calc.calculate_total(), 125.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 79.95)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('Item', 51.0)
        self.assertAlmostEqual(calc.calculate_total(), 62.73)

    def test_add_item_single(self):
        self.calc.add_item('Book', 29.99)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calc.add_item('Book', 29.99, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_multiple_different(self):
        self.calc.add_item('Book', 29.99)
        self.calc.add_item('Pen', 5.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_same_name_increments_quantity(self):
        self.calc.add_item('Book', 29.99, 2)
        self.calc.add_item('Book', 29.99, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_zero_quantity(self):
        self.calc.add_item('Book', 29.99, 0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Book', 29.99, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Book', -29.99)

    def test_add_item_zero_price(self):
        self.calc.add_item('Free Item', 0.0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 29.99)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Book', 'invalid')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Book', 29.99, 'invalid')

    def test_remove_item_existing(self):
        self.calc.add_item('Book', 29.99)
        self.calc.remove_item('Book')
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Nonexistent')

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Book', 29.99)
        self.assertAlmostEqual(self.calc.get_subtotal(), 29.99)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Book', 29.99, 2)
        self.calc.add_item('Pen', 5.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 74.98)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        result = self.calc.apply_discount(100.0, 50.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_hundred(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 101.0)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, 'invalid')

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        shipping = self.calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('invalid')

    def test_calculate_total_empty_order(self):
        total = self.calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Book', 100.0)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Book', 100.0)
        total = self.calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 110.7)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Book', 50.0)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Book', 150.0)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 184.5)

    def test_calculate_total_negative_discount(self):
        self.calc.add_item('Book', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-5.0)

    def test_calculate_total_over_hundred_discount(self):
        self.calc.add_item('Book', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=105.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single(self):
        self.calc.add_item('Book', 29.99)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_multiple_same(self):
        self.calc.add_item('Book', 29.99, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_different(self):
        self.calc.add_item('Book', 29.99, 2)
        self.calc.add_item('Pen', 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calc.add_item('Book', 29.99, 3)
        self.calc.add_item('Pen', 5.0, 2)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items_empty(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_single(self):
        self.calc.add_item('Book', 29.99)
        items = self.calc.list_items()
        self.assertIn('Book', items)
        self.assertEqual(len(items), 1)

    def test_list_items_multiple(self):
        self.calc.add_item('Book', 29.99)
        self.calc.add_item('Pen', 5.0)
        items = self.calc.list_items()
        self.assertIn('Book', items)
        self.assertIn('Pen', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Book', 29.99)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Book', 29.99)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calc.add_item('Book', 29.99)
        self.calc.remove_item('Book')
        self.assertTrue(self.calc.is_empty())