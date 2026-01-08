import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.total_items(), 0)

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calculator.is_empty())

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_update_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_multiple_different(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 1)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', 10.0, 0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_remove_last_item_clears_state(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_mixed_items(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_floats(self):
        self.calc.add_item('Item1', 10.1, 1)
        self.calc.add_item('Item2', 20.2, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 30.3)

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_equals_subtotal(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_exceeds_subtotal(self):
        result = self.calc.apply_discount(100.0, 150.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(50.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax_standard(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_total_standard(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        expected_tax = 50.0 * 0.23
        expected_shipping = 10.0
        self.assertAlmostEqual(total, 50.0 + expected_tax + expected_shipping)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        expected_tax = 200.0 * 0.23
        self.assertAlmostEqual(total, 200.0 + expected_tax)

    def test_calculate_total_full_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total(discount=50.0)
        self.assertEqual(total, 10.0)

    def test_total_items_mixed(self):
        self.calc.add_item('A', 10, 1)
        self.calc.add_item('B', 10, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_populated(self):
        self.calc.add_item('A', 10, 1)
        self.calc.add_item('B', 10, 1)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1, 1)
        self.assertFalse(self.calc.is_empty())

    def test_clear_order(self):
        self.calc.add_item('A', 1, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_clear_already_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())