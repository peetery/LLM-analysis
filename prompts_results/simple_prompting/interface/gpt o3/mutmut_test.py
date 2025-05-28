import unittest

from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    # def test_initial_state_empty(self):
    #     self.assertTrue(self.calc.is_empty())
    #     self.assertEqual(self.calc.total_items(), 0)
    #     self.assertAlmostEqual(self.calc.get_subtotal(), 0.0)
    #     self.assertEqual(self.calc.list_items(), [])

    def test_add_item_single(self):
        self.calc.add_item("Apple", 2.5, 4)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 4)
        self.assertIn("Apple", self.calc.list_items())
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_updates_quantity(self):
        self.calc.add_item("Book", 15.0, 1)
        self.calc.add_item("Book", 15.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 45.0)

    def test_remove_item_existing(self):
        self.calc.add_item("Pen", 1.0, 3)
        self.calc.remove_item("Pen")
        self.assertTrue(self.calc.is_empty())

    # def test_remove_item_nonexistent(self):
    #     with self.assertRaises(KeyError):
    #         self.calc.remove_item("Ghost")

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Bad", "free", 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Bad", -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Bad", 1.0, 0)

    def test_apply_discount_percent(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_no_discount(self):
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, -0.2)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50.0, 1.2)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item("X", 40.0, 2)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 40 * 2 * 1.23 + 10.0 * 1.23)

    # def test_calculate_total_with_discount_and_free_shipping(self):
    #     self.calc.add_item("Y", 60.0, 2)
    #     total = self.calc.calculate_total(0.2)
    #     discounted_subtotal = 120.0 * 0.8
    #     expected_total = discounted_subtotal + self.calc.calculate_tax(discounted_subtotal)
    #     self.assertAlmostEqual(total, expected_total)

    def test_total_items_multiple(self):
        self.calc.add_item("A", 5.0, 2)
        self.calc.add_item("B", 3.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item("C", 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item("D", 2.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item("Z", 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.1")


if __name__ == "__main__":
    unittest.main()
