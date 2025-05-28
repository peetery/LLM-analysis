import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_free_shipping_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_new(self):
        oc = OrderCalculator()
        oc.add_item("Apple", 2.5, 3)
        self.assertEqual(oc.total_items(), 3)
        self.assertIn("Apple", oc.list_items())
        self.assertEqual(oc.get_subtotal(), 7.5)

    def test_add_item_default_quantity(self):
        oc = OrderCalculator()
        oc.add_item("Banana", 1.0)
        self.assertEqual(oc.total_items(), 1)
        self.assertIn("Banana", oc.list_items())
        self.assertEqual(oc.get_subtotal(), 1.0)

    def test_add_item_increment_existing(self):
        oc = OrderCalculator()
        oc.add_item("Banana", 1.0, 2)
        oc.add_item("Banana", 1.0, 2)
        self.assertEqual(oc.total_items(), 4)
        self.assertEqual(oc.get_subtotal(), 4.0)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 1.0, 1)

    def test_add_item_price_zero(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("X", 0.0, 1)

    def test_add_item_price_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("X", -1.0, 1)

    def test_add_item_quantity_zero(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("X", 1.0, 0)

    def test_add_item_quantity_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("X", 1.0, -1)

    def test_add_item_same_name_different_price(self):
        oc = OrderCalculator()
        oc.add_item("X", 1.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item("X", 2.0, 1)

    def test_add_item_name_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(None, 1.0, 1)

    def test_add_item_price_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("X", "1.0", 1)

    def test_add_item_quantity_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("X", 1.0, 1.5)

    def test_remove_existing_item(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.remove_item("A")
        self.assertTrue(oc.is_empty())

    def test_remove_nonexistent_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item("Z")

    def test_remove_nonexistent_nonempty_order(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        with self.assertRaises(ValueError):
            oc.remove_item("B")

    def test_remove_item_name_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("A", 2.0, 2)
        oc.add_item("B", 3.0, 3)
        self.assertEqual(oc.get_subtotal(), 2*2 + 3*3)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item("A", 5.0, 2)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_no_discount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_typical(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(200.0, 0.25), 150.0)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.1)

    def test_apply_discount_discount_below_zero(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_one(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_subtotal_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount("100", 0.1)

    def test_apply_discount_discount_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, None)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(99.99), oc.shipping_cost)

    def test_calculate_shipping_equal_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(oc.calculate_shipping(0.0), 0.0)

    def test_calculate_shipping_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping(None)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_typical_default_rate(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(100.0), 100.0 * 0.23)

    def test_calculate_tax_typical_custom_rate(self):
        oc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(oc.calculate_tax(50.0), 5.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax("50")

    def test_calculate_total_no_discount_below_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 10.0, 5)
        total = oc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_no_discount_qualify_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 50.0, 4)
        total = oc.calculate_total()
        expected = 200.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_pushes_below_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 60.0, 2)
        total = oc.calculate_total(0.5)
        expected = (60.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_pushes_above_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 100.0, 2)
        total = oc.calculate_total(0.2)
        expected = 160.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_full_discount(self):
        oc = OrderCalculator()
        oc.add_item("A", 50.0, 2)
        total = oc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_invalid_discount_value(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            oc.calculate_total(1.1)

    def test_calculate_total_discount_type_error(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        with self.assertRaises(TypeError):
            oc.calculate_total("0.5")

    def test_total_items_empty_order(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_after_adds(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 2)
        oc.add_item("B", 2.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_clear_order_after_adds(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 2)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.total_items(), 0)
        self.assertEqual(oc.list_items(), [])

    def test_list_items_unique_names(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 2)
        oc.add_item("A", 1.0, 3)
        items = oc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn("A", items)

    def test_list_items_multiple_distinct(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.add_item("B", 2.0, 1)
        items = oc.list_items()
        self.assertCountEqual(items, ["A", "B"])

    def test_list_items_after_removal(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.add_item("B", 2.0, 1)
        oc.remove_item("A")
        self.assertEqual(oc.list_items(), ["B"])

    def test_list_items_empty_order(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    def test_is_empty_initial_state(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_add(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        self.assertFalse(oc.is_empty())

    def test_is_empty_after_remove_last(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.remove_item("A")
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_clear(self):
        oc = OrderCalculator()
        oc.add_item("A", 1.0, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())

if __name__ == "__main__":
    unittest.main()
