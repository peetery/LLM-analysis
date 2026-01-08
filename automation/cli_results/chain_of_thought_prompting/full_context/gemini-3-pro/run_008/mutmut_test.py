import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.oc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.oc.tax_rate, 0.23)
        self.assertEqual(self.oc.free_shipping_threshold, 100.0)
        self.assertEqual(self.oc.shipping_cost, 10.0)
        self.assertEqual(self.oc.items, [])

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_tax_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.oc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.oc.items), 1)
        self.assertEqual(self.oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_update_quantity(self):
        self.oc.add_item('Apple', 1.5, 5)
        self.oc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.oc.items), 1)
        self.assertEqual(self.oc.items[0]['quantity'], 8)

    def test_add_item_price_conflict(self):
        self.oc.add_item('Apple', 1.5, 5)
        with self.assertRaises(ValueError):
            self.oc.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('', 10.0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('Apple', 0.0)

    def test_add_item_invalid_quantity_low(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('Apple', 1.5, 0)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item('Apple', '10')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item('Apple', 10.0, '1')

    def test_remove_item_existing(self):
        self.oc.add_item('Apple', 1.5, 5)
        self.oc.remove_item('Apple')
        self.assertEqual(len(self.oc.items), 0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.oc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.remove_item(123)

    def test_get_subtotal_calculation(self):
        self.oc.add_item('Apple', 2.0, 3)
        self.oc.add_item('Banana', 1.0, 5)
        self.assertAlmostEqual(self.oc.get_subtotal(), 11.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.oc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.oc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.oc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.oc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, 1.5)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.oc.apply_discount('100', 0.2)

    def test_calculate_shipping_below_threshold(self):
        cost = self.oc.calculate_shipping(50.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.oc.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.oc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_shipping('50')

    def test_calculate_tax_normal(self):
        tax = self.oc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_tax('100')

    def test_calculate_total_standard_with_shipping(self):
        self.oc.add_item('Item1', 50.0, 1)
        total = self.oc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_free_shipping(self):
        self.oc.add_item('Item1', 200.0, 1)
        total = self.oc.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_discount_triggers_shipping(self):
        self.oc.add_item('Item1', 110.0, 1)
        total = self.oc.calculate_total(discount=0.1)
        expected_subtotal = 99.0
        expected_shipping = 10.0
        expected_tax = (99.0 + 10.0) * 0.23
        self.assertAlmostEqual(total, expected_subtotal + expected_shipping + expected_tax)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.oc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.oc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.oc.calculate_total(discount='0.2')

    def test_total_items(self):
        self.oc.add_item('A', 10.0, 2)
        self.oc.add_item('B', 5.0, 3)
        self.assertEqual(self.oc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.oc.total_items(), 0)

    def test_clear_order(self):
        self.oc.add_item('A', 10.0, 1)
        self.oc.clear_order()
        self.assertEqual(len(self.oc.items), 0)
        self.assertTrue(self.oc.is_empty())

    def test_list_items(self):
        self.oc.add_item('A', 10.0, 1)
        self.oc.add_item('B', 5.0, 1)
        items = self.oc.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty_true(self):
        self.assertTrue(self.oc.is_empty())

    def test_is_empty_false(self):
        self.oc.add_item('A', 10.0, 1)
        self.assertFalse(self.oc.is_empty())