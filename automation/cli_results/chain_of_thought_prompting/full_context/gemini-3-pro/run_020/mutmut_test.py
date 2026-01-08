import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom(self):
        oc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.05)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_new(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Banana', 0.5)
        self.assertEqual(oc.items[0]['quantity'], 1)

    def test_add_item_existing_update(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 5)

    def test_add_item_multiple(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.add_item('Banana', 2.0)
        self.assertEqual(len(oc.items), 2)

    def test_add_item_duplicate_name_diff_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
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
        with self.assertRaises(ValueError):
            oc.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 1.0, 0)

    def test_add_item_invalid_types(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            oc.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            oc.add_item('Apple', 1.0, '5')

    def test_remove_item_success(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_from_multiple(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.add_item('Banana', 2.0)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_success(self):
        oc = OrderCalculator()
        oc.add_item('Item1', 10.0, 2)
        oc.add_item('Item2', 5.0, 1)
        self.assertEqual(oc.get_subtotal(), 25.0)

    def test_get_subtotal_single(self):
        oc = OrderCalculator()
        oc.add_item('Item1', 10.0, 1)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_get_subtotal_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_success(self):
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

    def test_apply_discount_invalid_range(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-100.0, 0.1)

    def test_apply_discount_invalid_types(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_exact_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertEqual(oc.calculate_total(), 120.0)

    def test_calculate_total_with_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.1), 120.0)

    def test_calculate_total_free_shipping_via_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 200.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.5), 120.0)

    def test_calculate_total_paid_shipping_via_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.5), 72.0)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_invalid_discount_value(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            oc.calculate_total(discount=1.5)

    def test_calculate_total_invalid_discount_type(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            oc.calculate_total(discount='0.1')

    def test_total_items_multiple(self):
        oc = OrderCalculator()
        oc.add_item('Item1', 10.0, 2)
        oc.add_item('Item2', 5.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_clear_order_success(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_clear_order_already_empty(self):
        oc = OrderCalculator()
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_list_items_unique(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0)
        oc.add_item('B', 1.0)
        items = oc.list_items()
        self.assertCountEqual(items, ['A', 'B'])

    def test_list_items_duplicates_handled(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0)
        oc.add_item('A', 1.0)
        self.assertEqual(oc.list_items(), ['A'])

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