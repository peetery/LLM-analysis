import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_initial_is_empty(self):
        self.assertTrue(self.calculator.is_empty())

    def test_initial_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_initial_subtotal(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_single_item(self):
        self.calculator.add_item('Apple', 2.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Apple', 2.0, quantity=3)
        self.assertEqual(self.calculator.get_subtotal(), 6.0)

    def test_add_multiple_different_items(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.add_item('Banana', 3.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_add_duplicate_item_updates_quantity(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Apple', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -2.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, quantity=0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, quantity=-1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.0)

    def test_remove_existing_item(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_non_existent_item_raises_error(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Apple')

    def test_clear_order_removes_all_items(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.add_item('Banana', 3.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_clear_order_on_empty_instance(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 3.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 7.0)

    def test_apply_discount_standard(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_equals_subtotal(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_greater_than_subtotal(self):
        result = self.calculator.apply_discount(100.0, 120.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Item', 50.0, 1)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calculator.add_item('Item', 200.0, 1)
        expected = 200.0 * 1.23
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)

    def test_calculate_total_with_discount_below_threshold(self):
        self.calculator.add_item('Item', 110.0, 1)
        expected = (110.0 - 20.0 + 10.0) * 1.23
        self.assertAlmostEqual(self.calculator.calculate_total(discount=20.0), expected)

    def test_calculate_total_with_discount_above_threshold(self):
        self.calculator.add_item('Item', 200.0, 1)
        expected = (200.0 - 50.0) * 1.23
        self.assertAlmostEqual(self.calculator.calculate_total(discount=50.0), expected)

    def test_calculate_total_empty_order(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_total_items_count(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_list_items_content(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 1.0)
        self.assertEqual(set(self.calculator.list_items()), {'Apple', 'Banana'})

    def test_is_empty_state_transitions(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Apple', 1.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())