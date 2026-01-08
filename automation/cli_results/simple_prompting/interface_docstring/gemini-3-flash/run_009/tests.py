import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_valid_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -5)

    def test_add_item_mismatched_price(self):
        self.calculator.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5', 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, 1.5)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_boundaries(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, None)

    def test_calculate_shipping_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calculator.calculate_shipping(200.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax(None)

    def test_calculate_total_integration(self):
        self.calculator.add_item('Item1', 40.0, 2)
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 110.7)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Item1', 100.0, 2)
        self.assertAlmostEqual(self.calculator.calculate_total(0.5), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(0.1)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item1', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)

    def test_calculate_total_invalid_type(self):
        self.calculator.add_item('Item1', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.2')

    def test_total_items(self):
        self.calculator.add_item('A', 1.0, 5)
        self.calculator.add_item('B', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_unique(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 1.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())