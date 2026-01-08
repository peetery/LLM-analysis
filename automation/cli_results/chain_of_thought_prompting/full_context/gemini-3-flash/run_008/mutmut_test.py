import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
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

    def test_init_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_boundary_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calc.free_shipping_threshold, 0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['quantity'], 10)

    def test_add_item_existing_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 8)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 2)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_price_mismatch_exception(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_empty_name_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_zero_price_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_negative_price_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_type_error_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_add_item_type_error_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_add_item_type_error_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_not_found_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_normal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_normal(self):
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

    def test_apply_discount_negative_subtotal_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_range_error_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_range_error_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('50')

    def test_calculate_total_standard(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.0), 66.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.5), 110.0)

    def test_calculate_total_discount_triggers_shipping_cost(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.25), 110.0)

    def test_calculate_total_empty_order_exception(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_type_error_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_normal(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(len(calc.items), 0)

    def test_list_items_normal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 1.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_true_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false_after_add(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        self.assertFalse(calc.is_empty())