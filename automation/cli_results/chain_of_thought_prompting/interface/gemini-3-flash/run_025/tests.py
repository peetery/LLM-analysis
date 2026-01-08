import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

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

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type_tax(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_success(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Laptop')

    def test_add_item_multiple_quantity(self):
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_add_item_existing_increments_quantity(self):
        self.calculator.add_item('Book', 10.0, 1)
        self.calculator.add_item('Book', 10.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, 0)

    def test_add_item_price_mismatch(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 20.0, 1)

    def test_remove_item_success(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_get_subtotal_success(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 20.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 40.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        res = self.calculator.apply_discount(100.0, 0.1)
        self.assertEqual(res, 90.0)

    def test_apply_discount_zero(self):
        res = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(res, 100.0)

    def test_apply_discount_full(self):
        res = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(res, 0.0)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_success(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_success(self):
        self.calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(0.2), 110.7)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 10.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_success(self):
        self.calculator.add_item('Apple', 2.0, 5)
        items = self.calculator.list_items()
        self.assertIn('Apple', items[0])
        self.assertIn('5', items[0])

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])