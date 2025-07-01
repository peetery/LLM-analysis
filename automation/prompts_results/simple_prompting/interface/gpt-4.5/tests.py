import unittest
from typing import List
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_typical(self):
        self.calc.add_item("Book", 20.0, 2)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_default_quantity(self):
        self.calc.add_item("Pen", 5.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Invalid", -10.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Invalid", 10.0, 0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Invalid", "10.0", 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Invalid", 10.0, "one")

    def test_remove_item_existing(self):
        self.calc.add_item("Book", 20.0, 1)
        self.calc.remove_item("Book")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item("Ghost")

    def test_get_subtotal(self):
        self.calc.add_item("Book", 10.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_apply_discount_typical(self):
        result = self.calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(50.0, 0.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(50.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, 1.5)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(80.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("50.0")

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("100")

    def test_calculate_total_typical(self):
        self.calc.add_item("Item1", 50.0, 1)
        self.calc.add_item("Item2", 30.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0)

    def test_calculate_total_zero_discount(self):
        self.calc.add_item("Item1", 50.0, 1)
        total = self.calc.calculate_total()
        expected_tax = self.calc.calculate_tax(50.0)
        expected_shipping = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(total, 50.0 + expected_shipping + expected_tax)

    def test_calculate_total_full_discount(self):
        self.calc.add_item("Item1", 100.0, 1)
        total = self.calc.calculate_total(discount=1.0)
        expected_tax = self.calc.calculate_tax(0.0)
        expected_shipping = self.calc.calculate_shipping(0.0)
        self.assertAlmostEqual(total, expected_shipping + expected_tax)

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item("Item1", 20.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount="0.2")

    def test_total_items_multiple(self):
        self.calc.add_item("A", 10.0, 2)
        self.calc.add_item("B", 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item("Item", 10.0, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_typical(self):
        self.calc.add_item("A", 10.0)
        self.calc.add_item("B", 20.0)
        items = self.calc.list_items()
        self.assertIn("A", items)
        self.assertIn("B", items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item("Item", 1.0)
        self.assertFalse(self.calc.is_empty())


if __name__ == '__main__':
    unittest.main()