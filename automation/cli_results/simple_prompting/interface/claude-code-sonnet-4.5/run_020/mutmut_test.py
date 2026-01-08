import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        calc.add_item('item', 100.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 110.0)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=10.0)
        calc.add_item('item', 60.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 73.8)

    def test_add_item_single(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.0)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('apple', 1.0, 5)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('apple', 2.0)
        self.assertEqual(self.calculator.get_subtotal(), 2.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('item', -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('item', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('item', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0, 1)

    def test_add_item_duplicate_name(self):
        self.calculator.add_item('apple', 1.0, 2)
        self.calculator.add_item('apple', 1.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('item', 'invalid', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('item', 1.0, 'invalid')

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('apple', 2.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('apple', 1.0, 2)
        self.calculator.add_item('banana', 1.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 6.5)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_percentage(self):
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

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        shipping = self.calculator.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_positive_amount(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('apple', 150.0, 1)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 184.5)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_calculate_total_discount_over_one(self):
        self.calculator.add_item('apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('apple', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('apple', 1.0, 2)
        self.calculator.add_item('banana', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.assertIn('apple', self.calculator.list_items())

    def test_list_items_multiple(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.calculator.add_item('banana', 2.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('apple', items)
        self.assertIn('banana', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calculator.add_item('apple', 1.0, 1)
        self.calculator.remove_item('apple')
        self.assertTrue(self.calculator.is_empty())