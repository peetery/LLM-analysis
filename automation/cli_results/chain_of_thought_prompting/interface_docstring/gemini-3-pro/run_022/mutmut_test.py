import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.tax_rate, 0.23)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_valid(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calculator.tax_rate, 0.05)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calculator.shipping_cost, 5.0)

    def test_init_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        self.assertIn('Apple', calculator.list_items())
        self.assertEqual(calculator.total_items(), 10)

    def test_add_item_default_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Banana', 0.5)
        self.assertEqual(calculator.total_items(), 1)

    def test_add_existing_item_same_price(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 2)
        calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(calculator.total_items(), 5)
        self.assertEqual(len(calculator.list_items()), 1)

    def test_add_existing_item_conflict(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 2.0, 3)

    def test_add_item_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 1.0, 1)

    def test_add_item_invalid_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            calculator.add_item('Orange', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 1.5, 0)

    def test_add_item_bad_types(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item('Apple', '1.5', 1)

    def test_remove_item_success(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 2)
        calculator.remove_item('Apple')
        self.assertTrue(calculator.is_empty())

    def test_remove_item_not_found(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item('NonExistent')

    def test_remove_item_bad_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 10.0, 2)
        calculator.add_item('Item2', 5.0, 4)
        self.assertAlmostEqual(calculator.get_subtotal(), 40.0)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_valid(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_range(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_bad_types(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(99.9)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_exact_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_bad_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calculator = OrderCalculator(tax_rate=0.2)
        tax = calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_tax_zero(self):
        calculator = OrderCalculator(tax_rate=0.2)
        tax = calculator.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_tax_bad_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax('100')

    def test_calculate_total_standard_flow(self):
        calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 50.0, 1)
        total = calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_free_shipping_flow(self):
        calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 150.0, 1)
        total = calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 184.5)

    def test_calculate_total_empty(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=1.5)

    def test_total_items_sum(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0, 2)
        calculator.add_item('B', 5.0, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_is_empty_state(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())
        calculator.add_item('A', 10.0)
        self.assertFalse(calculator.is_empty())
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())

    def test_list_items_content(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0)
        calculator.add_item('B', 5.0)
        items = calculator.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_clear_order_effect(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0)
        calculator.clear_order()
        self.assertEqual(calculator.total_items(), 0)
        self.assertTrue(calculator.is_empty())