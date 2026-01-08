import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)

    def test_init_tax_rate_low_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_high_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_negative_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_negative_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_shipping_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_new(self):
        self.calculator.add_item("Apple", 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn("Apple", self.calculator.list_items())

    def test_add_item_with_quantity(self):
        self.calculator.add_item("Banana", 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_duplicate_merges(self):
        self.calculator.add_item("Apple", 1.0, 5)
        self.calculator.add_item("Apple", 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_empty_name_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 1.0, 1)

    def test_add_item_zero_price_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Freebie", 0.0, 1)

    def test_add_item_negative_price_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Debt", -1.0, 1)

    def test_add_item_zero_quantity_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.0, 0)

    def test_add_item_negative_quantity_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.0, -5)

    def test_add_item_mismatched_price_error(self):
        self.calculator.add_item("Apple", 1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0, 1)

    def test_add_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0, 1)

    def test_add_item_price_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", "1.0", 1)

    def test_add_item_quantity_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", 1.0, 1.5)

    def test_remove_item_success(self):
        self.calculator.add_item("Apple", 1.0, 1)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Banana")

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_single(self):
        self.calculator.add_item("Apple", 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 6.0)

    def test_get_subtotal_multiple(self):
        self.calculator.add_item("Apple", 2.0, 3)
        self.calculator.add_item("Banana", 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_zero(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_standard(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_negative_subtotal_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_low_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_high_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100", 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("50")

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_positive(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax(None)

    def test_calculate_total_standard(self):
        self.calculator.add_item("Widget", 25.0, 2) # subtotal 50.0
        # No discount:
        # discounted subtotal: 50.0
        # shipping: 10.0
        # basis: 60.0
        # tax: 60.0 * 0.23 = 13.8
        # total: 60.0 + 13.8 = 73.8
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), 73.8)

    def test_calculate_total_free_shipping_discount(self):
        self.calculator.add_item("Gadget", 100.0, 2) # subtotal 200.0
        # 50% discount:
        # discounted subtotal: 100.0
        # shipping: 0.0 (threshold met)
        # basis: 100.0
        # tax: 100.0 * 0.23 = 23.0
        # total: 100.0 + 23.0 = 123.0
        self.assertAlmostEqual(self.calculator.calculate_total(0.5), 123.0)

    def test_calculate_total_empty_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_error(self):
        self.calculator.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_calculate_total_type_error(self):
        self.calculator.add_item("Item", 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("0.1")

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_multiple(self):
        self.calculator.add_item("A", 1.0, 2)
        self.calculator.add_item("B", 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_non_empty(self):
        self.calculator.add_item("A", 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_already_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_multiple(self):
        self.calculator.add_item("Apple", 1.0, 1)
        self.calculator.add_item("Banana", 1.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Apple", items)
        self.assertIn("Banana", items)

    def test_is_empty_true_new(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false_with_item(self):
        self.calculator.add_item("A", 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_true_after_clear(self):
        self.calculator.add_item("A", 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

if __name__ == '__main__':
    unittest.main()