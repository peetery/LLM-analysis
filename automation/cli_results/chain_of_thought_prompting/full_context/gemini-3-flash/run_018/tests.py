import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(len(self.calc.items), 0)

    def test_init_custom_values(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.tax_rate, 0.1)
        self.assertEqual(custom_calc.free_shipping_threshold, 50.0)
        self.assertEqual(custom_calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_new(self):
        self.calc.add_item("Laptop", 1000.0, 1)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Laptop")
        self.assertEqual(self.calc.items[0]["price"], 1000.0)
        self.assertEqual(self.calc.items[0]["quantity"], 1)

    def test_add_item_increment_quantity(self):
        self.calc.add_item("Mouse", 25.0, 1)
        self.calc.add_item("Mouse", 25.0, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 3)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 10.0, 1)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Pen", 0, 1)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Pen", -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Pen", 10.0, 0)

    def test_add_item_price_mismatch(self):
        self.calc.add_item("Keyboard", 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Keyboard", 55.0, 1)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Pen", "10.0", 1)

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Pen", 10.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item("Item1", 10.0, 1)
        self.calc.add_item("Item2", 20.0, 1)
        self.calc.remove_item("Item1")
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Item2")

    def test_remove_item_missing(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("NonExistent")

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_single_item(self):
        self.calc.add_item("Item", 10.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 21.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item("Item1", 10.0, 1)
        self.calc.add_item("Item2", 20.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    def test_apply_discount_type_error_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_below_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 10.0
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("50.0")

    def test_calculate_tax_normal(self):
        self.calc.tax_rate = 0.2
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_no_discount(self):
        self.calc.add_item("Item", 100.0, 1)
        self.calc.free_shipping_threshold = 200.0
        self.calc.shipping_cost = 10.0
        self.calc.tax_rate = 0.1
        expected_total = (100.0 + 10.0) + (100.0 + 10.0) * 0.1
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected_total)

    def test_calculate_total_with_discount(self):
        self.calc.add_item("Item", 200.0, 1)
        self.calc.free_shipping_threshold = 150.0
        self.calc.shipping_cost = 10.0
        self.calc.tax_rate = 0.1
        discounted_subtotal = 200.0 * 0.5
        shipping = 10.0
        expected_total = (discounted_subtotal + shipping) * 1.1
        self.assertAlmostEqual(self.calc.calculate_total(0.5), expected_total)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item("Item", 200.0, 1)
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 10.0
        self.calc.tax_rate = 0.1
        expected_total = 200.0 + 200.0 * 0.1
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.1)

    def test_calculate_total_type_error_discount(self):
        self.calc.add_item("Item", 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.1")

    def test_total_items_calculation(self):
        self.calc.add_item("Item1", 10.0, 2)
        self.calc.add_item("Item2", 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order_functionality(self):
        self.calc.add_item("Item", 10.0, 1)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items_unique_names(self):
        self.calc.add_item("A", 10.0, 1)
        self.calc.add_item("B", 10.0, 1)
        self.calc.add_item("A", 10.0, 2)
        names = self.calc.list_items()
        self.assertEqual(len(names), 2)
        self.assertIn("A", names)
        self.assertIn("B", names)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item("Item", 10.0, 1)
        self.assertFalse(self.calc.is_empty())

if __name__ == "__main__":
    unittest.main()