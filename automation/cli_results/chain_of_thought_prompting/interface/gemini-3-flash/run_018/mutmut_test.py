import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_duplicate(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5, 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_standard(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item 1', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_total_items_mixed_quantities(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_names(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_addition(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())