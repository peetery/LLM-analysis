import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Laptop', self.calculator.list_items())

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Mouse', 25.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, 0)

    def test_add_item_different_price_same_name(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 15.0, 1)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', '10.0', 1)

    def test_remove_item_valid(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_out_of_range(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax(None)

    def test_calculate_total_no_discount_no_free_shipping(self):
        calc = OrderCalculator(0.2, 100.0, 10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertEqual(calc.calculate_total(discount=0.0), 72.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        calc = OrderCalculator(0.1, 100.0, 10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertEqual(calc.calculate_total(discount=0.5), 110.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='high')

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 5)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('Item', 10.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_unique(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_new(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Item', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_remove(self):
        self.calculator.add_item('Item', 1.0, 1)
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())