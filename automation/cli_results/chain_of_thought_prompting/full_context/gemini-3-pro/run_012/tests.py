import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

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

    def test_init_type_error_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_type_error_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_value_error_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_value_error_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_value_error_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_value_error_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_existing_update_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 8)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '5')

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_add_item_value_error_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_add_item_value_error_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_conflict_price(self):
        self.calc.add_item('Apple', 1.5, 5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_type_error_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_type_error_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_apply_discount_value_error_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_value_error_subtotal_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-50.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_standard_flow(self):
        self.calc.add_item('Item1', 50.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 66.0)

    def test_calculate_total_free_shipping_flow(self):
        self.calc.add_item('Item1', 200.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_type_error_discount(self):
        self.calc.add_item('Item1', 100.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items_populated(self):
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 20, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_populated(self):
        self.calc.add_item('A', 10)
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])

    def test_list_items_populated(self):
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 20)
        items = self.calc.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())