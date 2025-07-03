import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.tax_rate, 0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)
        self.assertEqual(calc.items, [])

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_free_shipping_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_tax_rate_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-5.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        self.assertEqual(len(calc.items), 1)
        item = calc.items[0]
        self.assertEqual(item["name"], "apple")
        self.assertEqual(item["price"], 1.0)
        self.assertEqual(item["quantity"], 1)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.add_item("banana", 2.0, 2)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0, 3)
        self.assertEqual(calc.items[0]["quantity"], 3)

    def test_add_item_accumulate_quantity(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0, 2)
        calc.add_item("apple", 1.0, 3)
        self.assertEqual(calc.items[0]["quantity"], 5)

    def test_add_item_conflicting_price(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        with self.assertRaises(ValueError):
            calc.add_item("apple", 2.0)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("apple", "1.0")

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("apple", 1.0, 2.5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0)

    def test_add_item_non_positive_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("apple", 0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("apple", 1.0, 0)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.remove_item("apple")
        self.assertEqual(calc.items, [])

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("apple")

    def test_remove_item_updates_state(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.add_item("banana", 2.0)
        calc.remove_item("apple")
        names = [item["name"] for item in calc.items]
        self.assertNotIn("apple", names)

    def test_get_subtotal_with_items(self):
        calc = OrderCalculator()
        calc.add_item("apple", 2.0, 3)
        calc.add_item("banana", 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_mid_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(80.0, 0.25), 60.0)

    def test_apply_discount_subtotal_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("80", 0.2)

    def test_apply_discount_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(80.0, None)

    def test_apply_discount_discount_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(80.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(80.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(200.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-5.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax([100])

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("apple", 10.0, 2)
        self.assertEqual(calc.calculate_total(0.0), 33.0)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=20.0, shipping_cost=10.0)
        calc.add_item("apple", 10.0, 2)
        self.assertEqual(calc.calculate_total(0.0), 22.0)

    def test_calculate_total_with_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item("apple", 10.0, 5)
        self.assertEqual(calc.calculate_total(0.2), 49.5)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=30.0, shipping_cost=5.0)
        calc.add_item("apple", 10.0, 5)
        self.assertEqual(calc.calculate_total(0.4), 33.0)

    def test_calculate_total_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_total("0.1")

    def test_calculate_total_invalid_discount_value(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0, 2)
        calc.add_item("banana", 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_after_adding(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_idempotent(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_unique(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.add_item("banana", 2.0)
        self.assertCountEqual(calc.list_items(), ["apple", "banana"])

    def test_list_items_duplicates(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.add_item("apple", 1.0)
        self.assertCountEqual(calc.list_items(), ["apple"])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())