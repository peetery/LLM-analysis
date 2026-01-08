import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 40.0, 1)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_add_item_normal(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_multiple(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Banana', 1.0, 10)
        self.assertEqual(self.calculator.total_items(), 15)
        self.assertEqual(len(self.calculator.list_items()), 2)

    def test_add_item_duplicate(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Broken', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Broken', 10.0, 0)

    def test_remove_item_normal(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('NonExistent')

    def test_clear_order(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.add_item('B', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_list_items_normal(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 1.0, 1)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_get_subtotal_normal(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Banana', 3.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 14.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount_normal(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeding_subtotal(self):
        result = self.calculator.apply_discount(50.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Gadget', 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Gadget', 100.0, 1)
        discount = 20.0
        discounted_subtotal = 80.0
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(discount=discount), expected)

    def test_calculate_total_empty_order(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Premium', 200.0, 1)
        subtotal = 200.0
        shipping = 0.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)

    def test_calculate_total_paid_shipping(self):
        self.calculator.add_item('Item', 99.99, 1)
        subtotal = 99.99
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)

    def test_precision_handling(self):
        self.calculator.add_item('Small', 0.1, 1)
        self.calculator.add_item('Small', 0.2, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3)