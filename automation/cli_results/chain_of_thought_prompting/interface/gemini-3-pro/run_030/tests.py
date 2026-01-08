import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.tax_rate, 0.23)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calculator.tax_rate, 0.1)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calculator.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calculator = OrderCalculator(tax_rate=0.0)
        self.assertAlmostEqual(calculator.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calculator = OrderCalculator(shipping_cost=0.0)
        self.assertAlmostEqual(calculator.shipping_cost, 0.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_specific_quantity(self):
        self.calc.add_item('Banana', 0.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 2.5)

    def test_add_item_existing_increments_quantity(self):
        self.calc.add_item('Apple', 1.0, quantity=2)
        self.calc.add_item('Apple', 1.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -10.0)

    def test_add_item_invalid_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, quantity=0)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_remove_item_clears_state(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)
        self.assertNotIn('Apple', self.calc.list_items())

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('A', 10.0)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_precision(self):
        self.calc.add_item('A', 0.1)
        self.calc.add_item('B', 0.2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3)

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_greater_than_subtotal(self):
        result = self.calc.apply_discount(50.0, 60.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_total_standard_order(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_empty_order(self):
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 0.0)

    def test_calculate_total_discount_clears_subtotal(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total(discount=50.0)
        self.assertAlmostEqual(total, 10.0)

    def test_total_items_sum(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_mixed_quantities(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('B', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 11)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_clear_empty_order(self):
        try:
            self.calc.clear_order()
        except Exception:
            self.fail('clear_order() raised Exception unexpectedly!')

    def test_list_items_populated(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())