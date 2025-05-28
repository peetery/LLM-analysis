import unittest

try:
    from order_calculator import OrderCalculator
except ImportError:
    from OrderCalculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def test_init_valid_default(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(oc.is_empty())

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_invalid_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_init_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_add_item_single(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 1.5, 2)
        self.assertEqual(oc.total_items(), 2)

    def test_add_item_duplicate_same_price(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 1.0, 1)
        oc.add_item("Apple", 1.0, 2)
        self.assertEqual(oc.total_items(), 3)

    def test_add_item_duplicate_different_price(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 1.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item("Apple", 2.0, 1)

    def test_add_item_invalid_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 1.0, 1)

    def test_add_item_invalid_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("Apple", 0, 1)

    def test_add_item_invalid_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("Apple", 1.0, 0)

    def test_add_item_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, "1.0", "two")

    def test_remove_item_existing(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 1.0, 1)
        oc.remove_item("Apple")
        self.assertTrue(oc.is_empty())

    def test_remove_item_non_existing(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item("Banana")

    def test_remove_item_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_non_empty(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 1.0, 2)
        oc.add_item("Banana", 2.0, 1)
        self.assertAlmostEqual(oc.get_subtotal(), 4.0)

    def test_get_subtotal_empty_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_valid(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-1.0, 0.2)

    def test_apply_discount_invalid_discount_low(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_high(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount("100", "0.2")

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping("100")

    def test_calculate_tax_valid_amount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax("100")

    def test_calculate_total_typical(self):
        oc = OrderCalculator()
        oc.add_item("Item", 20.0, 2)
        expected_subtotal = 40.0
        discounted_subtotal = expected_subtotal * 0.9
        shipping = 10.0
        taxable = discounted_subtotal + shipping
        expected_total = taxable + taxable * 0.23
        self.assertAlmostEqual(oc.calculate_total(0.1), expected_total, places=2)

    def test_calculate_total_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("Item", 100.0, 1)
        taxable = 100.0
        expected_total = taxable + taxable * 0.23
        self.assertAlmostEqual(oc.calculate_total(), expected_total, places=2)

    def test_calculate_total_invalid_discount(self):
        oc = OrderCalculator()
        oc.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(1.5)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_type_error(self):
        oc = OrderCalculator()
        oc.add_item("Item", 10.0, 1)
        with self.assertRaises(TypeError):
            oc.calculate_total("0.1")

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_multiple(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 2)
        oc.add_item("B", 2.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    def test_list_items_unique(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.add_item("A", 1.0, 1)
        oc.add_item("B", 2.0, 1)
        self.assertCountEqual(oc.list_items(), ["A", "B"])

    def test_is_empty_true(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_false(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        self.assertFalse(oc.is_empty())


if __name__ == "__main__":
    unittest.main()
