import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_initialization_defaults(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_initialization_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_add_item_valid(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 2)

    def test_add_item_duplicate_increase_quantity(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Book', 20.0, 3)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_duplicate_different_price(self):
        self.calculator.add_item('Book', 20.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 25.0)

    def test_remove_item_valid(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.remove_item('Book')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Nonexistent')

    def test_get_subtotal_valid(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Pen', 5.0, 4)
        self.assertEqual(self.calculator.get_subtotal(), 60.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        discounted = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(discounted, 80.0)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-50.0, 0.2)

    def test_calculate_shipping_free(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_paid(self):
        shipping = self.calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_valid(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Book', 50.0, 2)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Book', 100.0, 2)
        total = self.calculator.calculate_total(0.1)
        self.assertEqual(total, 221.4)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Book', 50.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.5)

    def test_total_items(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Pen', 5.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.add_item('Pen', 5.0)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['Book', 'Pen'])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Book', 20.0)
        self.assertFalse(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()