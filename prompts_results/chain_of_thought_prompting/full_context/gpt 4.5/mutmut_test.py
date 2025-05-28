import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)

    def test_custom_valid_initialization(self):
        oc = OrderCalculator(0.15, 200.0, 5.0)
        self.assertEqual(oc.tax_rate, 0.15)
        self.assertEqual(oc.free_shipping_threshold, 200.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_boundary_tax_rate_zero(self):
        oc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(oc.tax_rate, 0.0)

    def test_boundary_tax_rate_one(self):
        oc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(oc.tax_rate, 1.0)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_tax_rate_out_of_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_constructor_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_add_single_valid_item(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 2)
        self.assertEqual(oc.total_items(), 2)

    def test_add_multiple_different_items(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 1)
        oc.add_item('item2', 20.0, 2)
        self.assertEqual(oc.total_items(), 3)

    def test_add_same_item_twice_same_price(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 1)
        oc.add_item('item1', 10.0, 2)
        self.assertEqual(oc.total_items(), 3)

    def test_add_same_item_twice_different_price(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item('item1', 15.0, 1)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 10.0, 1)

    def test_add_item_nonpositive_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('item1', 0.0, 1)

    def test_add_item_invalid_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('item1', 10.0, 0)

    def test_add_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('item1', 'invalid', 1)

    def test_remove_existing_item(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 1)
        oc.remove_item('item1')
        self.assertTrue(oc.is_empty())

    def test_remove_nonexistent_item(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('item1')

    def test_remove_item_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item('item1', 10.0, 1)
        oc.add_item('item2', 20.0, 2)
        self.assertEqual(oc.get_subtotal(), 50.0)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item('item1', 15.0, 2)
        self.assertEqual(oc.get_subtotal(), 30.0)

    def test_get_subtotal_high_precision_prices(self):
        oc = OrderCalculator()
        oc.add_item('item1', 0.3333, 3)
        self.assertAlmostEqual(oc.get_subtotal(), 0.9999, places=4)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_valid_discount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_zero_discount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_maximum_discount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_invalid_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-50.0, 0.1)

    def test_apply_discount_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(-1.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        oc = OrderCalculator(0.2)
        self.assertEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_rate(self):
        oc = OrderCalculator(0.0)
        self.assertEqual(oc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item('item1', 50.0, 2)
        self.assertEqual(oc.calculate_total(), 123.0)

    # def test_calculate_total_with_discount(self):
    #     oc = OrderCalculator()
    #     oc.add_item('item1', 50.0, 2)
    #     self.assertEqual(oc.calculate_total(0.1), 112.0)


if __name__ == '__main__':
    unittest.main()
