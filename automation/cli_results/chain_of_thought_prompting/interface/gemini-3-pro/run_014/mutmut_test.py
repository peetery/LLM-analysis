import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_multiple_distinct(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Banana', 0.5, 1)
        self.assertEqual(self.calculator.total_items(), 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_add_item_increment_quantity(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0, 1)

    def test_remove_existing_item(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_subtotal_calculation(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.0, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 35.0)

    def test_subtotal_float_precision(self):
        self.calculator.add_item('A', 10.1, 1)
        self.calculator.add_item('B', 20.2, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 30.3)

    def test_apply_discount_zero(self):
        subtotal = 50.0
        result = self.calculator.apply_discount(subtotal, 0.0)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_shipping_below_threshold(self):
        subtotal = 50.0
        shipping = self.calculator.calculate_shipping(subtotal)
        self.assertEqual(shipping, 10.0)

    def test_shipping_above_threshold(self):
        subtotal = 150.0
        shipping = self.calculator.calculate_shipping(subtotal)
        self.assertEqual(shipping, 0.0)

    def test_shipping_exact_threshold(self):
        subtotal = 100.0
        shipping = self.calculator.calculate_shipping(subtotal)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_standard(self):
        amount = 100.0
        tax = self.calculator.calculate_tax(amount)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Expensive', 200.0, 1)
        total = self.calculator.calculate_total()
        expected_tax = 200.0 * 0.23
        expected_total = 200.0 + 0.0 + 46.0
        self.assertAlmostEqual(total, expected_total)

    def test_total_items_sum_quantities(self):
        self.calculator.add_item('A', 10.0, 5)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('A', 1.0)
        self.assertFalse(self.calculator.is_empty())