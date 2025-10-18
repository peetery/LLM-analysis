import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = OrderCalculator()
    
    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(150), 0.0)
    
    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 15.0)
        self.assertEqual(calc.calculate_shipping(250), 0.0)
    
    def test_add_item_single(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.5)
        self.assertEqual(self.calculator.total_items(), 1)
    
    def test_add_item_multiple_quantity(self):
        self.calculator.add_item("Apple", 1.5, 5)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)
        self.assertEqual(self.calculator.total_items(), 5)
    
    def test_add_item_default_quantity(self):
        self.calculator.add_item("Apple", 2.0)
        self.assertEqual(self.calculator.get_subtotal(), 2.0)
        self.assertEqual(self.calculator.total_items(), 1)
    
    def test_add_item_multiple_different(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)
        self.assertEqual(self.calculator.total_items(), 5)
    
    def test_add_item_same_name_multiple_times(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Apple", 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)
    
    def test_add_item_zero_price(self):
        self.calculator.add_item("Free Item", 0.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
    
    def test_add_item_zero_quantity(self):
        self.calculator.add_item("Apple", 1.5, 0)
        self.assertEqual(self.calculator.total_items(), 0)
    
    def test_add_item_negative_price(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item("Apple", -1.5, 1)
    
    def test_add_item_negative_quantity(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item("Apple", 1.5, -1)
    
    def test_add_item_invalid_name_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item(123, 1.5, 1)
    
    def test_add_item_invalid_price_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item("Apple", "invalid", 1)
    
    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item("Apple", 1.5, "invalid")
    
    def test_add_item_empty_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.add_item("", 1.5, 1)
    
    def test_remove_item_existing(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.remove_item("Apple")
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.total_items(), 0)
    
    def test_remove_item_non_existing(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item("NonExisting")
    
    def test_remove_item_from_empty_order(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item("Apple")
    
    def test_remove_item_invalid_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.remove_item(123)
    
    def test_get_subtotal_empty_order(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
    
    def test_get_subtotal_single_item(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.5)
    
    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)
    
    def test_get_subtotal_large_amounts(self):
        self.calculator.add_item("Expensive", 999.99, 100)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 99999.0, places=2)
    
    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)
    
    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)
    
    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)
    
    def test_apply_discount_invalid_negative(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.apply_discount(100.0, -0.1)
    
    def test_apply_discount_invalid_greater_than_one(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.apply_discount(100.0, 1.5)
    
    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.apply_discount("invalid", 0.1)
    
    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.apply_discount(100.0, "invalid")
    
    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.apply_discount(-100.0, 0.1)
    
    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)
    
    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)
    
    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)
    
    def test_calculate_shipping_zero_amount(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)
    
    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_shipping(-50.0)
    
    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_shipping("invalid")
    
    def test_calculate_tax_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertEqual(result, 23.0)
    
    def test_calculate_tax_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)
    
    def test_calculate_tax_negative_amount(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_tax(-100.0)
    
    def test_calculate_tax_invalid_type(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_tax("invalid")
    
    def test_calculate_tax_large_amount(self):
        result = self.calculator.calculate_tax(10000.0)
        self.assertEqual(result, 2300.0)
    
    def test_calculate_total_empty_order(self):
        result = self.calculator.calculate_total()
        self.assertEqual(result, 0.0)
    
    def test_calculate_total_no_discount_below_shipping_threshold(self):
        self.calculator.add_item("Apple", 10.0, 1)
        result = self.calculator.calculate_total(0.0)
        self.assertAlmostEqual(result, 10.0 + 10.0 + (20.0 * 0.23), places=2)
    
    def test_calculate_total_no_discount_above_shipping_threshold(self):
        self.calculator.add_item("Expensive", 150.0, 1)
        result = self.calculator.calculate_total(0.0)
        self.assertAlmostEqual(result, 150.0 + (150.0 * 0.23), places=2)
    
    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Apple", 100.0, 1)
        result = self.calculator.calculate_total(0.1)
        expected = 90.0 + (90.0 * 0.23)
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_calculate_total_full_discount(self):
        self.calculator.add_item("Apple", 50.0, 1)
        result = self.calculator.calculate_total(1.0)
        self.assertEqual(result, 0.0)
    
    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item("Apple", 50.0, 1)
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_total(-0.1)
    
    def test_calculate_total_discount_greater_than_one(self):
        self.calculator.add_item("Apple", 50.0, 1)
        with self.assertRaises((ValueError, TypeError)):
            self.calculator.calculate_total(1.5)
    
    def test_calculate_total_default_discount(self):
        self.calculator.add_item("Apple", 50.0, 1)
        result = self.calculator.calculate_total()
        expected = 50.0 + 10.0 + (60.0 * 0.23)
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)
    
    def test_total_items_single_item(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.assertEqual(self.calculator.total_items(), 1)
    
    def test_total_items_multiple_items(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)
    
    def test_total_items_after_remove(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.calculator.remove_item("Apple")
        self.assertEqual(self.calculator.total_items(), 3)
    
    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
    
    def test_clear_order_with_items(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
    
    def test_clear_order_multiple_times(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.clear_order()
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)
    
    def test_list_items_empty_order(self):
        result = self.calculator.list_items()
        self.assertEqual(result, [])
    
    def test_list_items_single_item(self):
        self.calculator.add_item("Apple", 1.5, 1)
        result = self.calculator.list_items()
        self.assertIn("Apple", result)
    
    def test_list_items_multiple_items(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        result = self.calculator.list_items()
        self.assertIn("Apple", result)
        self.assertIn("Banana", result)
        self.assertEqual(len(result), 2)
    
    def test_list_items_after_remove(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.calculator.remove_item("Apple")
        result = self.calculator.list_items()
        self.assertNotIn("Apple", result)
        self.assertIn("Banana", result)
    
    def test_list_items_returns_list(self):
        result = self.calculator.list_items()
        self.assertIsInstance(result, list)
    
    def test_is_empty_initial_state(self):
        self.assertTrue(self.calculator.is_empty())
    
    def test_is_empty_after_add_item(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.assertFalse(self.calculator.is_empty())
    
    def test_is_empty_after_clear(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
    
    def test_is_empty_after_remove_all_items(self):
        self.calculator.add_item("Apple", 1.5, 1)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())
    
    def test_complex_workflow(self):
        self.calculator.add_item("Apple", 1.5, 2)
        self.calculator.add_item("Banana", 2.0, 3)
        self.calculator.add_item("Orange", 3.0, 1)
        self.assertEqual(self.calculator.total_items(), 6)
        self.calculator.remove_item("Banana")
        self.assertEqual(self.calculator.total_items(), 3)
        result = self.calculator.calculate_total(0.1)
        self.assertGreater(result, 0)
        items = self.calculator.list_items()
        self.assertIn("Apple", items)
        self.assertNotIn("Banana", items)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
    
    def test_precision_floating_point(self):
        self.calculator.add_item("Item", 0.1, 3)
        subtotal = self.calculator.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)
    
    def test_large_quantity(self):
        self.calculator.add_item("Item", 1.0, 1000)
        self.assertEqual(self.calculator.total_items(), 1000)
        self.assertEqual(self.calculator.get_subtotal(), 1000.0)
    
    def test_many_different_items(self):
        for i in range(50):
            self.calculator.add_item(f"Item{i}", 1.0, 1)
        self.assertEqual(self.calculator.total_items(), 50)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 50)


if __name__ == '__main__':
    unittest.main()