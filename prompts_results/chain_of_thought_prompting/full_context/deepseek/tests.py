import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_default_parameters(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_valid_parameters(self):
        calculator = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.15)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_non_numeric_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_init_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_item_default_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0]["quantity"], 1)

    def test_add_item_specific_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(calculator.items[0]["quantity"], 3)

    def test_add_existing_item_same_price(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item1", 10.0, 2)
        self.assertEqual(calculator.items[0]["quantity"], 3)

    def test_add_item_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("", 10.0)

    def test_add_item_non_string_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 10.0)

    def test_add_item_negative_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", -10.0)

    def test_add_item_non_numeric_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Item1", "10.0")

    def test_add_item_zero_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", 10.0, 0)

    def test_add_item_negative_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", 10.0, -1)

    def test_add_item_non_integer_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item("Item1", 10.0, 1.5)

    def test_add_item_same_name_different_price(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        with self.assertRaises(ValueError):
            calculator.add_item("Item1", 15.0)

    def test_remove_existing_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.remove_item("Item1")
        self.assertEqual(len(calculator.items), 0)

    def test_remove_non_existent_item(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item("Item1")

    def test_remove_item_non_string_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_get_subtotal_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertEqual(calculator.get_subtotal(), 30.0)

    def test_get_subtotal_items_with_quantity_gt_1(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(calculator.get_subtotal(), 30.0)

    def test_apply_discount_valid(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero_percent(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_discount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-100.0, 0.2)

    def test_apply_discount_too_high_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_non_numeric_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount("100", 0.2)

    def test_apply_discount_non_numeric_discount(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount(100.0, "0.2")

    def test_calculate_shipping_free_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_paid_shipping(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calculator.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_exact_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_non_numeric_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping("100")

    def test_calculate_tax_positive_amount(self):
        calculator = OrderCalculator(tax_rate=0.23)
        self.assertEqual(calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-100.0)

    def test_calculate_tax_non_numeric_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax("100")

    def test_calculate_total_no_discount_no_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 90.0)
        self.assertEqual(calculator.calculate_total(), 90.0 + 10.0 + (90.0 + 10.0) * 0.23)

    def test_calculate_total_with_discount_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 200.0)
        discounted = 200.0 * 0.8
        self.assertEqual(calculator.calculate_total(0.2), discounted + discounted * 0.23)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount_value(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 100.0)
        with self.assertRaises(ValueError):
            calculator.calculate_total(1.1)

    def test_calculate_total_non_numeric_discount(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 100.0)
        with self.assertRaises(TypeError):
            calculator.calculate_total("0.2")

    def test_total_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_total_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.total_items(), 1)

    def test_total_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertEqual(calculator.total_items(), 2)

    def test_total_items_quantity_gt_1(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(calculator.total_items(), 3)

    def test_clear_order_non_empty(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.clear_order()
        self.assertEqual(len(calculator.items), 0)

    def test_clear_order_empty(self):
        calculator = OrderCalculator()
        calculator.clear_order()
        self.assertEqual(len(calculator.items), 0)

    def test_list_items_empty_order(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.list_items(), [])

    def test_list_items_single_item(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.list_items(), ["Item1"])

    def test_list_items_multiple_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item2", 20.0)
        self.assertCountEqual(calculator.list_items(), ["Item1", "Item2"])

    def test_list_items_duplicate_names(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.add_item("Item1", 10.0)
        self.assertEqual(calculator.list_items(), ["Item1"])

    def test_is_empty_new_order(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_after_adding_items(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        self.assertFalse(calculator.is_empty())

    def test_is_empty_after_clearing_order(self):
        calculator = OrderCalculator()
        calculator.add_item("Item1", 10.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())