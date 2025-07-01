import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_typical(self):
        self.calc.add_item("apple", 1.0, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        self.calc.add_item("banana", 0.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_remove_item(self):
        self.calc.add_item("orange", 2.0, 2)
        self.calc.remove_item("orange")
        self.assertEqual(self.calc.total_items(), 0)

    def test_get_subtotal_typical(self):
        self.calc.add_item("milk", 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_apply_discount_typical(self):
        discounted = self.calc.apply_discount(100.0, 0.1)
        self.assertEqual(discounted, 90.0)

    def test_apply_discount_edge_case_zero(self):
        discounted = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_calculate_shipping_free(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_paid(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_typical(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_total_typical(self):
        self.calc.add_item("bread", 2.0, 10)
        total = self.calc.calculate_total()
        self.assertEqual(total, 34.6)

    def test_calculate_total_with_discount(self):
        self.calc.add_item("bread", 2.0, 10)
        total = self.calc.calculate_total(0.1)
        self.assertAlmostEqual(total, 31.6)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item("bread", 2.0, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items_typical(self):
        self.calc.add_item("bread", 2.0)
        self.calc.add_item("milk", 3.0)
        items = self.calc.list_items()
        self.assertListEqual(sorted(items), ["bread", "milk"])

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.calc.add_item("bread", 2.0)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("bread", -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("bread", 1.0, 0)

    def test_remove_nonexistent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item("nonexistent")


if __name__ == '__main__':
    unittest.main()