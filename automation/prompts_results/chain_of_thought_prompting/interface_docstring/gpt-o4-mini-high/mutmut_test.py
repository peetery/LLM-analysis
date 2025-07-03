import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_tax_rate_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10)

    def test_init_free_shipping_threshold_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_init_shipping_cost_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Widget", 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.list_items(), ["Widget"])

    def test_add_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item("Gadget", 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 15.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_repeated_same_name_price(self):
        calc = OrderCalculator()
        calc.add_item("X", 2.0, 2)
        calc.add_item("X", 2.0, 4)
        self.assertEqual(calc.get_subtotal(), 12.0)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(calc.list_items(), ["X"])

    def test_add_multiple_distinct_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 8.0)
        self.assertCountEqual(calc.list_items(), ["A", "B"])
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0)

    def test_add_item_price_non_positive(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 0)

    def test_add_item_quantity_less_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 1.0, 0)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item("Item", 1.0)
        with self.assertRaises(ValueError):
            calc.add_item("Item", 2.0)

    def test_add_item_name_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_price_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Item", "10")

    def test_add_item_quantity_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Item", 1.0, 2.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.remove_item("A")
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("NoSuch")

    def test_remove_item_name_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 2.0, 2)
        calc.add_item("B", 3.0, 3)
        self.assertEqual(calc.get_subtotal(), 13.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_partial(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.25), 75.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-5.0, 0.1)

    def test_apply_discount_discount_less_than_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_greater_than_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.2)

    def test_apply_discount_subtotal_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("50", 0.1)

    def test_apply_discount_discount_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(50.0, None)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), calc.shipping_cost)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(calc.free_shipping_threshold), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(200.0), 0.0)

    def test_calculate_shipping_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("100")

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax([50])

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(), 123.0)

    def test_calculate_total_with_discount_shipping_applies(self):
        calc = OrderCalculator()
        calc.add_item("A", 50.0, 2)
        self.assertAlmostEqual(calc.calculate_total(0.1), 123.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_less_than_zero(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_discount_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_discount_wrong_type(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total("0.2")

    def test_total_items_after_adds(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.list_items(), [])
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_distinct(self):
        calc = OrderCalculator()
        calc.add_item("X", 1.0)
        calc.add_item("Y", 2.0)
        self.assertCountEqual(calc.list_items(), ["X", "Y"])

    def test_list_items_repeated_adds_deduped(self):
        calc = OrderCalculator()
        calc.add_item("X", 1.0)
        calc.add_item("X", 1.0)
        self.assertEqual(calc.list_items(), ["X"])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_fresh(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

if __name__ == "__main__":
    unittest.main()