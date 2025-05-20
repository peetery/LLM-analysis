import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        oc = OrderCalculator(0.15, 50.0, 5.0)
        self.assertEqual(oc.tax_rate, 0.15)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_initialization_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_initialization_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10)

    def test_initialization_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_add_single_item_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_add_item_custom_quantity(self):
        oc = OrderCalculator()
        oc.add_item("pen", 2.5, 4)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_add_item_negative_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("book", -5.0)

    def test_add_item_zero_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("book", 0.0)

    def test_add_item_negative_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("book", 5.0, -2)

    def test_add_item_zero_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("book", 5.0, 0)

    def test_add_duplicate_item_names(self):
        oc = OrderCalculator()
        oc.add_item("book", 5.0, 1)
        oc.add_item("book", 5.0, 2)
        self.assertEqual(oc.get_subtotal(), 15.0)

    def test_remove_existing_item(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0)
        oc.remove_item("book")
        self.assertTrue(oc.is_empty())

    def test_remove_nonexistent_item(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0)
        oc.remove_item("pen")
        self.assertFalse(oc.is_empty())

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0, 2)
        oc.add_item("pen", 5.0, 3)
        self.assertEqual(oc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        self.assertEqual(oc.get_subtotal(), 0.0)

    def test_apply_valid_discount(self):
        oc = OrderCalculator()
        discounted = oc.apply_discount(100.0, 0.1)
        self.assertEqual(discounted, 90.0)

    def test_apply_zero_discount(self):
        oc = OrderCalculator()
        discounted = oc.apply_discount(100.0, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_full_discount(self):
        oc = OrderCalculator()
        discounted = oc.apply_discount(100.0, 1.0)
        self.assertEqual(discounted, 0.0)

    def test_apply_excessive_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.5)

    def test_apply_negative_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_shipping_below_threshold(self):
        oc = OrderCalculator()
        shipping = oc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_above_threshold(self):
        oc = OrderCalculator()
        shipping = oc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_at_threshold(self):
        oc = OrderCalculator()
        shipping = oc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_shipping(-10.0)

    def test_calculate_tax_positive_amount(self):
        oc = OrderCalculator()
        tax = oc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        tax = oc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-50.0)

    def test_calculate_total_with_discount(self):
        oc = OrderCalculator()
        oc.add_item("book", 100.0)
        total = oc.calculate_total(0.1)
        expected = (90.0 + 10.0) + 23.0
        self.assertEqual(total, expected)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item("book", 100.0)
        total = oc.calculate_total()
        expected = (100.0 + 0.0) + 23.0
        self.assertEqual(total, 123.0)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        total = oc.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_full_discount(self):
        oc = OrderCalculator()
        oc.add_item("book", 100.0)
        total = oc.calculate_total(1.0)
        expected = (0.0 + 10.0) + 0.0
        self.assertEqual(total, 10.0)

    def test_total_items_count(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0, 2)
        oc.add_item("pen", 5.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_empty_order(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_clear_order_with_items(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0, 2)
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    def test_clear_empty_order(self):
        oc = OrderCalculator()
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    def test_list_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0)
        oc.add_item("pen", 5.0)
        self.assertListEqual(sorted(oc.list_items()), ["book", "pen"])

    def test_list_items_empty_order(self):
        oc = OrderCalculator()
        self.assertListEqual(oc.list_items(), [])

    def test_is_empty_true(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_false(self):
        oc = OrderCalculator()
        oc.add_item("book", 10.0)
        self.assertFalse(oc.is_empty())


if __name__ == "__main__":
    unittest.main()