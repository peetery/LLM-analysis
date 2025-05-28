import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    def test_constructor_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_constructor_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_constructor_negative_tax_rate_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_constructor_excessive_tax_rate_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_constructor_negative_free_shipping_threshold_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_constructor_negative_shipping_cost_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_constructor_invalid_parameter_type_exception(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.1")

    def test_add_item_valid_single_item(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_multiple_distinct_items(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.add_item("Pen", 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_same_item_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 1)
        calc.add_item("Book", 10.0, 2)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_empty_name_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0, 1)

    def test_add_item_zero_price_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 0.0, 1)

    def test_add_item_negative_quantity_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 10.0, -1)

    def test_add_item_same_name_different_price_exception(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Book", 12.0, 1)

    def test_add_item_invalid_name_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Book", "ten", 1)

    def test_add_item_invalid_quantity_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Book", 10.0, "one")

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.remove_item("Book")
        self.assertTrue(calc.is_empty())

    def test_remove_nonexistent_item_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Book")

    def test_remove_item_invalid_name_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_from_empty_order_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Book")

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.add_item("Pen", 5.0, 2)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item("Book", 15.0, 2)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_empty_order_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_max_discount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_discount_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_excessive_discount_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_invalid_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_calculate_shipping_free_shipping(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_paid_shipping(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("100")

    def test_calculate_tax_normal_amount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_total_valid_order_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("Book", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(), 123.0)

    # def test_calculate_total_valid_order_with_discount(self):
    #     calc = OrderCalculator()
    #     calc.add_item("Book", 50.0, 2)
    #     self.assertAlmostEqual(calc.calculate_total(0.1), 111.6)

    def test_calculate_total_empty_order_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items_initially_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("Book", 50.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())


if __name__ == "__main__":
    unittest.main()
