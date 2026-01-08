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
        oc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.05)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

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
            OrderCalculator(tax_rate=1.5)

    def test_init_invalid_value_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_value_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_value_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 2})

    def test_add_item_existing_update(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 5)

    def test_add_item_custom_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Banana', 0.5, 10)
        self.assertEqual(oc.items[0]['quantity'], 10)

    def test_add_item_integer_price_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Orange', 1)
        self.assertEqual(oc.items[0]['price'], 1)
        self.assertEqual(oc.items[0]['quantity'], 1)

    def test_add_item_same_name_diff_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 2.0)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 0)

    def test_add_item_invalid_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 1.0, 0)

    def test_add_item_invalid_type_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0)

    def test_add_item_invalid_type_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', '1.0')

    def test_add_item_invalid_type_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', 1.0, '1')

    def test_remove_item_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_non_existent(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0, 2)
        oc.add_item('B', 5.0, 3)
        self.assertEqual(oc.get_subtotal(), 35.0)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0, 1)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_get_subtotal_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_valid(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_value_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_value_high(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_subtotal_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_type_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_type_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_equal_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('99')

    def test_calculate_tax_valid(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_total_integration_no_discount_shipping_applied(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 50.0, 1)
        self.assertEqual(oc.calculate_total(), 72.0)

    def test_calculate_total_integration_discount_causes_shipping(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.1), 120.0)

    def test_calculate_total_integration_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 200.0, 1)
        self.assertEqual(oc.calculate_total(), 240.0)

    def test_calculate_total_full_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertEqual(oc.calculate_total(discount=1.0), 12.0)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_invalid_type_discount(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            oc.calculate_total(discount='0.1')

    def test_total_items_normal(self):
        oc = OrderCalculator()
        oc.add_item('A', 1, 2)
        oc.add_item('B', 1, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item('A', 1)
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)
        self.assertTrue(oc.is_empty())

    def test_list_items(self):
        oc = OrderCalculator()
        oc.add_item('A', 1)
        oc.add_item('B', 2)
        items = oc.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())
        oc.add_item('A', 1)
        self.assertFalse(oc.is_empty())