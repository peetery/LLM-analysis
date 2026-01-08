import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(len(self.calc.items), 0)

    def test_init_custom(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.tax_rate, 0.1)
        self.assertEqual(custom_calc.free_shipping_threshold, 50.0)
        self.assertEqual(custom_calc.shipping_cost, 5.0)

    def test_init_type_error_tax(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_type_error_shipping(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_value_error_tax_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_value_error_tax_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_value_error_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Laptop')

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'free')

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, 1.5)

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_value_error_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_add_item_value_error_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)

    def test_add_item_value_error_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_value_error_price_mismatch(self):
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_item_value_error_missing(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Bread', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 11.0)

    def test_get_subtotal_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_type_error_rate(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '10%')

    def test_apply_discount_value_error_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_value_error_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.calc.tax_rate = 0.23
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_success(self):
        self.calc.add_item('Product', 80.0, 1)
        subtotal = 80.0
        discounted = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.23
        expected = 80.0 + 10.0 + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected)

    def test_calculate_total_with_discount_triggering_shipping(self):
        self.calc.add_item('Product', 110.0, 1)
        discounted = 110.0 * 0.9
        self.assertTrue(discounted < 100.0)
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.1), expected)

    def test_calculate_total_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.0)

    def test_calculate_total_type_error_discount(self):
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_count(self):
        self.calc.add_item('Apple', 1.0, 3)
        self.calc.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items_unique(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('Apple', 1.0)
        self.assertFalse(self.calc.is_empty())