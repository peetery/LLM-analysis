import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item1', 40.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 10)
        self.assertEqual(self.calc.get_subtotal(), 15.0)

    def test_add_item_existing_accumulates_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 2.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -5.0)

    def test_add_item_zero_or_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', 5.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 5.0)

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_non_existent_item(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_remove_from_empty_order(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Ghost')

    def test_subtotal_mixed_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 42.0)

    def test_subtotal_empty_order(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_subtotal_float_precision(self):
        self.calc.add_item('A', 0.1, 1)
        self.calc.add_item('B', 0.2, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3)

    def test_apply_discount_valid(self):
        subtotal = 100.0
        discount = 20.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 80.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        self.assertEqual(self.calc.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_exceeds_subtotal(self):
        subtotal = 50.0
        discount = 60.0
        self.assertEqual(self.calc.apply_discount(subtotal, discount), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_full_flow(self):
        self.calc.add_item('Item', 50.0, 2)
        expected_total = 100.0 - 10.0 + 10.0 + 90.0 * 0.23
        self.assertAlmostEqual(self.calc.calculate_total(discount=10.0), expected_total)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calc.calculate_total(), 0.0)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Expensive', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_total_items_count(self):
        self.calc.add_item('A', 10.0, 5)
        self.calc.add_item('B', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_is_empty_state_changes(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_format(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)