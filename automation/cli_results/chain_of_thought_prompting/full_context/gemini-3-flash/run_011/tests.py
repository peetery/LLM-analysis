import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(len(calc.items), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])

    def test_init_invalid_shipping_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_init_tax_rate_out_of_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_out_of_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 2.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_update_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 4)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '10.0')

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.0, 1.5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 0)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 1.5, 4)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_success(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_out_of_range_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_out_of_range_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_total_full_flow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total(discount=0.2)
        self.assertAlmostEqual(total, 99.0)

    def test_calculate_total_shipping_boundary_due_to_discount(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 110.0, 1)
        total = calc.calculate_total(discount=0.2)
        self.assertEqual(total, 98.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_sum(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(len(calc.items), 0)

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.add_item('Apple', 1.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        self.assertFalse(calc.is_empty())