import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_params(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_params(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_specific_quantity(self):
        self.calculator.add_item('Banana', 0.8, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 0.8, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(len(self.calculator.list_items()), 2)

    def test_add_existing_item_updates_quantity(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -1)

    def test_remove_existing_item(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_floating_point_precision(self):
        self.calculator.add_item('Item1', 0.1)
        self.calculator.add_item('Item2', 0.2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3, places=7)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_equal_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_positive_amount(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_sum_of_quantities(self):
        self.calculator.add_item('A', 1.0, 2)
        self.calculator.add_item('B', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order_already_empty(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_with_items(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.add_item('B', 1.0)
        self.assertCountEqual(self.calculator.list_items(), ['A', 'B'])

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_adding(self):
        self.calculator.add_item('A', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_removing_last(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.remove_item('A')
        self.assertTrue(self.calculator.is_empty())