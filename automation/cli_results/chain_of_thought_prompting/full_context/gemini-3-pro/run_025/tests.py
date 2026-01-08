import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

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
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_tax_rate_value_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_value_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_threshold_value_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_shipping_cost_value_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_update_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 5)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 8)

    def test_add_item_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Banana', 0.5)
        self.assertEqual(oc.items[0]['quantity'], 1)

    def test_add_item_invalid_name_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 10.0)

    def test_add_item_invalid_name_value_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 10.0)

    def test_add_item_invalid_price_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', '1.5')

    def test_add_item_invalid_price_value(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 0)

    def test_add_item_invalid_quantity_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', 1.5, '10')

    def test_add_item_invalid_quantity_value(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 1.5, 0)

    def test_add_item_duplicate_name_diff_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 2.0)

    def test_remove_item_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_not_found(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 2.0, 5)
        oc.add_item('Banana', 1.0, 10)
        self.assertEqual(oc.get_subtotal(), 20.0)

    def test_get_subtotal_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_valid(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_type_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_type_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_value_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_value_high(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = oc.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = oc.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = oc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        oc = OrderCalculator(tax_rate=0.2)
        tax = oc.calculate_tax(100.0)
        self.assertEqual(tax, 20.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator(tax_rate=0.2)
        tax = oc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_total_flow(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=10.0)
        oc.add_item('Item1', 100.0, 1)
        total = oc.calculate_total(discount=0.2)
        self.assertEqual(total, 99.0)

    def test_calculate_total_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item1', 200.0, 1)
        total = oc.calculate_total(discount=0.1)
        self.assertEqual(total, 216.0)

    def test_calculate_total_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            oc.calculate_total(discount='0.1')

    def test_calculate_total_negative_subtotal_check(self):
        oc = OrderCalculator()
        oc.items = [{'name': 'Bad', 'price': -50.0, 'quantity': 1}]
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_total_items(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0, 2)
        oc.add_item('B', 1.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0)
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)
        self.assertTrue(oc.is_empty())

    def test_list_items(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0)
        oc.add_item('B', 1.0)
        oc.add_item('A', 1.0)
        items = oc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())
        oc.add_item('A', 1.0)
        self.assertFalse(oc.is_empty())