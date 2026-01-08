import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_boundary_low(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_boundary_high(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_too_high_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_type_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertIn('Laptop', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_existing_increases_quantity(self):
        self.calc.add_item('Mouse', 25.0, 1)
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_large_quantity(self):
        self.calc.add_item('Screw', 0.1, 1000000)
        self.assertEqual(self.calc.total_items(), 1000000)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)

    def test_add_item_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Gift', 0.0, 1)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Debt', -10.0, 1)

    def test_add_item_invalid_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_add_item_price_conflict_raises_value_error(self):
        self.calc.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 15.0, 1)

    def test_add_item_invalid_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '1')

    def test_remove_item_success(self):
        self.calc.add_item('Phone', 500.0, 1)
        self.calc.remove_item('Phone')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_precision(self):
        self.calc.add_item('Tiny', 0.0001, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.0001)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_standard(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_hundred_percent(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate_low_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.01)

    def test_apply_discount_invalid_rate_high_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.01)

    def test_apply_discount_invalid_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_no_discount_with_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected)

    def test_calculate_total_discount_no_shipping(self):
        self.calc.add_item('Expensive', 200.0, 1)
        discounted_subtotal = 160.0
        shipping = 0.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected)

    def test_calculate_total_discount_triggers_shipping(self):
        self.calc.add_item('Limit', 110.0, 1)
        discounted_subtotal = 88.0
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected)

    def test_calculate_total_zero_total(self):
        self.calc.add_item('Free', 10.0, 1)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(self.calc.calculate_total(1.0), expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        self.calc.add_item('A', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.1)

    def test_calculate_total_invalid_type_raises_type_error(self):
        self.calc.add_item('A', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_multiple(self):
        self.calc.add_item('A', 10.0, 5)
        self.calc.add_item('B', 20.0, 2)
        self.assertEqual(self.calc.total_items(), 7)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique_names(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 1)
        self.calc.add_item('A', 10.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_lifecycle(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_removes_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 10.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())