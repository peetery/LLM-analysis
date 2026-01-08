import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        # Verifying defaults via internal state or related calculations
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_add_item_normal(self):
        self.calculator.add_item("Apple", 1.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn("Apple", self.calculator.list_items())

    def test_add_item_with_quantity(self):
        self.calculator.add_item("Apple", 1.5, quantity=5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_existing_increment_quantity(self):
        self.calculator.add_item("Apple", 1.5, quantity=1)
        self.calculator.add_item("Apple", 1.5, quantity=2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 1.5)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", -1.5)

    def test_add_item_quantity_less_than_one(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.5, quantity=0)

    def test_add_item_existing_name_different_price(self):
        self.calculator.add_item("Apple", 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", "1.5")

    def test_remove_item_existing(self):
        self.calculator.add_item("Apple", 1.5)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Banana")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Apple", 1.5, 2)  # 3.0
        self.calculator.add_item("Banana", 2.0, 3) # 6.0
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_get_subtotal_precision(self):
        self.calculator.add_item("Item1", 0.1, 1)
        self.calculator.add_item("Item2", 0.2, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_hundred_percent(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_normal(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-10.0)

    def test_calculate_tax_positive(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_below_threshold(self):
        self.calculator.add_item("Item", 50.0, 1)
        # subtotal 50, shipping 10, total_pre_tax 60, tax 0.23*60=13.8, total 73.8
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_above_threshold(self):
        self.calculator.add_item("Item", 200.0, 1)
        # subtotal 200, shipping 0, tax 0.23*200=46.0, total 246.0
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item", 100.0, 1)
        # discount 0.5 -> discounted_subtotal 50, shipping 10, tax 0.23*60=13.8, total 73.8
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.5), 73.8)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_integration(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=20.0)
        calc.add_item("A", 40.0, 2) # subtotal 80
        # discount 0.25 -> 60. shipping 20 -> 80. tax 10% -> 8. total 88.
        self.assertAlmostEqual(calc.calculate_total(discount=0.25), 88.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_sum_quantities(self):
        self.calculator.add_item("A", 1.0, 2)
        self.calculator.add_item("B", 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_names(self):
        self.calculator.add_item("A", 1.0)
        self.calculator.add_item("B", 2.0)
        self.assertCountEqual(self.calculator.list_items(), ["A", "B"])

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item("A", 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_remove_last(self):
        self.calculator.add_item("A", 1.0)
        self.calculator.remove_item("A")
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order(self):
        self.calculator.add_item("A", 1.0)
        self.calculator.add_item("B", 2.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_already_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

if __name__ == '__main__':
    unittest.main()