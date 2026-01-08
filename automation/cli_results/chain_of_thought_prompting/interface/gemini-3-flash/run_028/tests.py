import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.08)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 2.5, 4)
        self.assertIn('Apple', self.calculator.list_items())
        self.assertEqual(self.calculator.total_items(), 4)

    def test_add_item_updates_quantity(self):
        self.calculator.add_item('Apple', 2.5, 4)
        self.calculator.add_item('Apple', 2.5, 2)
        self.assertEqual(self.calculator.total_items(), 6)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.5, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.5, 0)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 2.5, 4)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_clear_order(self):
        self.calculator.add_item('Apple', 2.5, 4)
        self.calculator.add_item('Bread', 5.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_count(self):
        self.calculator.add_item('Apple', 2.5, 10)
        self.calculator.add_item('Orange', 3.0, 5)
        self.assertEqual(self.calculator.total_items(), 15)

    def test_list_items_content(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.calculator.add_item('Banana', 1.5, 1)
        items = self.calculator.list_items()
        self.assertCountEqual(items, ['Apple', 'Banana'])

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_initial(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 2.5, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_get_subtotal_calculation(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.calculator.add_item('Bread', 10.0, 2)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_apply_discount_standard(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 90.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_full(self):
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 1.0)
        self.assertEqual(discounted, 0.0)

    def test_apply_discount_invalid_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_excessive(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_boundary(self):
        threshold = self.calculator.free_shipping_threshold
        self.assertEqual(self.calculator.calculate_shipping(threshold), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_integration(self):
        self.calculator.add_item('Item A', 20.0, 1)
        self.calculator.add_item('Item B', 30.0, 1)
        total = self.calculator.calculate_total(0.1)
        self.assertAlmostEqual(total, 67.65)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Expensive Item', 200.0, 1)
        total = self.calculator.calculate_total(0.0)
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calculator.calculate_total(), 0.0)