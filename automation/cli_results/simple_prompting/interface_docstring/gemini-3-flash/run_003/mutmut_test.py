import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_valid_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertIsNotNone(calc)

    def test_init_value_error_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_value_error_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_value_error_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new_item(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Mouse', 25.0, 1)
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_value_error_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Freebie', 0.0)

    def test_add_item_value_error_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Debt', -10.0)

    def test_add_item_value_error_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_add_item_value_error_mismatched_price(self):
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 10.0)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_value_error_missing(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(200.0, 0.15), 170.0)

    def test_apply_discount_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_value_error_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_complex(self):
        self.calc.add_item('A', 30.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 78.72)

    def test_calculate_total_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_type_error_discount(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order_logic(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())