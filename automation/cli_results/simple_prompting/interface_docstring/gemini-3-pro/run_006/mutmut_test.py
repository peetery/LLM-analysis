import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 5.0)
        self.assertEqual(calc.calculate_shipping(150.0), 15.0)

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 7.5)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -1)

    def test_add_item_same_name_diff_price(self):
        self.calculator.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, '1')

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 2.0)
        self.calculator.remove_item('Apple')
        self.assertNotIn('Apple', self.calculator.list_items())
        self.assertIn('Banana', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 1)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Ghost')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(49.9), 5.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.1), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_standard(self):
        self.calculator.add_item('Item1', 40.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.0), 49.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Item1', 100.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 88.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item1', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_calculate_total_negative_subtotal_case(self):
        pass

    def test_calculate_total_type_error(self):
        self.calculator.add_item('Item1', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 10, 5)
        self.calculator.add_item('B', 20, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 20)
        self.calculator.add_item('A', 10)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())