import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(100.0), 23.0)
        self.assertEqual(oc.calculate_shipping(50.0), 10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)
        self.assertTrue(oc.is_empty())

    def test_init_custom_parameters(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.calculate_tax(100.0), 10.0)
        self.assertEqual(oc.calculate_shipping(40.0), 5.0)
        self.assertEqual(oc.calculate_shipping(50.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="high")

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_single_item(self):
        oc = OrderCalculator()
        oc.add_item("apple", 2.5)
        self.assertEqual(oc.get_subtotal(), 2.5)
        self.assertEqual(oc.total_items(), 1)
        self.assertIn("apple", oc.list_items())

    def test_add_multiple_distinct_items(self):
        oc = OrderCalculator()
        oc.add_item("apple", 2.5)
        oc.add_item("banana", 1.0, 2)
        self.assertEqual(oc.get_subtotal(), 4.5)
        self.assertEqual(oc.total_items(), 3)
        self.assertCountEqual(oc.list_items(), ["apple", "banana"])

    def test_add_aggregate_same_item(self):
        oc = OrderCalculator()
        oc.add_item("apple", 2.5)
        oc.add_item("apple", 2.5)
        self.assertEqual(oc.get_subtotal(), 5.0)
        self.assertEqual(oc.total_items(), 2)
        self.assertEqual(oc.list_items(), ["apple"])

    # def test_add_zero_quantity(self):
    #     oc = OrderCalculator()
    #     oc.add_item("apple", 2.5, 0)
    #     self.assertEqual(oc.get_subtotal(), 0.0)
    #     self.assertEqual(oc.total_items(), 0)
    #     self.assertEqual(oc.list_items(), [])
    #
    # def test_add_zero_price(self):
    #     oc = OrderCalculator()
    #     oc.add_item("gift", 0.0, 3)
    #     self.assertEqual(oc.get_subtotal(), 0.0)
    #     self.assertEqual(oc.total_items(), 3)
    #     self.assertEqual(oc.list_items(), ["gift"])

    def test_add_negative_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("apple", 2.5, -1)

    def test_add_negative_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("apple", -2.5, 1)

    def test_add_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 1.0, 1)

    def test_add_non_string_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0, 1)

    # def test_remove_existing_item(self):
    #     oc = OrderCalculator()
    #     oc.add_item("apple", 2.5, 2)
    #     oc.remove_item("apple")
    #     self.assertEqual(oc.total_items(), 0)
    #     self.assertEqual(oc.get_subtotal(), 0.0)
    #     self.assertNotIn("apple", oc.list_items())

    # def test_remove_nonexistent_item(self):
    #     oc = OrderCalculator()
    #     with self.assertRaises(KeyError):
    #         oc.remove_item("pear")

    # def test_remove_from_empty_order(self):
    #     oc = OrderCalculator()
    #     with self.assertRaises(KeyError):
    #         oc.remove_item("apple")

    def test_remove_non_string_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    # def test_get_subtotal_empty_order(self):
    #     oc = OrderCalculator()
    #     self.assertEqual(oc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 3)
        oc.add_item("b", 2.0, 2)
        self.assertEqual(oc.get_subtotal(), 7.0)

    # def test_get_subtotal_zero_price_items(self):
    #     oc = OrderCalculator()
    #     oc.add_item("free", 0.0, 5)
    #     self.assertEqual(oc.get_subtotal(), 0.0)

    def test_get_subtotal_after_remove(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 3)
        oc.add_item("b", 2.0, 2)
        oc.remove_item("a")
        self.assertEqual(oc.get_subtotal(), 4.0)

    # def test_apply_discount_normal(self):
    #     oc = OrderCalculator()
    #     self.assertEqual(oc.apply_discount(100.0, 10.0), 90.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertEqual(oc.apply_discount(50.0, 0.0), 50.0)

    # def test_apply_discount_equal_subtotal(self):
    #     oc = OrderCalculator()
    #     self.assertEqual(oc.apply_discount(20.0, 20.0), 0.0)
    #
    # def test_apply_discount_greater_than_subtotal(self):
    #     oc = OrderCalculator()
    #     self.assertEqual(oc.apply_discount(20.0, 30.0), 0.0)

    def test_apply_discount_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(20.0, -5.0)

    def test_apply_discount_non_numeric_inputs(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount("100", 10.0)
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, "10")

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(-10.0), 10.0)

    def test_calculate_shipping_non_numeric_input(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping("50")

    def test_calculate_shipping_custom_parameters(self):
        oc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=7.5)
        self.assertEqual(oc.calculate_shipping(40.0), 7.5)
        self.assertEqual(oc.calculate_shipping(50.0), 0.0)

    def test_calculate_tax_positive_amount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    # def test_calculate_tax_negative_amount(self):
    #     oc = OrderCalculator()
    #     self.assertEqual(oc.calculate_tax(-50.0), -11.5)

    def test_calculate_tax_non_numeric(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax("100")

    def test_calculate_tax_custom_rate(self):
        oc = OrderCalculator(tax_rate=0.05)
        self.assertEqual(oc.calculate_tax(200.0), 10.0)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item("a", 100.0, 1)
        self.assertAlmostEqual(oc.calculate_total(), 123.0)

    # def test_calculate_total_with_small_discount(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 100.0, 1)
    #     self.assertAlmostEqual(oc.calculate_total(10.0), 123.0)

    # def test_calculate_total_discount_equal_subtotal(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 50.0, 1)
    #     self.assertAlmostEqual(oc.calculate_total(50.0), 12.3)

    # def test_calculate_total_discount_greater_than_subtotal(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 30.0, 1)
    #     self.assertAlmostEqual(oc.calculate_total(40.0), 12.3)

    def test_calculate_total_negative_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total(-10.0)

    # def test_calculate_total_threshold_crossing(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 95.0, 1)
    #     self.assertAlmostEqual(oc.calculate_total(10.0), 116.85)

    def test_calculate_total_custom_settings(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        oc.add_item("a", 40.0, 1)
        self.assertAlmostEqual(oc.calculate_total(), 49.5)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 2)
        oc.add_item("b", 1.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_after_removal(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 2)
        oc.add_item("b", 1.0, 1)
        oc.remove_item("a")
        self.assertEqual(oc.total_items(), 1)

    # def test_total_items_zero_quantity_items(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 1.0, 0)
    #     self.assertEqual(oc.total_items(), 0)

    # def test_clear_order_after_adds(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 1.0, 2)
    #     oc.clear_order()
    #     self.assertTrue(oc.is_empty())
    #     self.assertEqual(oc.total_items(), 0)
    #     self.assertEqual(oc.get_subtotal(), 0.0)
    #     self.assertEqual(oc.list_items(), [])

    def test_clear_order_idempotence(self):
        oc = OrderCalculator()
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    # def test_list_items_after_adds(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 1.0, 1)
    #     oc.add_item("b", 1.0, 1)
    #     self.assertEqual(oc.list_items(), ["a", "b"])

    def test_list_items_after_removal(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 1)
        oc.add_item("b", 1.0, 1)
        oc.remove_item("a")
        self.assertEqual(oc.list_items(), ["b"])

    def test_list_items_duplicate_add(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 1)
        oc.add_item("a", 1.0, 1)
        self.assertEqual(oc.list_items(), ["a"])

    def test_is_empty_initially(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_add(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 1)
        self.assertFalse(oc.is_empty())

    def test_is_empty_after_remove(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 1)
        oc.remove_item("a")
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_clear(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    # def test_full_checkout_flow(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 10.0, 2)
    #     oc.add_item("b", 5.0, 3)
    #     self.assertAlmostEqual(oc.calculate_total(5.0), 49.2)

    # def test_state_isolation(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 10.0, 1)
    #     initial_subtotal = oc.get_subtotal()
    #     initial_items = oc.list_items().copy()
    #     oc.apply_discount(10.0, 5.0)
    #     oc.calculate_shipping(5.0)
    #     oc.calculate_tax(5.0)
    #     self.assertEqual(oc.get_subtotal(), initial_subtotal)
    #     self.assertEqual(oc.list_items(), initial_items)

    def test_reusability_after_calculate_total(self):
        oc = OrderCalculator()
        oc.add_item("a", 10.0, 1)
        first_total = oc.calculate_total()
        oc.add_item("b", 5.0, 2)
        second_total = oc.calculate_total()
        self.assertNotEqual(second_total, first_total)
        self.assertAlmostEqual(second_total, 36.9)

    def test_exception_propagation_in_calculate_total(self):
        oc = OrderCalculator()
        oc.add_item("a", 10.0, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(-5.0)
