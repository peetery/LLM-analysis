import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(oc.tax_rate, 0.15)
        self.assertEqual(oc.free_shipping_threshold, 200.0)
        self.assertEqual(oc.shipping_cost, 20.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_type_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_value_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_value_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_value_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_invalid_value_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item('Widget', 10.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Widget', 'price': 10.0, 'quantity': 5})

    def test_add_item_default_quantity(self):
        self.calc.add_item('Widget', 10.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.calc.add_item('Widget', 10.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_price_conflict(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 12.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10')
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', 10.0, 1.5)

    def test_remove_item_existing(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.remove_item('Widget')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Nonexistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_clear_order(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])

    def test_list_items(self):
        self.calc.add_item('Widget A', 10.0)
        self.calc.add_item('Widget B', 20.0)
        self.assertCountEqual(self.calc.list_items(), ['Widget A', 'Widget B'])

    def test_total_items(self):
        self.calc.add_item('Widget A', 10.0, 2)
        self.calc.add_item('Widget B', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Widget', 10.0)
        self.assertFalse(self.calc.is_empty())

    def test_get_subtotal_valid(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.calc.add_item('Gadget', 5.0, 4)
        self.assertEqual(self.calc.get_subtotal(), 40.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Widget', 50.0)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Widget', 200.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_calculate_total_discount_triggers_shipping(self):
        self.calc.add_item('Widget', 110.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 134.07)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='free')