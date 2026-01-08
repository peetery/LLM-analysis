import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_valid_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_valid_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_tax_rate_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_invalid_tax_rate_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_existing_update_quantity(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.calculator.add_item('Apple', 1.5, 5)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 15)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)

    def test_add_item_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5')

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, '1')

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_remove_item_valid(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 2.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_no_discount(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_range_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_range_low(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(99.9)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_valid_no_shipping_cost(self):
        self.calculator.add_item('Expensive Item', 200.0)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_calculate_total_valid_with_shipping_cost(self):
        self.calculator.add_item('Cheap Item', 50.0)
        total = self.calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 72.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 5)
        self.calculator.add_item('A', 10)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())