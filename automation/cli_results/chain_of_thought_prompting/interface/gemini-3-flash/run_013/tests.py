import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 8.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_normal(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 2)
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_add_item_merging(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 2)
        calc.add_item("Apple", 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item("Sample", 0.0, 1)
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertIn("Sample", calc.list_items()[0])

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Invalid", -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 1.0, 0)
        with self.assertRaises(ValueError):
            calc.add_item("Apple", 1.0, -1)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Apple", "1.0", 1)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 2)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Banana")

    def test_remove_item_multi_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 5)
        calc.remove_item("Apple")
        self.assertTrue(calc.is_empty())

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.0, 2)
        calc.add_item("Banana", 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item("Item", 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3)

    def test_apply_discount_standard(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -5.0)

    def test_apply_discount_over_limit(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 105.0)

    def test_calculate_shipping_paid(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertIn(result, [0.0, 10.0])

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_positive(self):
        calc = OrderCalculator(tax_rate=0.20)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.20)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_total_integration(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("Widget", 50.0, 1)
        total = calc.calculate_total(discount=20.0)
        discounted_subtotal = 40.0
        shipping = 10.0
        expected_tax = (40.0 + 10.0) * 0.1
        self.assertEqual(total, 40.0 + 10.0 + expected_tax)

    def test_calculate_total_discount_override(self):
        calc = OrderCalculator()
        calc.add_item("Item", 100.0, 1)
        total1 = calc.calculate_total(0.0)
        total2 = calc.calculate_total(50.0)
        self.assertLess(total2, total1)

    def test_calculate_total_empty(self):
        calc = OrderCalculator(tax_rate=0.2, shipping_cost=10.0)
        expected = (0.0 + 10.0) * 1.2
        self.assertAlmostEqual(calc.calculate_total(), expected)

    def test_total_items_count(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_list_items_formatting(self):
        calc = OrderCalculator()
        calc.add_item("Apple", 1.5, 2)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], str)
        self.assertIn("Apple", items[0])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_states(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item("A", 1.0, 1)
        self.assertFalse(calc.is_empty())
        calc.remove_item("A")
        self.assertTrue(calc.is_empty())

if __name__ == '__main__':
    unittest.main()