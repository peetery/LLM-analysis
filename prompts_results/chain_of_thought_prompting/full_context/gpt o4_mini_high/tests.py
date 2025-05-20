import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_valid_parameters_zero(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_valid_int_parameters(self):
        calc = OrderCalculator(tax_rate=1, free_shipping_threshold=50, shipping_cost=5)
        self.assertEqual(calc.tax_rate, 1)
        self.assertEqual(calc.free_shipping_threshold, 50)
        self.assertEqual(calc.shipping_cost, 5)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="a")

    def test_init_type_error_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="a")

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="a")

    def test_init_value_error_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_value_error_free_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_normal(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        self.assertEqual(calc.items, [{"name": "A", "price": 10.0, "quantity": 1}])

    def test_add_item_price_int(self):
        calc = OrderCalculator()
        calc.add_item("B", 5, 2)
        self.assertEqual(calc.items, [{"name": "B", "price": 5, "quantity": 2}])

    def test_add_item_quantity_multiple(self):
        calc = OrderCalculator()
        calc.add_item("C", 1.5, 3)
        self.assertEqual(calc.items[0]["quantity"], 3)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.add_item("B", 20.0)
        names = {item["name"] for item in calc.items}
        self.assertEqual(names, {"A", "B"})

    def test_add_item_merge_quantity(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 2)
        calc.add_item("A", 10.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["quantity"], 5)

    def test_add_item_conflicting_price(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        with self.assertRaises(ValueError):
            calc.add_item("A", 12.0)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0, 1)

    def test_add_item_price_non_positive(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("A", 0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("A", -5.0, 1)

    def test_add_item_quantity_less_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("A", 10.0, 0)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("A", "x", 1)

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("A", 10.0, "x")

    def test_remove_item_normal(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.remove_item("A")
        self.assertEqual(calc.items, [])

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Z")

    def test_remove_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_empty_name_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("")

    def test_get_subtotal_normal(self):
        calc = OrderCalculator()
        calc.add_item("A", 5.0, 2)
        calc.add_item("B", 2.5, 4)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_mixed_types(self):
        calc = OrderCalculator()
        calc.add_item("A", 3, 3)
        calc.add_item("B", 2.5, 2)
        self.assertEqual(calc.get_subtotal(), 14.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_normal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(0.0, 0.5), 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_discount_out_of_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_subtotal_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("x", 0.1)

    def test_apply_discount_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "x")

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("x")

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(-10.0), 10.0)

    def test_calculate_tax_normal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("x")

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(1e6), 1e6 * 0.23)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 2)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 36.9)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(), 123.0)

    def test_calculate_total_with_discount_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(0.5), 73.8)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.5), 123.0)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 1)
        self.assertAlmostEqual(calc.calculate_total(1.0), 12.3)

    def test_calculate_total_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_total("x")

    def test_calculate_total_discount_out_of_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_correctness(self):
        calc = OrderCalculator()
        calc.add_item("A", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(0.1), 123.0)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_after_adds_and_merges(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 2.0, 3)
        calc.add_item("A", 1.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_removals(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 1.0, 3)
        calc.remove_item("A")
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_after_adds(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 1)
        calc.clear_order()
        self.assertEqual(calc.items, [])

    def test_clear_order_idempotent(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(calc.items, [])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_multiple_unique(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.add_item("B", 2.0)
        calc.add_item("C", 3.0)
        self.assertEqual(set(calc.list_items()), {"A", "B", "C"})

    def test_list_items_deduplication(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("A", 1.0, 3)
        calc.add_item("B", 2.0)
        self.assertEqual(set(calc.list_items()), {"A", "B"})

    def test_is_empty_initial(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_remove_last(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.remove_item("A")
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
