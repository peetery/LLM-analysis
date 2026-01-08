import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_params(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Laptop')

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 2.0, 2)
        calc.add_item('Pen', 2.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Gift', 0.0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 15.0, 0)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Coffee', 5.0)
        with self.assertRaises(ValueError):
            calc.add_item('Coffee', 6.0)

    def test_add_item_type_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            calc.add_item('Key', 'free')
        with self.assertRaises(TypeError):
            calc.add_item('Key', 10.0, 1.5)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Phone', 500.0)
        calc.remove_item('Phone')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_success(self):
        calc = OrderCalculator()
        calc.add_item('Item A', 10.0, 2)
        calc.add_item('Item B', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('50')

    def test_calculate_total_full_flow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Widget', 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_discount_triggers_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Product', 110.0, 1)
        self.assertEqual(calc.calculate_shipping(110.0), 0.0)
        discounted = calc.apply_discount(110.0, 0.2)
        self.assertEqual(calc.calculate_shipping(discounted), 10.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_type_error(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='high')

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 5)
        calc.add_item('B', 1.0, 3)
        self.assertEqual(calc.total_items(), 8)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(len(calc.items), 0)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Alpha', 1.0)
        calc.add_item('Beta', 2.0)
        calc.add_item('Alpha', 1.0)
        names = calc.list_items()
        self.assertEqual(len(names), 2)
        self.assertIn('Alpha', names)
        self.assertIn('Beta', names)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        self.assertFalse(calc.is_empty())