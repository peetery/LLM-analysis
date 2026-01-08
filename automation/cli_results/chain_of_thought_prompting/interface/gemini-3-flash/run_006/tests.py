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
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 5.0)
        self.assertEqual(calc.calculate_shipping(250.0), 0.0)

    def test_add_item_success(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertIn('Laptop', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Mouse', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 60.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', -10.0, 1)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', 10.0, -1)

    def test_remove_item_success(self):
        self.calculator.add_item('Keyboard', 50.0, 1)
        self.calculator.remove_item('Keyboard')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Ghost Item')

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('B', 20.0, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_count(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 15.0, 5)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_populated(self):
        items = ['Apple', 'Banana']
        for item in items:
            self.calculator.add_item(item, 1.0)
        self.assertCountEqual(self.calculator.list_items(), items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_new_calculator(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_with_items(self):
        self.calculator.add_item('Bread', 2.0)
        self.assertFalse(self.calculator.is_empty())

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Item A', 10.0, 2)
        self.calculator.add_item('Item B', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount_standard(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_exceeding_subtotal(self):
        result = self.calculator.apply_discount(50.0, 60.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_standard(self):
        self.calculator = OrderCalculator(tax_rate=0.2)
        self.assertEqual(self.calculator.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_integration(self):
        self.calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        self.calculator.add_item('Shoes', 80.0, 1)
        expected_total = 87.0
        self.assertEqual(self.calculator.calculate_total(discount=10.0), expected_total)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_free_shipping(self):
        self.calculator = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        self.calculator.add_item('Phone', 200.0, 1)
        self.assertEqual(self.calculator.calculate_total(), 200.0)