import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertTrue(calculator.is_empty())

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

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
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0]['name'], 'Laptop')

    def test_add_item_merge_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Mouse', 25.0, 1)
        calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0]['quantity'], 3)

    def test_add_item_invalid_name_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Item', '10.0')

    def test_add_item_invalid_quantity_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Item', 10.0, 1.5)

    def test_add_item_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 10.0)

    def test_add_item_zero_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Item', 0.0)

    def test_add_item_negative_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Item', -10.0)

    def test_add_item_invalid_quantity_value(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Item', 10.0, 0)

    def test_add_item_price_mismatch_exception(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calculator.add_item('Item', 15.0)

    def test_remove_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Item A', 10.0)
        calculator.add_item('Item B', 20.0)
        calculator.remove_item('Item A')
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0]['name'], 'Item B')

    def test_remove_item_invalid_name_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(None)

    def test_remove_item_non_existent_exception(self):
        calculator = OrderCalculator()
        calculator.add_item('Item A', 10.0)
        with self.assertRaises(ValueError):
            calculator.remove_item('Item B')

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0)
        self.assertFalse(calculator.is_empty())

    def test_total_items_count(self):
        calculator = OrderCalculator()
        calculator.add_item('Item A', 10.0, 2)
        calculator.add_item('Item B', 20.0, 5)
        self.assertEqual(calculator.total_items(), 7)

    def test_list_items_unique(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0)
        calculator.add_item('B', 20.0)
        items = calculator.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_clear_order_resets_state(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(len(calculator.items), 0)

    def test_get_subtotal_success(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0, 2)
        calculator.add_item('B', 5.0, 3)
        self.assertEqual(calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order_exception(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_success(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_discount_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_range_low(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_range_high(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping('100')

    def test_calculate_tax_success(self):
        calculator = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calculator.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calculator = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_exception(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax(None)

    def test_calculate_total_no_discount(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(0.0), 72.0)

    def test_calculate_total_with_discount(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(0.2), 108.0)

    def test_calculate_total_free_shipping_triggered(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(0.5), 110.0)

    def test_calculate_total_empty_order_exception(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            calculator.calculate_total('0.1')