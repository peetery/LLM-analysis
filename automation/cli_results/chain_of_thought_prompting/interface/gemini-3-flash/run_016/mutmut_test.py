import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(60), 0.0)
        self.assertEqual(calc.calculate_shipping(40), 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_add_item_normal(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_accumulation(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Apple', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -2.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, -1)

    def test_remove_item_normal(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Banana')

    def test_clear_order(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Banana', 3.0, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_is_empty_new_calculator(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items_sum(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 3.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_content(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Banana', 3.0, 1)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 10.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 16.0)

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

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_normal(self):
        self.assertEqual(self.calculator.calculate_tax(200.0), 46.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_qualify_free_shipping(self):
        self.calculator.add_item('Item', 150.0, 1)
        self.assertEqual(self.calculator.calculate_total(), 184.5)