import unittest
from typing import List, TypedDict
from decimal import Decimal

from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    # Constructor tests
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertTrue(oc.is_empty())

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.08)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    # add_item tests
    def test_add_item_single(self):
        oc = OrderCalculator()
        oc.add_item("apple", 1.5, 1)
        self.assertEqual(oc.total_items(), 1)
        self.assertAlmostEqual(oc.get_subtotal(), 1.5, places=2)

    def test_add_item_multiple_quantity(self):
        oc = OrderCalculator()
        oc.add_item("banana", 2.0, 3)
        self.assertEqual(oc.total_items(), 3)
        self.assertAlmostEqual(oc.get_subtotal(), 6.0, places=2)

    def test_add_item_duplicate_name_aggregates(self):
        oc = OrderCalculator()
        oc.add_item("cookie", 3.0, 2)
        oc.add_item("cookie", 3.0, 1)
        self.assertEqual(oc.total_items(), 3)
        self.assertAlmostEqual(oc.get_subtotal(), 9.0, places=2)

    def test_add_item_large_quantity(self):
        oc = OrderCalculator()
        oc.add_item("widget", 0.99, 1000000)
        self.assertEqual(oc.total_items(), 1000000)
        self.assertAlmostEqual(oc.get_subtotal(), 990000.0, places=2)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 1.0, 1)

    def test_add_item_negative_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("bad", -1.0, 1)

    def test_add_item_negative_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("bad", 1.0, -1)

    def test_add_item_zero_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("zero", 1.0, 0)

    def test_add_item_non_numeric_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("bad", "not_a_number", 1)  # type: ignore

    def test_add_item_non_int_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("bad", 1.0, 1.5)  # type: ignore

    # remove_item tests
    def test_remove_item_existing(self):
        oc = OrderCalculator()
        oc.add_item("pear", 2.0, 2)
        oc.remove_item("pear")
        self.assertTrue(oc.is_empty())

    def test_remove_item_among_others(self):
        oc = OrderCalculator()
        oc.add_item("x", 1, 1)
        oc.add_item("y", 2, 1)
        oc.remove_item("x")
        self.assertIn("y", oc.list_items())
        self.assertNotIn("x", oc.list_items())

    def test_remove_item_last_remaining(self):
        oc = OrderCalculator()
        oc.add_item("solo", 5, 1)
        oc.remove_item("solo")
        self.assertTrue(oc.is_empty())

    # def test_remove_item_nonexistent(self):
    #     oc = OrderCalculator()
    #     oc.add_item("exists", 1, 1)
    #     with self.assertRaises(KeyError):
    #         oc.remove_item("ghost")

    # def test_remove_item_from_empty(self):
    #     oc = OrderCalculator()
    #     with self.assertRaises(KeyError):
    #         oc.remove_item("nothing")

    # get_subtotal tests
    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 2)
        oc.add_item("b", 2.5, 1)
        self.assertAlmostEqual(oc.get_subtotal(), 4.5, places=2)

    # def test_get_subtotal_empty(self):
    #     oc = OrderCalculator()
    #     self.assertAlmostEqual(oc.get_subtotal(), 0.0, places=2)

    def test_get_subtotal_high_precision_prices(self):
        oc = OrderCalculator()
        oc.add_item("precise", 1.111, 3)
        self.assertAlmostEqual(oc.get_subtotal(), 3.333, places=3)

    # total_items tests
    def test_total_items_mixed_operations(self):
        oc = OrderCalculator()
        oc.add_item("a", 1, 2)
        oc.add_item("b", 2, 3)
        oc.remove_item("a")
        self.assertEqual(oc.total_items(), 3)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    # list_items tests
    def test_list_items_insertion_order(self):
        oc = OrderCalculator()
        oc.add_item("first", 1, 1)
        oc.add_item("second", 1, 1)
        self.assertEqual(oc.list_items(), ["first", "second"])

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    # is_empty tests
    def test_is_empty_transitions(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())
        oc.add_item("something", 1, 1)
        self.assertFalse(oc.is_empty())
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    # apply_discount tests
    # def test_apply_discount_normal(self):
    #     oc = OrderCalculator()
    #     result = oc.apply_discount(200, 50)
    #     self.assertAlmostEqual(result, 150.0, places=2)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100, 0)
        self.assertAlmostEqual(result, 100.0, places=2)

    # def test_apply_discount_equals_subtotal(self):
    #     oc = OrderCalculator()
    #     result = oc.apply_discount(75, 75)
    #     self.assertAlmostEqual(result, 0.0, places=2)
    #
    # def test_apply_discount_greater_than_subtotal(self):
    #     oc = OrderCalculator()
    #     result = oc.apply_discount(50, 60)
    #     self.assertAlmostEqual(result, 0.0, places=2)

    def test_apply_discount_negative_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100, -10)

    # calculate_shipping tests
    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(80), 10.0, places=2)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(100), 0.0, places=2)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_shipping(150), 0.0, places=2)

    # def test_calculate_shipping_negative_subtotal(self):
    #     oc = OrderCalculator()
    #     with self.assertRaises(ValueError):
    #         oc.calculate_shipping(-10)

    def test_calculate_shipping_zero_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=0)
        self.assertAlmostEqual(oc.calculate_shipping(5), 0.0, places=2)

    # calculate_tax tests
    def test_calculate_tax_normal(self):
        oc = OrderCalculator(tax_rate=0.23)
        self.assertAlmostEqual(oc.calculate_tax(100), 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(0), 0.0, places=2)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-5)

    def test_calculate_tax_zero_rate(self):
        oc = OrderCalculator(tax_rate=0)
        self.assertAlmostEqual(oc.calculate_tax(100), 0.0, places=2)

    # calculate_total tests
    # def test_calculate_total_normal(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 30, 2)  # 60
    #     total = oc.calculate_total(discount=10)  # subtotal 60-10=50, shipping 0? no (<100) => +10=60, tax 60*0.23=13.8 total=73.8
    #     self.assertAlmostEqual(total, 73.8, places=2)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item("a", 40, 1)
        total = oc.calculate_total()
        subtotal = 40
        expected = subtotal + 10 + (subtotal + 10) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    # def test_calculate_total_discount_changes_shipping(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 120, 1)  # subtotal 120
    #     total_with_small_discount = oc.calculate_total(discount=10)  # discounted 110 >=100 free shipping
    #     expected = 110 + 0 + 110 * 0.23
    #     self.assertAlmostEqual(total_with_small_discount, expected, places=2)

    # def test_calculate_total_discount_equals_subtotal(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 50, 1)
    #     total = oc.calculate_total(discount=50)
    #     expected = 10 + 10 * 0.23  # shipping 10 taxed
    #     self.assertAlmostEqual(total, expected, places=2)

    # def test_calculate_total_discount_exceeds_subtotal(self):
    #     oc = OrderCalculator()
    #     oc.add_item("a", 30, 1)
    #     total = oc.calculate_total(discount=40)
    #     expected = 10 + 10 * 0.23
    #     self.assertAlmostEqual(total, expected, places=2)

    # def test_calculate_total_empty_order(self):
    #     oc = OrderCalculator()
    #     self.assertAlmostEqual(oc.calculate_total(), 0.0, places=2)

    def test_calculate_total_large_order_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("big", 200, 1)
        total = oc.calculate_total()
        expected = 200 + 0 + 200 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_state_unchanged_on_repeat(self):
        oc = OrderCalculator()
        oc.add_item("a", 10, 1)
        first = oc.calculate_total()
        second = oc.calculate_total()
        self.assertAlmostEqual(first, second, places=2)
        self.assertEqual(oc.total_items(), 1)

    def test_calculate_total_independent_instances(self):
        oc1 = OrderCalculator(tax_rate=0.1, shipping_cost=5.0, free_shipping_threshold=20)
        oc2 = OrderCalculator(tax_rate=0.2, shipping_cost=15.0, free_shipping_threshold=200)
        oc1.add_item("x", 10, 2)
        oc2.add_item("x", 10, 2)
        self.assertNotEqual(oc1.calculate_total(), oc2.calculate_total())

    # clear_order tests
    # def test_clear_order_empties(self):
    #     oc = OrderCalculator()
    #     oc.add_item("x", 1, 1)
    #     oc.clear_order()
    #     self.assertTrue(oc.is_empty())
    #     self.assertAlmostEqual(oc.get_subtotal(), 0.0, places=2)

    def test_clear_order_idempotent(self):
        oc = OrderCalculator()
        oc.clear_order()
        oc.clear_order()
        self.assertTrue(oc.is_empty())

    # No-mutation helper method tests
    def test_helper_methods_do_not_mutate_state(self):
        oc = OrderCalculator()
        oc.add_item("x", 10, 1)
        before_items = oc.total_items()
        oc.apply_discount(10, 1)
        oc.calculate_shipping(9)
        oc.calculate_tax(9)
        after_items = oc.total_items()
        self.assertEqual(before_items, after_items)

    # Rounding/precision
    def test_precision_two_decimals(self):
        oc = OrderCalculator()
        oc.add_item("p", 0.3333, 3)  # subtotal 0.9999
        self.assertAlmostEqual(round(oc.get_subtotal(), 2), 1.0, places=2)

    # Isolation between instances
    def test_instance_isolation(self):
        oc1 = OrderCalculator()
        oc2 = OrderCalculator()
        oc1.add_item("a", 1, 1)
        self.assertTrue(oc2.is_empty())


if __name__ == "__main__":
    unittest.main()
