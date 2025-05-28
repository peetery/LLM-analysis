import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.items, [])

    def test_init_custom_params(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)
        self.assertTrue(oc.is_empty())

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.1')

    def test_init_invalid_tax_rate_value_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_value_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_free_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item(self):
        oc = OrderCalculator()
        oc.add_item('apple', 1.0, 2)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['name'], 'apple')
        self.assertEqual(oc.items[0]['price'], 1.0)
        self.assertEqual(oc.items[0]['quantity'], 2)

    def test_add_multiple_same_item_increases_quantity(self):
        oc = OrderCalculator()
        oc.add_item('banana', 0.5, 3)
        oc.add_item('banana', 0.5, 2)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price(self):
        oc = OrderCalculator()
        oc.add_item('orange', 1.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item('orange', 1.5, 1)

    def test_add_item_invalid_name_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0, 1)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 1.0, 1)

    def test_add_item_invalid_price_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('pear', '1.0', 1)

    def test_add_item_price_non_positive(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('pear', 0, 1)

    def test_add_item_invalid_quantity_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('pear', 1.0, 1.5)

    def test_add_item_quantity_less_than_one(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('pear', 1.0, 0)

    def test_remove_existing_item(self):
        oc = OrderCalculator()
        oc.add_item('apple', 1.0, 1)
        oc.remove_item('apple')
        self.assertTrue(oc.is_empty())

    def test_remove_nonexistent_item(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('ghost')

    def test_remove_item_invalid_name_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item('apple', 2.0, 3)
        self.assertEqual(oc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 2)
        oc.add_item('b', 2.5, 4)
        self.assertEqual(oc.get_subtotal(), 1.0*2 + 2.5*4)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_typical(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100.0, 0.2), 80.0, places=2)

    def test_apply_discount_zero_discount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(50.0, 0.0), 50.0, places=2)

    def test_apply_discount_full_discount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(50.0, 1.0), 0.0, places=2)

    def test_apply_discount_invalid_subtotal_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.1')

    def test_apply_discount_discount_out_of_range_low(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_out_of_range_high(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.5)

    def test_calculate_shipping_free(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('50')

    def test_calculate_tax_typical(self):
        oc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(oc.calculate_tax(100.0), 10.0, places=2)

    def test_calculate_tax_zero(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(oc.calculate_tax(0.0), 0.0, places=2)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-1.0)

    def test_calculate_total_no_discount_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item('item', 100.0, 1)
        total = oc.calculate_total()
        expected = 100.0 + 0.0 + 100.0*0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        oc = OrderCalculator()
        oc.add_item('item', 50.0, 1)
        total = oc.calculate_total(0.1)
        discounted = 50.0 * 0.9
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax, places=2)

    def test_calculate_total_with_discount_shipping_free(self):
        oc = OrderCalculator()
        oc.add_item('item', 200.0, 1)
        total = oc.calculate_total(0.5)
        discounted = 200.0 * 0.5
        shipping = 0.0
        tax = discounted * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax, places=2)

    def test_calculate_total_invalid_discount_type(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 1)
        with self.assertRaises(TypeError):
            oc.calculate_total('0.1')

    def test_calculate_total_discount_out_of_range(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(1.1)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_multiple(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 2)
        oc.add_item('b', 2.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.items, [])

    def test_list_items_unique(self):
        oc = OrderCalculator()
        oc.add_item('x', 1.0, 1)
        oc.add_item('y', 2.0, 1)
        oc.add_item('x', 1.0, 2)
        items = oc.list_items()
        self.assertCountEqual(items, ['x', 'y'])

    def test_is_empty_true(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_false(self):
        oc = OrderCalculator()
        oc.add_item('a', 1.0, 1)
        self.assertFalse(oc.is_empty())

if __name__ == '__main__':
    unittest.main()
