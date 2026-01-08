import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_tax_rate_boundary_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_tax_rate_boundary_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.calculate_tax(100.0), 100.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_parameter_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_add_item_normal(self):
        self.calc.add_item("Apple", 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn("Apple", self.calc.list_items())

    def test_add_item_custom_quantity(self):
        self.calc.add_item("Apple", 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_increment_quantity(self):
        self.calc.add_item("Apple", 1.0, 2)
        self.calc.add_item("Apple", 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 1.0, 1)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0, 1)

    def test_add_item_invalid_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 1.0, 0)

    def test_add_item_price_mismatch(self):
        self.calc.add_item("Apple", 1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0, 1)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "1.0", 1)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 1.0, 1)
        self.calc.remove_item("Apple")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("Banana")

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item("Apple", 1.0, 2)
        self.calc.add_item("Banana", 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 8.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_normal(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_boundary_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_boundary_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("100")

    def test_calculate_total_no_discount(self):
        self.calc.add_item("Item", 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        expected_total = (subtotal + shipping) * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected_total)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item("Item", 200.0, 1)
        discounted_subtotal = 180.0 # 10% of 200
        shipping = 0.0 # > 100
        expected_total = (discounted_subtotal + shipping) * 1.23
        self.assertAlmostEqual(self.calc.calculate_total(0.1), expected_total)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_total_items_count(self):
        self.calc.add_item("A", 1.0, 10)
        self.calc.add_item("B", 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item("A", 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique_names(self):
        self.calc.add_item("Apple", 1.0, 1)
        self.calc.add_item("Banana", 2.0, 1)
        self.calc.add_item("Apple", 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Apple", items)
        self.assertIn("Banana", items)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item("A", 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item("A")
        self.assertTrue(self.calc.is_empty())

if __name__ == '__main__':
    unittest.main()