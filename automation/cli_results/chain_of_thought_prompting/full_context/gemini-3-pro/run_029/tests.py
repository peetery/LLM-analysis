import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_tax_rate_value_error_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_value_error_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_value_error_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_value_error_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_existing_increase_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 8)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_conflict_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '10')

    def test_add_item_name_empty_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_price_negative_or_zero_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            calc.add_item('Banana', -1.0)

    def test_add_item_quantity_negative_or_zero_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_not_found_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_success(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_success(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_subtotal_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_range_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_negative_amount_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_total_standard_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 66.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 216.0)

    def test_calculate_total_empty_order_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_total_items_success(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_success(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_list_items_success(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0)
        items = calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_initial(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false_after_add(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        self.assertFalse(calc.is_empty())