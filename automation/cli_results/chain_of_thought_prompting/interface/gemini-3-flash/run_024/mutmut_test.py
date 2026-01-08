import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_normal(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertIn('Apple', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free', 0.0)

    def test_add_item_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Debt', -5.0)

    def test_add_item_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 0)

    def test_add_item_different_price_error(self):
        self.calc.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0)

    def test_remove_item_normal(self):
        self.calc.add_item('Apple', 2.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_normal(self):
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Banana', 3.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 7.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_normal(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_out_of_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_out_of_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_normal(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_normal(self):
        self.calc.add_item('Item', 50.0, 1)
        expected_total = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected_total)

    def test_calculate_total_with_discount_threshold_toggle_on(self):
        self.calc.add_item('Item', 90.0, 1)
        self.calc.add_item('Item2', 20.0, 1)
        expected_total = 110.0 * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected_total)

    def test_calculate_total_with_discount_threshold_toggle_off(self):
        self.calc.add_item('Item', 110.0, 1)
        discounted_subtotal = 110.0 * 0.8
        expected_total = (discounted_subtotal + 10.0) * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_normal(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        self.assertEqual(sorted(self.calc.list_items()), ['A', 'B'])

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_flow(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())