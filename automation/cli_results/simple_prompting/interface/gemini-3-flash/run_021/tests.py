import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.default_tax = 0.23
        self.default_threshold = 100.0
        self.default_shipping = 10.0
        self.calc = OrderCalculator(tax_rate=self.default_tax, free_shipping_threshold=self.default_threshold, shipping_cost=self.default_shipping)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_typical(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1000.0)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_multiple_quantities(self):
        self.calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 75.0)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '1')

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -10.0, 1)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, -1)

    def test_remove_item_existing(self):
        self.calc.add_item('Item', 10.0, 1)
        self.calc.remove_item('Item')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_typical(self):
        self.assertEqual(self.calc.apply_discount(100.0, 20.0), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 100.0), 0.0)

    def test_apply_discount_more_than_subtotal(self):
        self.assertEqual(self.calc.apply_discount(100.0, 150.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(self.default_threshold - 1), self.default_shipping)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(self.default_threshold), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(self.default_threshold + 1), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_typical(self):
        self.calc.add_item('Item', 50.0, 1)
        expected_subtotal = 50.0
        expected_shipping = 10.0
        expected_tax = 50.0 * 0.23
        self.assertAlmostEqual(self.calc.calculate_total(), expected_subtotal + expected_shipping + expected_tax)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Item', 100.0, 2)
        discounted_subtotal = 150.0
        expected_shipping = 0.0
        expected_tax = discounted_subtotal * 0.23
        self.assertAlmostEqual(self.calc.calculate_total(discount=50.0), discounted_subtotal + expected_shipping + expected_tax)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 7)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())