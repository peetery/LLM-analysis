import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_boundaries(self):
        calc_zero = OrderCalculator(tax_rate=0.0)
        calc_full = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_zero.tax_rate, 0.0)
        self.assertEqual(calc_full.tax_rate, 1.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_out_of_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_out_of_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_add_new_item(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 1)
        self.assertIn('Laptop', calc.list_items())
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_duplicate_item_merge(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 1.5, 2)
        calc.add_item('Pen', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Freebie', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Debt', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_conflicting_price(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Item', 20.0, 1)

    def test_add_item_type_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0', 1)
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 1.5)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.5, 2)
        self.assertEqual(calc.get_subtotal(), 21.0)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_out_of_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_standard(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_total_no_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.0), 66.0)

    def test_total_with_discount_and_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.5), 110.0)

    def test_total_discount_removes_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 110.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.2), 107.8)

    def test_total_order_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 10.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_list_items_unique(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 10.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertFalse(calc.is_empty())

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
if __name__ == '__main__':
    unittest.main()