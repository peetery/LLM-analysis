import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 15.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 5.0)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calculator.add_item('Apple', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Banana', 3.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 13.0)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_same_name(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Apple', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 5.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 5.0, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -5.0, 1)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 5.0, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 5.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '5.0', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 5.0, '1')

    def test_remove_item_after_multiple_adds(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Banana', 3.0, 1)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.get_subtotal(), 3.0)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Banana', 3.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 19.0)

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

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

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

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Apple', 50.0, 1)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 73.8)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calculator.add_item('Apple', 150.0, 1)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 184.5)

    def test_calculate_total_with_full_discount(self):
        self.calculator.add_item('Apple', 50.0, 1)
        total = self.calculator.calculate_total(1.0)
        self.assertEqual(total, 12.3)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item(self):
        self.calculator.add_item('Apple', 5.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_multiple_quantities(self):
        self.calculator.add_item('Apple', 5.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Banana', 3.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 5.0, 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 5.0, 2)
        self.calculator.add_item('Banana', 3.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_initially(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 5.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_remove(self):
        self.calculator.add_item('Apple', 5.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 5.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())