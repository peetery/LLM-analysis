import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom_valid(self):
        calc = OrderCalculator(0.05, 50.0, 5.0)
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

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_add_item_success(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 5.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Apple', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 10.0, -1)

    def test_add_item_different_price_conflict(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 12.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '10.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 10.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Orange')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_paid(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)
        self.assertEqual(self.calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_free_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_free_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-5.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_basic_paid_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 72.0)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 120.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

    def test_total_items_multiple_items(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 15)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique_names(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 10.0)
        self.calc.add_item('A', 10.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())