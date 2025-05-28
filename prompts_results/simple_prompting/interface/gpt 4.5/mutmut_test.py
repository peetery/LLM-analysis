import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_initial_state_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_add_item(self):
        self.calc.add_item('Book', 12.5, 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 2)

    def test_remove_item(self):
        self.calc.add_item('Book', 12.5, 2)
        self.calc.remove_item('Book')
        self.assertTrue(self.calc.is_empty())

    def test_get_subtotal(self):
        self.calc.add_item('Pen', 1.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 0.1
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 90.0)

    def test_calculate_shipping_above_threshold(self):
        self.calc.add_item('Laptop', 150.0)
        discounted_subtotal = self.calc.apply_discount(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.calculate_shipping(discounted_subtotal), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.calc.add_item('Book', 20.0)
        discounted_subtotal = self.calc.apply_discount(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.calculate_shipping(discounted_subtotal), 10.0)

    def test_calculate_tax(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 2)
        total = self.calc.calculate_total()
        expected = 100.0 + 23.0  # subtotal + tax (shipping free)
        self.assertEqual(total, expected)

    # def test_calculate_total_with_discount(self):
    #     self.calc.add_item('Item', 100.0, 1)
    #     total = self.calc.calculate_total(0.1)
    #     expected_subtotal = 90.0
    #     expected_tax = 20.7
    #     self.assertEqual(total, expected_subtotal + expected_tax)

    def test_total_items_multiple(self):
        self.calc.add_item('Book', 10.0, 2)
        self.calc.add_item('Pen', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 7)

    def test_clear_order(self):
        self.calc.add_item('Book', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item('Pen', 1.0)
        self.calc.add_item('Book', 5.0)
        self.assertListEqual(sorted(self.calc.list_items()), ['Book', 'Pen'])

    def test_invalid_item_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -1.0)

    def test_invalid_item_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', 10.0, 0)

    # def test_remove_nonexistent_item(self):
    #     with self.assertRaises(KeyError):
    #         self.calc.remove_item('Nonexistent')

    def test_apply_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)


if __name__ == '__main__':
    unittest.main()
