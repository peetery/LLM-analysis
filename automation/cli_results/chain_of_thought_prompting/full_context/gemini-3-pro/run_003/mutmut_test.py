import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_type_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_range_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_range_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_range_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_range_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        self.calc.add_item('Orange', 1.0, 5)
        self.calc.add_item('Orange', 1.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 8)

    def test_add_item_conflict_different_price(self):
        self.calc.add_item('Grapes', 3.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Grapes', 4.0, 1)

    def test_add_item_invalid_type_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_invalid_type_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0')

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, '5')

    def test_add_item_invalid_value_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_value_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -5.0)

    def test_add_item_invalid_value_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_remove_item_success(self):
        self.calc.add_item('Milk', 2.5)
        self.calc.remove_item('Milk')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Bread')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_success(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_boundary_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_boundary_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_range_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_too_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_value_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)
        cost = self.calc.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_value_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item1', 40.0, 2)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 110.7)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item1', 200.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item1', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        self.calc.add_item('A', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())