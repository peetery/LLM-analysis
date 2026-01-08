import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_value_error_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_value_error_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_value_error_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Apple")
        self.assertEqual(self.calc.items[0]["price"], 2.0)
        self.assertEqual(self.calc.items[0]["quantity"], 5)

    def test_add_item_default_quantity(self):
        self.calc.add_item("Apple", 2.0)
        self.assertEqual(self.calc.items[0]["quantity"], 1)

    def test_add_item_increase_quantity(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.calc.add_item("Apple", 2.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 8)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "2.0")

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 2.0, 1.5)

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 2.0)

    def test_add_item_value_error_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0)

    def test_add_item_value_error_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0)

    def test_add_item_value_error_quantity_low(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0, 0)

    def test_add_item_value_error_mismatched_price(self):
        self.calc.add_item("Apple", 2.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 3.0)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 2.0)
        self.calc.add_item("Banana", 1.0)
        self.calc.remove_item("Apple")
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Banana")

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_item_not_found(self):
        self.calc.add_item("Apple", 2.0)
        with self.assertRaises(ValueError):
            self.calc.remove_item("Banana")

    def test_get_subtotal_success(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.calc.add_item("Banana", 1.0, 10)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    def test_apply_discount_type_error_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, None)

    def test_apply_discount_value_error_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_value_error_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_not_free(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)
        self.assertEqual(self.calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("50")

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_tax_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_total_no_discount_no_shipping(self):
        self.calc.add_item("Item", 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_with_discount_and_shipping(self):
        self.calc.add_item("Item", 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 123.0)

    def test_calculate_total_with_discount_no_shipping(self):
        self.calc.add_item("Item", 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 221.4)

    def test_calculate_total_type_error(self):
        self.calc.add_item("Item", 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.1")

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item("A", 1.0, 2)
        self.calc.add_item("B", 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item("A", 1.0)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item("A", 1.0)
        self.calc.add_item("B", 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("A", items)
        self.assertIn("B", items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item("A", 1.0)
        self.assertFalse(self.calc.is_empty())

if __name__ == "__main__":
    unittest.main()