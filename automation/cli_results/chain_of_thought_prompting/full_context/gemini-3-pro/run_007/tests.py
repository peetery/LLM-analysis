import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertEqual(calculator.items, [])

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.05)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Widget', 10.0, 2)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0], {'name': 'Widget', 'price': 10.0, 'quantity': 2})

    def test_add_item_existing_update_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Widget', 10.0, 1)
        calculator.add_item('Widget', 10.0, 2)
        self.assertEqual(len(calculator.items), 1)
        self.assertEqual(calculator.items[0]['quantity'], 3)

    def test_add_item_conflict_price(self):
        calculator = OrderCalculator()
        calculator.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            calculator.add_item('Widget', 12.0, 1)

    def test_add_item_invalid_name_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 10.0)

    def test_add_item_invalid_name_empty(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 10.0)

    def test_add_item_invalid_price_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Widget', '10.0')

    def test_add_item_invalid_price_value(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Widget', 0)
        with self.assertRaises(ValueError):
            calculator.add_item('Widget', -5.0)

    def test_add_item_invalid_quantity_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Widget', 10.0, '2')

    def test_add_item_invalid_quantity_value(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Widget', 10.0, 0)

    def test_remove_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Widget', 10.0)
        calculator.remove_item('Widget')
        self.assertEqual(len(calculator.items), 0)

    def test_remove_item_not_found(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item('Nonexistent')

    def test_remove_item_invalid_name_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 10.0, 2)
        calculator.add_item('Item2', 5.0, 1)
        self.assertEqual(calculator.get_subtotal(), 25.0)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 10.0, 3)
        self.assertEqual(calculator.get_subtotal(), 30.0)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_success(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_percent(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-50.0, 0.1)

    def test_apply_discount_invalid_types(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            calculator.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping('50')

    def test_calculate_tax_success(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        calculator = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax('100')

    def test_calculate_total_standard(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 72.0)

    def test_calculate_total_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item1', 200.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 240.0)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 10.0)
        with self.assertRaises(TypeError):
            calculator.calculate_total(discount='0.1')

    def test_total_items_sum(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0, 2)
        calculator.add_item('B', 20.0, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_empty(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_clear_order(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0)
        calculator.clear_order()
        self.assertEqual(calculator.items, [])
        self.assertTrue(calculator.is_empty())

    def test_list_items_unique(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0)
        calculator.add_item('B', 20.0)
        calculator.add_item('A', 10.0)
        items = calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_state(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())
        calculator.add_item('A', 10.0)
        self.assertFalse(calculator.is_empty())