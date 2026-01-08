import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('Item', 60.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 73.8, places=2)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('Item', 10.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 30.75, places=2)

    def test_add_item_single(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 1.0)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 2.0)
        self.assertEqual(self.calc.get_subtotal(), 2.0)

    def test_add_item_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 3.5)

    def test_add_item_update_existing(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_add_item_invalid_type_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_type_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0', 1)

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 4.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_hundred(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 101.0)

    def test_apply_discount_invalid_type_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 10.0)

    def test_apply_discount_invalid_type_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '10')

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

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Apple', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Apple', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8, places=2)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Apple', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 3)
        self.calc.add_item('Banana', 0.5, 2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())