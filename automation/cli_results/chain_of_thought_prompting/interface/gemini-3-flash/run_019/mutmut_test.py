import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_values_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_add_item_adds_new_entry(self):
        self.calculator.add_item('Widget', 10.0, 2)
        self.assertIn('Widget', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 2)

    def test_add_item_updates_existing_quantity(self):
        self.calculator.add_item('Widget', 10.0, 2)
        self.calculator.add_item('Widget', 10.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_price_mismatch_raises_error(self):
        self.calculator.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Widget', 15.0, 1)

    def test_add_item_invalid_inputs_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Widget', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Widget', 10.0, 0)

    def test_remove_item_removes_entry(self):
        self.calculator.add_item('Widget', 10.0, 1)
        self.calculator.remove_item('Widget')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existent_item_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Gadget')

    def test_clear_order_empties_calculator(self):
        self.calculator.add_item('Widget', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_returns_sum_of_quantities(self):
        self.calculator.add_item('Widget', 10.0, 2)
        self.calculator.add_item('Gadget', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items_returns_unique_names(self):
        self.calculator.add_item('Widget', 10.0, 1)
        self.calculator.add_item('Gadget', 20.0, 1)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['Widget', 'Gadget'])

    def test_is_empty_returns_correct_bool(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Widget', 10.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_get_subtotal_calculates_correctly(self):
        self.calculator.add_item('Widget', 10.0, 2)
        self.calculator.add_item('Gadget', 20.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 40.0)

    def test_apply_discount_calculates_correctly(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_invalid_rate_raises_error(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_applies_cost_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_free_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_free_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_calculates_correctly(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_total_standard_calculation(self):
        self.calculator.add_item('Widget', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_discount_affects_shipping_eligibility(self):
        self.calculator.add_item('Premium Item', 100.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 123.0)