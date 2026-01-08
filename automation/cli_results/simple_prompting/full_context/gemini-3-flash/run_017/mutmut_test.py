import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_value_error_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_value_error_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_value_error_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 2.5)
        self.assertEqual(self.calc.items[0]['quantity'], 4)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.2)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_increment_existing(self):
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '10.0')

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 10.0, 1.5)

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_value_error_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, 0)

    def test_add_item_value_error_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_add_item_value_error_price_mismatch(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, 1)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Orange')

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 13.0)

    def test_get_subtotal_empty_order_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_typical(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_none(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_type_error_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_value_error_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_tax_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_complex(self):
        self.calc.add_item('Item', 50.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 123.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 246.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_type_error(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.5')

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.items), 0)

    def test_list_items_uniqueness(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        self.calc.add_item('A', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())