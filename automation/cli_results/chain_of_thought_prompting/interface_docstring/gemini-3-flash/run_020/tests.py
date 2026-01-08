import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_add_item_success(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertIn("Apple", calc.list_items())

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)
        calc.add_item("Apple", 2.0, 3)
        self.assertEqual(calc.total_items(), 8)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 2.0, 1)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 0.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 2.0, 0)

    def test_add_item_different_price_same_name(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 3.0, 1)

    def test_add_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0, 1)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Banana")

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)
        calc.add_item("Banana", 3.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)  # 10.0
        calc.add_item("Banana", 3.0, 2) # 6.0
        self.assertEqual(calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 5)
        calc.add_item("Banana", 3.0, 2)
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_apply_discount_normal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_one_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_invalid_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_standard_flow(self):
        # subtotal: 100, discount: 0.1 -> 90.0
        # shipping: 90 < 100 -> +10.0 = 100.0
        # tax: 0.23 * 100.0 = 23.0
        # total: 100.0 + 23.0 = 123.0
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Widget", 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_no_discount(self):
        # subtotal: 100, discount: 0.0 -> 100.0
        # shipping: 100 >= 100 -> 0.0
        # tax: 0.23 * 100.0 = 23.0
        # total: 123.0
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Widget", 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(), 123.0)

    def test_calculate_total_discount_triggers_shipping(self):
        # subtotal: 110, discount: 0.1 -> 99.0
        # shipping: 99 < 100 -> +10.0 = 109.0
        # tax: 0.23 * 109.0 = 25.07
        # total: 109.0 + 25.07 = 134.07
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Widget", 110.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 134.07)

    def test_calculate_total_zero_total(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item("Freebie", 10.0, 1)
        self.assertEqual(calc.calculate_total(discount=1.0), 0.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.5)

    def test_list_items_populated(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 2.0, 1)
        calc.add_item("Banana", 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Apple", items)
        self.assertIn("Banana", items)

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_initial(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removal(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.0, 1)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

if __name__ == '__main__':
    unittest.main()