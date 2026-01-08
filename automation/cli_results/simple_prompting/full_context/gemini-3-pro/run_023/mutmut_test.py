import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

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

    def test_init_invalid_value_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_value_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_value_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_value_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_existing_update_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_invalid_type_name(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)

    def test_add_item_invalid_type_price(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '10')

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 10.0, 1.5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 10.0, 0)

    def test_add_item_invalid_price_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)

    def test_add_item_duplicate_name_different_price(self):
        self.calculator.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 1.0, 5)
        self.assertEqual(self.calculator.get_subtotal(), 11.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_type_subtotal(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_invalid_type_discount(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_range_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_range_too_high(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_standard(self):
        cost = self.calculator.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_free(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)
        cost_above = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost_above, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_success(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-50.0)

    def test_calculate_total_standard(self):
        self.calculator.add_item('Item1', 50.0, 1)
        total = self.calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Item1', 200.0, 1)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_multiple(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_list_items(self):
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 20.0)
        self.calculator.add_item('A', 10.0, 2)
        items = self.calculator.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('A', 10.0)
        self.assertFalse(self.calculator.is_empty())