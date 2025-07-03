import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.list_items(), [])

    def test_init_custom_params(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_values_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        self.assertEqual(calc.get_subtotal(), 1.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.list_items(), ["apple"])

    def test_add_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item("banana", 2.0, quantity=5)
        self.assertEqual(calc.get_subtotal(), 10.0)
        self.assertEqual(calc.total_items(), 5)

    def test_add_same_item_twice_accumulates_quantity(self):
        calc = OrderCalculator()
        calc.add_item("orange", 1.5, quantity=2)
        calc.add_item("orange", 1.5, quantity=3)
        self.assertEqual(calc.get_subtotal(), 7.5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item("freebie", 0.0)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertIn("freebie", calc.list_items())

    def test_add_item_large_price_and_quantity(self):
        calc = OrderCalculator()
        calc.add_item("expensive", 1e6, quantity=1000)
        self.assertEqual(calc.get_subtotal(), 1e9)
        self.assertEqual(calc.total_items(), 1000)

    def test_add_item_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("bad", -1.0)

    def test_add_item_non_positive_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("bad", 1.0, quantity=0)
        with self.assertRaises(ValueError):
            calc.add_item("bad", 1.0, quantity=-5)

    def test_add_item_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_non_numeric_price_or_quantity_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("item", "one", 1)
        with self.assertRaises(TypeError):
            calc.add_item("item", 1.0, "two")

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.remove_item("apple")
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)
        self.assertNotIn("apple", calc.list_items())

    def test_remove_last_item_makes_order_empty(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.remove_item("apple")
        self.assertTrue(calc.is_empty())

    def test_remove_item_twice_raises_key_error(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.remove_item("apple")
        with self.assertRaises(KeyError):
            calc.remove_item("apple")

    def test_remove_non_string_name_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_nonexistent_item_raises_key_error(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item("ghost")

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_after_adds(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, 2)
        calc.add_item("b", 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 1.0*2 + 2.5*3)

    def test_get_subtotal_after_removals(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, 2)
        calc.remove_item("a")
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item("x", 0.1)
        calc.add_item("y", 0.2)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3, places=7)

    def test_apply_discount_normal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(80.0, 1.0), 0.0)

    def test_apply_discount_over_100_percent_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_non_numeric_discount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.1")

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(0.0, 0.5), 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_threshold_zero_always_free(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(0.0), 0.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_calculate_shipping_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_shipping(-10.0)

    def test_calculate_shipping_non_numeric_input_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("free")

    def test_calculate_tax_normal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-5.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_non_numeric_input_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("100")

    def test_calculate_total_empty_order_no_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_total(), 0.0)

    def test_calculate_total_under_free_shipping_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("item", 50.0)
        self.assertAlmostEqual(calc.calculate_total(), 73.8, places=7)

    def test_calculate_total_over_free_shipping_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("item", 150.0)
        self.assertAlmostEqual(calc.calculate_total(), 150.0*1.23, places=7)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item("a", 50.0)
        calc.add_item("b", 60.0)
        self.assertAlmostEqual(calc.calculate_total(0.1), 134.07, places=2)

    def test_calculate_total_discount_to_zero(self):
        calc = OrderCalculator()
        calc.add_item("item", 50.0)
        self.assertAlmostEqual(calc.calculate_total(1.0), 12.3, places=7)

    def test_calculate_total_invalid_discount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_custom_parameters_combined(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item("a", 30.0)
        self.assertAlmostEqual(calc.calculate_total(0.5), 24.0, places=7)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_adds(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, 3)
        calc.add_item("b", 2.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removals(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, 3)
        calc.remove_item("a")
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item("big", 1.0, 10**6)
        self.assertEqual(calc.total_items(), 10**6)

    def test_clear_order_resets_state(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.list_items(), [])

    def test_clear_order_on_empty_does_not_raise(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_after_adds(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.add_item("b", 2.0)
        self.assertEqual(calc.list_items(), ["a", "b"])

    def test_list_items_duplicate_adds(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.add_item("a", 1.0)
        self.assertEqual(calc.list_items(), ["a"])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.add_item("b", 2.0)
        calc.remove_item("a")
        self.assertEqual(calc.list_items(), ["b"])

    def test_list_items_deterministic_order(self):
        calc = OrderCalculator()
        calc.add_item("b", 1.0)
        calc.add_item("a", 1.0)
        self.assertEqual(calc.list_items(), ["b", "a"])

    def test_is_empty_on_init(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.remove_item("a")
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_full_checkout_workflow(self):
        calc = OrderCalculator()
        calc.add_item("apple", 50.0)
        calc.add_item("banana", 60.0)
        total = calc.calculate_total(0.1)
        self.assertAlmostEqual(total, 134.07, places=2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.list_items(), [])

    def test_mixed_adds_removes_before_total(self):
        calc = OrderCalculator()
        calc.add_item("widget", 10.0, 2)
        calc.add_item("gadget", 5.0)
        calc.remove_item("widget")
        calc.add_item("doodad", 20.0, 3)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 92.25, places=2)

    def test_exception_recovery_state_unchanged(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("bad", -1.0)
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.get_subtotal(), 0.0)