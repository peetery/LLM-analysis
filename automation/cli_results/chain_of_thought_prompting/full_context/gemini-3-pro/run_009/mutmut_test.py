import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='50')

    def test_init_invalid_shipping_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='5')

    def test_init_tax_rate_underflow(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_overflow(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Widget', 'price': 10.0, 'quantity': 2})

    def test_add_item_default_quantity(self):
        self.calc.add_item('Widget', 10.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_existing_increment(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.calc.add_item('Widget', 10.0, 3)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10.0')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', 10.0, '2')

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', -10.0)

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)

    def test_add_item_duplicate_name_diff_price(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 12.0)

    def test_remove_item_valid(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.remove_item('Widget')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_not_exist(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_overflow(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_standard(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 246.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 10.0)
        self.calc.add_item('A', 10.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())