import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
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
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='high')

    def test_add_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertIn('Apple', calc.list_items())
        self.assertEqual(calc.total_items(), 10)

    def test_add_existing_item_updates_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 8)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -5.0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_conflict_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 'price')

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 5.0)
        items = calc.list_items()
        self.assertCountEqual(items, ['A', 'B'])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        self.assertFalse(calc.is_empty())

    def test_get_subtotal_success(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_success(self):
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

    def test_apply_discount_invalid_range_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_free_exact(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_free_above(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('99')

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_standard_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('A', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(), 72.0)

    def test_calculate_total_with_discount_and_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('A', 100.0)
        self.assertAlmostEqual(calc.calculate_total(discount=0.2), 99.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=10.0)
        calc.add_item('A', 60.0)
        self.assertAlmostEqual(calc.calculate_total(), 66.0)

    def test_calculate_total_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_type_error_discount(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')