import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(40), 5.0)
        self.assertEqual(calc.calculate_shipping(60), 0.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)
        self.assertEqual(calc.calculate_shipping(10), 0.0)

    def test_add_item_normal(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1.5)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_quantity(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)
        self.assertEqual(self.calculator.total_items(), 10)

    def test_add_item_cumulative(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.5, 1)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5, 1)

    def test_remove_item_normal(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Bread', 2.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_tax_normal(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_total_items_count(self):
        self.calculator.add_item('A', 1, 2)
        self.calculator.add_item('B', 1, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('A', 1, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_list_items_names(self):
        self.calculator.add_item('Apple', 1, 1)
        self.calculator.add_item('Banana', 1, 1)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)