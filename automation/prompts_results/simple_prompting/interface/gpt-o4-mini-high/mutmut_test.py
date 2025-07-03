import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_add_item_and_is_not_empty(self):
        self.calculator.add_item("apple", 1.0, 2)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("apple", "free", 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("apple", 1.0, "two")

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("apple", -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("apple", 1.0, 0)

    def test_remove_item(self):
        self.calculator.add_item("banana", 2.0, 3)
        self.calculator.remove_item("banana")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("pear")

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("a", 5.0, 2)
        self.calculator.add_item("b", 3.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 13.0)

    def test_apply_discount_typical(self):
        result = self.calculator.apply_discount(100.0, 15.0)
        self.assertAlmostEqual(result, 85.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(50.0, 0.0)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_invalid_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(50.0, -5.0)

    def test_apply_discount_invalid_too_large(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(30.0, 40.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(50.0)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax_typical(self):
        tax = self.calculator.calculate_tax(200.0)
        self.assertAlmostEqual(tax, 200.0 * 0.23)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_after_adding(self):
        self.calculator.add_item("x", 2.0, 3)
        self.calculator.add_item("y", 5.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item("z", 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item("item1", 1.0, 1)
        self.calculator.add_item("item2", 2.0, 2)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ["item1", "item2"])

    def test_calculate_total_typical(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=1000.0, shipping_cost=5.0)
        oc.add_item("a", 10.0, 2)
        oc.add_item("b", 20.0, 1)
        total = oc.calculate_total(discount=5.0)
        # subtotal = 40, discounted = 35, shipping = 5, tax = 3.5, total = 43.5
        self.assertAlmostEqual(total, 43.5)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=0.0, shipping_cost=10.0)
        oc.add_item("a", 50.0, 1)
        total = oc.calculate_total()
        # subtotal = 50, discounted = 50, shipping = 0, tax = 10
        self.assertAlmostEqual(total, 60.0)

if __name__ == '__main__':
    unittest.main()