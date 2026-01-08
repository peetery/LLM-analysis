import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_add_item_normal(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 5.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertCountEqual(self.calc.list_items(), ['Apple', 'Banana'])

    def test_add_item_updates_quantity(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_calculation(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_positive(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_exactly_subtotal(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 100.0), 0.0)

    def test_apply_discount_more_than_subtotal(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 150.0), 0.0)

    def test_apply_discount_negative_value(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_exactly_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_normal_rate(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 120.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(30.0), 123.0)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calc.calculate_total(), 0.0)

    def test_calculate_total_free_shipping_case(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_total_items_multiple_calls(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 15)

    def test_is_empty_lifecycle(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items_output(self):
        self.calc.add_item('Item1', 1.0)
        self.calc.add_item('Item2', 1.0)
        self.assertCountEqual(self.calc.list_items(), ['Item1', 'Item2'])

    def test_clear_order_state(self):
        self.calc.add_item('A', 10.0, 10)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertTrue(self.calc.is_empty())

    def test_integration_add_remove_calculate(self):
        self.calc.add_item('A', 50.0, 2)
        self.calc.add_item('B', 10.0, 1)
        self.calc.remove_item('B')
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)