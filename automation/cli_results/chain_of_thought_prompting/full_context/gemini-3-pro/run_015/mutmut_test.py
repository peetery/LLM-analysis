import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.oc = OrderCalculator()

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.05)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_valid(self):
        self.oc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.oc.items), 1)
        self.assertEqual(self.oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.oc.add_item('Orange', 2.0)
        self.assertEqual(self.oc.items[0]['quantity'], 1)

    def test_add_item_existing_update_quantity(self):
        self.oc.add_item('Apple', 1.5, 10)
        self.oc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.oc.items[0]['quantity'], 15)

    def test_add_item_same_name_diff_price(self):
        self.oc.add_item('Apple', 1.5, 10)
        with self.assertRaises(ValueError):
            self.oc.add_item('Apple', 2.0, 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('', 10.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('Freebie', 0.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.oc.add_item('Apple', 1.5, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.oc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.oc.add_item('Apple', '10.0')
        with self.assertRaises(TypeError):
            self.oc.add_item('Apple', 10.0, '1')

    def test_remove_item_valid(self):
        self.oc.add_item('Apple', 1.5)
        self.oc.add_item('Banana', 2.0)
        self.oc.remove_item('Apple')
        self.assertEqual(len(self.oc.items), 1)
        self.assertEqual(self.oc.items[0]['name'], 'Banana')

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.oc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.oc.add_item('A', 10.0, 2)
        self.oc.add_item('B', 5.0, 4)
        self.assertEqual(self.oc.get_subtotal(), 40.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.oc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.oc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.oc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.oc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.oc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.oc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.oc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.oc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_tax('100')

    def test_calculate_total_standard(self):
        self.oc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.oc.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        self.oc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.oc.calculate_total(), 123.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.oc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.oc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.oc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.oc.total_items(), 0)
        self.oc.add_item('A', 10, 2)
        self.oc.add_item('B', 20, 3)
        self.assertEqual(self.oc.total_items(), 5)

    def test_clear_order(self):
        self.oc.add_item('A', 10)
        self.oc.clear_order()
        self.assertEqual(self.oc.items, [])
        self.assertTrue(self.oc.is_empty())

    def test_list_items(self):
        self.oc.add_item('A', 10)
        self.oc.add_item('B', 20)
        self.oc.add_item('A', 10)
        items = self.oc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.oc.is_empty())
        self.oc.add_item('A', 10)
        self.assertFalse(self.oc.is_empty())