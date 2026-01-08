import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.is_empty(), True)

    def test_init_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-0.5)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 10)
        self.assertEqual(calc.total_items(), 10)
        self.assertIn("Apple", calc.list_items())

    def test_add_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Banana", 2.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_existing_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 10)
        calc.add_item("Apple", 1.5, 5)
        self.assertEqual(calc.total_items(), 15)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0, 1)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Apple", -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 1.0, 0)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 2.0, 1)

    def test_add_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Apple", "1.5", 1)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 1)
        calc.remove_item("Apple")
        self.assertEqual(calc.is_empty(), True)

    def test_remove_item_missing(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Orange")

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.5, 4)
        self.assertAlmostEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.5, 4)
        calc.add_item("Banana", 1.0, 5)
        self.assertAlmostEqual(calc.get_subtotal(), 15.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_standard(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_out_of_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertAlmostEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Item", 50.0, 1)
        # subtotal 50, shipping 10, base 60, tax 12, total 72
        self.assertAlmostEqual(calc.calculate_total(0.0), 72.0)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=20.0)
        calc.add_item("Item", 100.0, 1)
        # subtotal 100, discount 0.5 -> 50, shipping 20, base 70, tax 7, total 77
        self.assertAlmostEqual(calc.calculate_total(0.5), 77.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Item", 150.0, 1)
        # subtotal 150, shipping 0, base 150, tax 30, total 180
        self.assertAlmostEqual(calc.calculate_total(0.0), 180.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_total_items_populated(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_clears_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.is_empty(), True)
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 1)
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("A", items)
        self.assertIn("B", items)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_state_changes(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)
        calc.add_item("A", 1.0, 1)
        self.assertEqual(calc.is_empty(), False)
        calc.remove_item("A")
        self.assertEqual(calc.is_empty(), True)

if __name__ == '__main__':
    unittest.main()