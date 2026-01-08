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

    def test_init_type_error_tax(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_type_error_shipping(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_value_error_tax_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_value_error_tax_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_value_error_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_normal(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Banana', 0.5)
        self.assertEqual(oc.items[0]['quantity'], 1)

    def test_add_item_existing_increment(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 5)

    def test_add_item_type_error_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', '10.0')

    def test_add_item_type_error_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', 10.0, '5')

    def test_add_item_value_error_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 10.0)

    def test_add_item_value_error_price_non_positive(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 0.0)

    def test_add_item_value_error_quantity_non_positive(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 10.0, 0)

    def test_add_item_value_error_different_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 12.0)

    def test_remove_item_normal(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 10.0)
        oc.remove_item('Apple')
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_type_error_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_remove_item_value_error_not_found(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('NonExistent')

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 10.0, 2)
        oc.add_item('Banana', 5.0, 3)
        self.assertEqual(oc.get_subtotal(), 35.0)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 10.0, 1)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
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

    def test_apply_discount_type_error_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.2)

    def test_apply_discount_type_error_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.2')

    def test_apply_discount_value_error_range(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.5)

    def test_apply_discount_value_error_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_equal_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('50')

    def test_calculate_tax_normal(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_tax_value_error_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10.0)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0)
        oc.add_item('Item1', 100.0, 1)
        self.assertEqual(oc.calculate_total(), 123.0)

    def test_calculate_total_with_discount_below_threshold(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item1', 100.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.5), 66.0)

    def test_calculate_total_with_discount_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0)
        oc.add_item('Item1', 200.0, 1)
        self.assertEqual(oc.calculate_total(discount=0.1), 198.0)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_type_error_discount(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            oc.calculate_total(discount='0.1')

    def test_calculate_total_value_error_discount_range(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            oc.calculate_total(discount=1.5)

    def test_calculate_total_negative_subtotal_check(self):
        oc = OrderCalculator()
        oc.items = [{'name': 'Test', 'price': -100.0, 'quantity': 1}]
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_total_items_populated(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0, 2)
        oc.add_item('B', 5.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_clear_order_populated(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0)
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_clear_order_already_empty(self):
        oc = OrderCalculator()
        oc.clear_order()
        self.assertEqual(len(oc.items), 0)

    def test_list_items_populated(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0)
        oc.add_item('B', 20.0)
        items = oc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    def test_is_empty_initial(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_false_after_add(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0)
        self.assertFalse(oc.is_empty())

    def test_is_empty_true_after_clear(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0)
        oc.clear_order()
        self.assertTrue(oc.is_empty())