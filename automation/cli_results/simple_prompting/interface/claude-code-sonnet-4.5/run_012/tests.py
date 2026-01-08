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
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_same_name_multiple_times(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_zero_price(self):
        self.calc.add_item('Free Item', 0.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'invalid', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, 'invalid')

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Nonexistent')

    def test_remove_item_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_multiple_quantities(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 2.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_percentage(self):
        result = self.calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.1)

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
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Apple', 10.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 10.0 * 1.23 + 10.0, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 150.0 * 1.23, places=2)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Apple', 50.0, 2)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 90.0 * 1.23, places=2)

    def test_calculate_total_empty_order(self):
        total = self.calc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_with_full_discount(self):
        self.calc.add_item('Apple', 50.0, 2)
        total = self.calc.calculate_total(discount=1.0)
        self.assertEqual(total, 0.0)

    def test_calculate_total_negative_discount(self):
        self.calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_over_one(self):
        self.calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_multiple_quantities(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 1.0, 3)
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
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
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