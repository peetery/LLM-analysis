import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_valid_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Apple', 2.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, 0)

    def test_add_item_conflicting_price(self):
        self.calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'free')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_missing(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 5.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.25), 75.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, None)

    def test_calculate_shipping_with_cost(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_total_no_discount_no_free_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_total_items_multiple_entries(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_uniqueness(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertCountEqual(items, ['A', 'B'])

    def test_is_empty_state(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())