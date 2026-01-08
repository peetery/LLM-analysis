import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.get_subtotal(), 1.5)

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Banana', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_aggregation(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', -10.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadItem', 10.0, 0)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        try:
            self.calculator.remove_item('Ghost')
        except KeyError:
            self.fail('remove_item raised KeyError for non-existent item')
        self.assertTrue(self.calculator.is_empty())

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 2.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false_after_add(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_total_items(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Banana', 2.0, 1)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_get_subtotal_normal(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 31.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount(self):
        subtotal = 100.0
        discount = 10.0
        self.assertEqual(self.calculator.apply_discount(subtotal, discount), 90.0)

    def test_apply_discount_exceeds_subtotal(self):
        subtotal = 50.0
        discount = 60.0
        self.assertEqual(self.calculator.apply_discount(subtotal, discount), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        expected_subtotal = 50.0
        expected_tax = 50.0 * 0.23
        expected_shipping = 10.0
        expected_total = 50.0 + 11.5 + 10.0
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        expected_subtotal = 200.0
        expected_tax = 200.0 * 0.23
        expected_shipping = 0.0
        expected_total = 200.0 + 46.0 + 0.0
        self.assertAlmostEqual(self.calculator.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=20.0), 108.4)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_float_precision(self):
        self.calculator.add_item('A', 0.1, 1)
        self.calculator.add_item('B', 0.2, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 10.369)