import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        c = OrderCalculator()
        self.assertTrue(c.is_empty())
        self.assertEqual(c.total_items(), 0)

    def test_init_custom_values(self):
        c = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(c.is_empty())

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_new(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_add_item_existing_same_price(self):
        self.calc.add_item('Widget', 10.0, 1)
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_add_item_defaults(self):
        self.calc.add_item('Widget', 10.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, -1)

    def test_add_item_same_name_different_price(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 12.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.remove_item('Widget')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_success(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        discounted = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(discounted, 80.0)

    def test_apply_discount_zero(self):
        discounted = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(discounted, 100.0)

    def test_apply_discount_full(self):
        discounted = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(discounted, 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_standard(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_free_exact(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_free_above(self):
        cost = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_custom_rate(self):
        c = OrderCalculator(tax_rate=0.1)
        tax = c.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 10.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_basic(self):
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 200.0)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount_triggering_shipping(self):
        self.calc.add_item('Item', 110.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 134.07)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 5.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_duplicates(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('A', 10.0)
        items = self.calc.list_items()
        self.assertEqual(items, ['A'])

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())