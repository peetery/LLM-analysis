import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertAlmostEqual(self.calculator.tax_rate, 0.23)
        self.assertAlmostEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_configuration(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.tax_rate, 0.1)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_greater_than_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertEqual(self.calculator.list_items(), ['Apple'])

    def test_add_item_existing(self):
        self.calculator.add_item('Apple', 1.5, 5)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Freebie', 0.0)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Debt', -5.0)

    def test_add_item_invalid_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, 0)

    def test_add_item_price_mismatch(self):
        self.calculator.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)

    def test_remove_item_valid(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Ghost')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 1.0, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 8.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_boundary_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_boundary_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.2)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_calculate_tax_invalid_amount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item1', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item1', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_total_items_valid(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 20, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 20)
        items = self.calculator.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())