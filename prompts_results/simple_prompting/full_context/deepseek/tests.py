import unittest
from typing import List
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertEqual(calculator.items, [])

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_free_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Item1")
        self.assertEqual(self.calculator.items[0]["price"], 10.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 2)

    def test_add_item_duplicate_increases_quantity(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 5)

    def test_add_item_duplicate_different_price(self):
        self.calculator.add_item("Item1", 10.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 15.0, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Item1", "10.0", 1)

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", -10.0, 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Item1", 10.0, "1")

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 10.0, 0)

    def test_remove_item_valid(self):
        self.calculator.add_item("Item1", 10.0, 1)
        self.calculator.remove_item("Item1")
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Item1")

    def test_remove_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item2", 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100.0", 0.1)

    def test_apply_discount_invalid_subtotal_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "0.1")

    def test_apply_discount_invalid_discount_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_not_free(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("100.0")

    def test_calculate_tax_valid(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("100.0")

    def test_calculate_tax_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_valid(self):
        self.calculator.add_item("Item1", 10.0, 2)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 24.6)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item1", 100.0, 1)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 101.43)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item("Item1", 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount="0.1")

    def test_total_items(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item2", 5.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item("Item1", 10.0, 1)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items(self):
        self.calculator.add_item("Item1", 10.0, 1)
        self.calculator.add_item("Item2", 5.0, 1)
        self.calculator.add_item("Item1", 10.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Item1", items)
        self.assertIn("Item2", items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("Item1", 10.0, 1)
        self.assertFalse(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()