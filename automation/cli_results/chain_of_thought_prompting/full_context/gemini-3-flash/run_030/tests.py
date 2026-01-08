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
        custom_calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(custom_calc.tax_rate, 0.1)
        self.assertEqual(custom_calc.free_shipping_threshold, 50.0)
        self.assertEqual(custom_calc.shipping_cost, 5.0)

    def test_init_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_tax_rate_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_threshold_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])

    def test_init_shipping_cost_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_new(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Apple")
        self.assertEqual(self.calc.items[0]["quantity"], 5)

    def test_add_item_increase_quantity(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.calc.add_item("Apple", 2.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 8)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 2.0, 1)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0, 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0, 1)

    def test_add_item_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0, 0)

    def test_add_item_price_conflict(self):
        self.calc.add_item("Apple", 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.5, 1)

    def test_add_item_name_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)

    def test_add_item_price_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "2.0", 1)

    def test_add_item_quantity_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 2.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 2.0, 1)
        self.calc.remove_item("Apple")
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("Orange")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_clear_order(self):
        self.calc.add_item("Apple", 2.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_already_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_get_subtotal_success(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.calc.add_item("Orange", 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_range_error_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_range_error_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_subtotal_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    def test_apply_discount_rate_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("100")

    def test_calculate_total_standard(self):
        self.calc.add_item("Item", 50.0, 1)
        expected_subtotal = 50.0
        expected_shipping = 10.0
        expected_tax = (50.0 + 10.0) * 0.23
        expected_total = 50.0 + 10.0 + expected_tax
        self.assertAlmostEqual(self.calc.calculate_total(), expected_total)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item("Item", 100.0, 1)
        expected_subtotal = 100.0
        expected_shipping = 0.0
        expected_tax = 100.0 * 0.23
        expected_total = 100.0 + expected_tax
        self.assertAlmostEqual(self.calc.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calc.add_item("Item", 100.0, 1)
        discount = 0.5
        expected_disc_subtotal = 50.0
        expected_shipping = 10.0
        expected_tax = (50.0 + 10.0) * 0.23
        expected_total = 50.0 + 10.0 + expected_tax
        self.assertAlmostEqual(self.calc.calculate_total(discount), expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item("Item", 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.1")

    def test_total_items_count(self):
        self.calc.add_item("Apple", 2.0, 2)
        self.calc.add_item("Orange", 3.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items_unique_names(self):
        self.calc.add_item("Apple", 2.0, 2)
        self.calc.add_item("Orange", 3.0, 1)
        items = self.calc.list_items()
        self.assertIn("Apple", items)
        self.assertIn("Orange", items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item("Apple", 2.0, 1)
        self.assertFalse(self.calc.is_empty())

if __name__ == '__main__':
    unittest.main()