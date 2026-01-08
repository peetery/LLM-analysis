import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertIsNotNone(calc)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.0)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Orange', 2.0, 5)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 3.0)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Orange', 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 8.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', -1.0, 1)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', 10.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 'ten', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 10.0, 'one')

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('')

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Item', 10.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Item1', 10.0, 1)
        self.calculator.add_item('Item2', 20.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 50.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_valid(self):
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

    def test_calculate_tax_positive(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        total = self.calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 73.8, places=2)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 100.0, 1)
        total = self.calculator.calculate_total(0.0)
        self.assertEqual(total, 123.0)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Item', 10.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_empty(self):
        items = self.calculator.list_items()
        self.assertEqual(items, [])

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 1.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Orange', 2.0, 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())