import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_tax_rate_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_tax_rate_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_existing_same_price(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 8)

    def test_add_item_existing_different_price(self):
        self.calc.add_item('Apple', 1.5, 5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_add_item_invalid_price_zero_or_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free', 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Paying You', -5.0)

    def test_add_item_invalid_quantity_low(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_standard(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax_standard(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_standard_flow(self):
        self.calc.add_item('Item', 80.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 108.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 120.0)

    def test_calculate_total_discount_causes_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 120.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='high')

    def test_total_items(self):
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1)
        self.assertFalse(self.calc.is_empty())

    def test_clear_order(self):
        self.calc.add_item('A', 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.items, [])

    def test_list_items(self):
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 5)
        self.calc.add_item('A', 10)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)