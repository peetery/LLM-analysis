import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.tax_rate, 0.1)
        self.assertEqual(custom_calc.free_shipping_threshold, 50.0)
        self.assertEqual(custom_calc.shipping_cost, 5.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_add_item_custom_quantity(self):
        self.calc.add_item('Orange', 0.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQtyNeg', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_remove_non_existent_item(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_from_empty_list(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_subtotal_single_item(self):
        self.calc.add_item('Book', 15.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 15.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_subtotal_float_precision(self):
        self.calc.add_item('A', 10.1, 1)
        self.calc.add_item('B', 20.2, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 30.3)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_shipping_exactly_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_standard(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_rounding(self):
        tax = self.calc.calculate_tax(10.0)
        self.assertAlmostEqual(tax, 2.3)

    def test_total_items_count(self):
        self.calc.add_item('A', 1, 2)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items_format(self):
        self.calc.add_item('A', 1, 1)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertTrue(all((isinstance(i, str) for i in items)))
        self.assertTrue(any(('A' in i for i in items)))

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1)
        self.assertFalse(self.calc.is_empty())