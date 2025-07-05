import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()
    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="invalid")

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="invalid")

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="invalid")

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_free_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Item1")
        self.assertEqual(self.calculator.items[0]["price"], 10.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 2)

    def test_add_item_default_quantity(self):
        self.calculator.add_item("Item1", 10.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 1)

    def test_add_item_existing_item(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item1", 10.0, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 5)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item("Item1", 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 15.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", -10.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Item1", 10.0, -1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Item1", "invalid")

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Item1", 10.0, "invalid")

    def test_remove_item(self):
        self.calculator.add_item("Item1", 10.0)
        self.calculator.add_item("Item2", 20.0)
        self.calculator.remove_item("Item1")
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Item2")

    def test_remove_item_nonexistent(self):
        self.calculator.add_item("Item1", 10.0)
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Item2")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item2", 20.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 80.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("invalid", 0.2)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "invalid")

    def test_apply_discount_invalid_discount_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_with_free_shipping(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("invalid")

    def test_calculate_tax(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("invalid")

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item("Item1", 10.0, 2)
        total = self.calculator.calculate_total()
        expected = (20.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item1", 50.0, 2)
        total = self.calculator.calculate_total(0.2)
        discounted = 100.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item("Item1", 100.0, 2)
        total = self.calculator.calculate_total(0.1)
        discounted = 200.0 * 0.9
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item("Item1", 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("invalid")

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item2", 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item("Item1", 10.0)
        self.calculator.add_item("Item2", 20.0)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items(self):
        self.calculator.add_item("Item1", 10.0)
        self.calculator.add_item("Item2", 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Item1", items)
        self.assertIn("Item2", items)

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_duplicates(self):
        self.calculator.add_item("Item1", 10.0, 2)
        self.calculator.add_item("Item1", 10.0, 3)
        self.calculator.add_item("Item2", 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("Item1", 10.0)
        self.assertFalse(self.calculator.is_empty())

if __name__ == "main":
    unittest.main()