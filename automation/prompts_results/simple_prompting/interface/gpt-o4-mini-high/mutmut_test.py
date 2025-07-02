import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_parameters(self):
        custom = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom.tax_rate, 0.1)
        self.assertEqual(custom.free_shipping_threshold, 50.0)
        self.assertEqual(custom.shipping_cost, 5.0)

    def test_add_item_and_list_and_total_items(self):
        self.calc.add_item("apple", 1.0, 3)
        self.assertIn("apple", self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        self.calc.add_item("banana", 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("item", "free", 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("item", -5.0, 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("item", 1.0, "two")

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("item", 1.0, -1)

    def test_remove_item(self):
        self.calc.add_item("pear", 2.0, 2)
        self.calc.remove_item("pear")
        self.assertNotIn("pear", self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 0)

    def test_remove_nonexistent_item_raises(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("nonexistent")

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item("a", 1.5, 2)
        self.calc.add_item("b", 2.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.5*2 + 2.0*3)

    def test_apply_discount_typical(self):
        subtotal = 100.0
        self.assertEqual(self.calc.apply_discount(subtotal, 10.0), 90.0)

    def test_apply_discount_zero(self):
        subtotal = 50.0
        self.assertEqual(self.calc.apply_discount(subtotal, 0.0), 50.0)

    def test_apply_discount_equal_subtotal(self):
        subtotal = 20.0
        self.assertEqual(self.calc.apply_discount(subtotal, 20.0), 0.0)

    def test_apply_discount_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, -5.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(30.0, 40.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_typical(self):
        amount = 100.0
        expected = amount * self.calc.tax_rate
        self.assertAlmostEqual(self.calc.calculate_tax(amount), expected)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item("x", 10.0, 2)
        total = self.calc.calculate_total()
        subtotal = 10.0 * 2
        shipping = self.calc.shipping_cost
        tax = (subtotal + shipping) * self.calc.tax_rate
        self.assertAlmostEqual(total, subtotal + shipping + tax)

    def test_calculate_total_with_discount_above_threshold(self):
        self.calc.add_item("y", 60.0, 2)
        total = self.calc.calculate_total(discount=20.0)
        subtotal = 60.0 * 2
        discounted = subtotal - 20.0
        shipping = 0.0
        tax = discounted * self.calc.tax_rate
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-5.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item("z", 5.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_multiple(self):
        self.calc.add_item("a", 1.0, 1)
        self.calc.add_item("b", 2.0, 2)
        self.assertCountEqual(self.calc.list_items(), ["a", "b"])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item("item", 1.0, 1)
        self.assertFalse(self.calc.is_empty())

if __name__ == "__main__":
    unittest.main()