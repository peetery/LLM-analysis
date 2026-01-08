import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_valid_defaults(self):
        c = OrderCalculator()
        self.assertTrue(c.is_empty())

    def test_init_valid_custom(self):
        c = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(c.is_empty())

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Widget', 10.0, 1)
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_add_item_defaults(self):
        self.calc.add_item('Widget', 10.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_name_clash_different_price(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 11.0)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0.0)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', -10.0)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10.0')

    def test_remove_item_valid(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.remove_item('Widget')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_rate_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_rate_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_simple(self):
        self.calc.add_item('A', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 72.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('A', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 216.0)

    def test_calculate_total_discount_causes_shipping(self):
        self.calc.add_item('A', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 120.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.assertEqual(self.calc.total_items(), 2)

    def test_clear_order(self):
        self.calc.add_item('A', 10)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_list_items(self):
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 20)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())