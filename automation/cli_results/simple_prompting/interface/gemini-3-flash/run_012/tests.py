import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_add_item_valid(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 1000.0)
        self.assertIn('Laptop', self.calculator.list_items())

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 75.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Broken', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Nothing', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Negative', 10.0, -5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Keyboard', 50.0, 1)
        self.calculator.remove_item('Keyboard')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_non_existing(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 40.0)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 20.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 80.0)

    def test_apply_discount_exceeding_subtotal(self):
        subtotal = 50.0
        discount = 100.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 15.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        amount = 100.0
        self.assertAlmostEqual(self.calculator.calculate_tax(amount), 20.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Item', 50.0, 1)
        expected_total = 50.0 + 15.0 + 50.0 * 0.2
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Big Item', 200.0, 1)
        discount = 50.0
        discounted_subtotal = 150.0
        shipping = 0.0
        tax = 150.0 * 0.2
        expected_total = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(discount), expected_total)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 2.0, 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('X', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_invalid_input_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Name', 'Free')