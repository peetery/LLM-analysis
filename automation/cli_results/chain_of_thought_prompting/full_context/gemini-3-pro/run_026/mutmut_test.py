import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_type_tax(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_type_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_invalid_type_shipping(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_invalid_value_tax_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_value_tax_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_value_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_value_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_normal(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 1})

    def test_add_item_multiple_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Banana', 0.5, quantity=10)
        self.assertEqual(oc.items[0]['quantity'], 10)

    def test_add_item_existing_update(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, quantity=2)
        oc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 5)

    def test_add_item_invalid_type_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 10.0)

    def test_add_item_invalid_type_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Item', '10.0')

    def test_add_item_invalid_type_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Item', 10.0, quantity=1.5)

    def test_add_item_invalid_value_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 10.0)

    def test_add_item_invalid_value_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Item', 0.0)

    def test_add_item_invalid_value_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Item', 10.0, quantity=0)

    def test_add_item_duplicate_name_diff_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_remove_item_not_found(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            oc.remove_item('Banana')

    def test_get_subtotal_multiple(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 2.0, quantity=2)
        oc.add_item('Banana', 1.0, quantity=3)
        self.assertEqual(oc.get_subtotal(), 7.0)

    def test_get_subtotal_single(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 2.0, quantity=1)
        self.assertEqual(oc.get_subtotal(), 2.0)

    def test_get_subtotal_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_normal(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_type_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_type_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_value_range(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('50.0')

    def test_calculate_tax_normal(self):
        oc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(oc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero(self):
        oc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100.0')

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-50.0)

    def test_calculate_total_full_flow(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0)
        self.assertAlmostEqual(oc.calculate_total(discount=0.2), 99.0)

    def test_calculate_total_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=150.0, shipping_cost=10.0)
        oc.add_item('Item', 200.0)
        self.assertAlmostEqual(oc.calculate_total(discount=0.1), 198.0)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 50.0)
        self.assertAlmostEqual(oc.calculate_total(), 66.0)

    def test_calculate_total_invalid_type_discount(self):
        oc = OrderCalculator()
        oc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            oc.calculate_total(discount='0.1')

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_populated(self):
        oc = OrderCalculator()
        oc.add_item('Item A', 10.0, quantity=2)
        oc.add_item('Item B', 20.0, quantity=3)
        self.assertEqual(oc.total_items(), 5)

    def test_clear_order_populated(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_clear_order_already_empty(self):
        oc = OrderCalculator()
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_list_items_populated(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.add_item('Banana', 1.0)
        items = oc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    def test_is_empty_initial(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_false(self):
        oc = OrderCalculator()
        oc.add_item('Item', 1.0)
        self.assertFalse(oc.is_empty())

    def test_is_empty_after_clear(self):
        oc = OrderCalculator()
        oc.add_item('Item', 1.0)
        oc.clear_order()
        self.assertTrue(oc.is_empty())