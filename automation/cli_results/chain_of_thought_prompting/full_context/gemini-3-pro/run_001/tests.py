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

    def test_init_custom(self):
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

    def test_init_invalid_value_tax_rate_large(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_value_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_value_shipping_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 2})

    def test_add_item_existing_increment(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_existing_price_mismatch(self):
        self.calculator.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_add_item_invalid_type_name(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)

    def test_add_item_invalid_type_price(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5')

    def test_add_item_invalid_type_quantity(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, '2')

    def test_add_item_invalid_value_name_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)

    def test_add_item_invalid_value_price_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0)

    def test_add_item_invalid_value_price_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.5)

    def test_add_item_invalid_value_quantity_small(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, 0)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty(self):
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

    def test_apply_discount_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_apply_discount_invalid_value_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_value_large(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.2)

    def test_calculate_shipping_standard(self):
        cost = self.calculator.calculate_shipping(99.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_free(self):
        cost = self.calculator.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_threshold_boundary(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('99')

    def test_calculate_tax_success(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_integration(self):
        self.calculator.add_item('Item1', 50.0, 1)
        total = self.calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item1', 200.0, 1)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_type_discount(self):
        self.calculator.add_item('Item1', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_calculate_total_invalid_value_discount(self):
        self.calculator.add_item('Item1', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_total_items_normal(self):
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 5)
        self.calculator.add_item('A', 10)
        items = self.calculator.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())