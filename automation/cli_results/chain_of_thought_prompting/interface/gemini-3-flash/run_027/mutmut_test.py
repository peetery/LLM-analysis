import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_multiple(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Banana', 1.0, 10)
        self.assertEqual(self.calculator.total_items(), 15)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_add_item_duplicate_name(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order_populated(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_remove(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_total_items_count(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_names(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 1.0, 1)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Apple', 2.5, 2)
        self.calculator.add_item('Banana', 3.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 8.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator(shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_positive(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)