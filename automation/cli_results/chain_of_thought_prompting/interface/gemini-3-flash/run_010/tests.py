import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(40), 5.0)
        self.assertEqual(calc.calculate_shipping(60), 0.0)

    def test_add_item_single_default_quantity(self):
        self.calculator.add_item("Apple", 1.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.0)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item("Apple", 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", -1.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.0, -1)

    def test_add_item_empty_name(self):
        self.calculator.add_item("", 1.0)
        self.assertIn("", self.calculator.list_items())

    def test_add_item_existing_item_updates(self):
        self.calculator.add_item("Apple", 1.0, 1)
        self.calculator.add_item("Apple", 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_remove_existing_item(self):
        self.calculator.add_item("Apple", 1.0)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existing_item(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item("Banana")

    def test_clear_populated_order(self):
        self.calculator.add_item("Apple", 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item("Apple", 1.0, 2)
        self.calculator.add_item("Banana", 2.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 4.0)

    def test_total_items_multiple_quantities(self):
        self.calculator.add_item("Apple", 1.0, 10)
        self.calculator.add_item("Banana", 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 15)

    def test_is_empty_transitions(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item("Apple", 1.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_apply_discount_zero(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_partial(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_equal(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 100.0), 0.0)

    def test_apply_discount_greater(self):
        result = self.calculator.apply_discount(100.0, 150.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_positive(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item("Item", 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        expected_tax = (subtotal + shipping) * 0.23
        expected_total = subtotal + shipping + expected_tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item", 200.0, 1)
        discount = 50.0
        discounted_subtotal = 150.0
        shipping = 0.0
        expected_tax = (discounted_subtotal + shipping) * 0.23
        expected_total = discounted_subtotal + shipping + expected_tax
        self.assertAlmostEqual(self.calculator.calculate_total(discount=discount), expected_total)

    def test_calculate_total_empty_order(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_populated(self):
        items = ["Apple", "Banana", "Cherry"]
        for item in items:
            self.calculator.add_item(item, 1.0)
        self.assertCountEqual(self.calculator.list_items(), items)

if __name__ == '__main__':
    unittest.main()