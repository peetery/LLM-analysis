import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='high')

    def test_add_item_typical(self):
        self.calculator.add_item('book', 10.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_add_item_merge_quantities(self):
        self.calculator.add_item('book', 10.0, 1)
        self.calculator.add_item('book', 10.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('book', -5, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('book', 10, 0)

    def test_add_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_remove_item_typical(self):
        self.calculator.add_item('pen', 2.0, 1)
        self.calculator.remove_item('pen')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('unknown')

    def test_get_subtotal_typical(self):
        self.calculator.add_item('item1', 20.0, 2)
        self.calculator.add_item('item2', 15.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 55.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_typical(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-50.0, 0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(50.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(50.0, 1.1)

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("fifty", 0.2)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_paid(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("fifty")

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("ten")

    def test_calculate_total_typical(self):
        self.calculator.add_item('item', 50.0, 2)
        total = self.calculator.calculate_total(discount=0.1)
        expected = ((100 * 0.9) + 0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items_typical(self):
        self.calculator.add_item('item1', 10.0, 3)
        self.calculator.add_item('item2', 5.0, 2)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order_typical(self):
        self.calculator.add_item('item', 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_typical(self):
        self.calculator.add_item('apple', 1.0)
        self.calculator.add_item('banana', 2.0)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['apple', 'banana'])

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item('apple', 1.0)
        self.assertFalse(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()
