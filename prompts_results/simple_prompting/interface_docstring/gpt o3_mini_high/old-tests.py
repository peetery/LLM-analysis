import unittest
from typing import List
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_valid(self):
        calc = OrderCalculator(0.2, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.2)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(1.1)

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(0.2, -10.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(0.2, 50.0, -5.0)

    def test_add_item_typical(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.assertIn("Widget", self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_merge_quantities(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.calc.add_item("Widget", 10.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", 0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", 10.0, -1)

    def test_add_item_conflicting_price(self):
        self.calc.add_item("Widget", 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", 12.0, 1)

    def test_add_item_non_string_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item(123, 10.0, 1)

    def test_add_item_non_numeric_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", "10", 1)

    def test_add_item_non_integer_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Widget", 10.0, "2")

    def test_remove_item_typical(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.calc.remove_item("Widget")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("NonExistent")

    def test_get_subtotal_typical(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.calc.add_item("Gadget", 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 10.0 * 2 + 5.0 * 3)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_typical(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_edge_cases(self):
        result_no_discount = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result_no_discount, 100.0)
        result_full_discount = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result_full_discount, 0.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_discount_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_discount_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_free(self):
        cost = self.calc.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_not_free(self):
        cost = self.calc.calculate_shipping(50.0)
        self.assertEqual(cost, self.calc.shipping_cost)

    def test_calculate_shipping_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-10.0)

    def test_calculate_tax_typical(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0 * self.calc.tax_rate)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-50.0)

    def test_calculate_total_typical(self):
        self.calc.add_item("Widget", 20.0, 2)
        self.calc.add_item("Gadget", 30.0, 1)
        subtotal = self.calc.get_subtotal()
        discount = 0.1
        discounted = self.calc.apply_discount(subtotal, discount)
        shipping = self.calc.calculate_shipping(discounted)
        tax = self.calc.calculate_tax(discounted + shipping)
        expected_total = discounted + shipping + tax
        total = self.calc.calculate_total(discount)
        self.assertAlmostEqual(total, expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.1)

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item("Widget", 20.0, 2)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.1)

    def test_total_items(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.calc.add_item("Gadget", 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item("Widget", 10.0, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items(self):
        self.calc.add_item("Widget", 10.0, 1)
        self.calc.add_item("Gadget", 5.0, 1)
        self.calc.add_item("Widget", 10.0, 2)
        items = self.calc.list_items()
        self.assertEqual(set(items), {"Widget", "Gadget"})

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item("Widget", 10.0, 1)
        self.assertFalse(self.calc.is_empty())

if __name__ == "__main__":
    unittest.main()
