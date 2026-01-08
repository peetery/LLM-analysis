import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_init_default_values(self):
        default_calc = OrderCalculator()
        self.assertEqual(default_calc.calculate_tax(100.0), 23.0)
        self.assertEqual(default_calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(default_calc.calculate_shipping(100.0), 0.0)

    def test_init_custom_values(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertEqual(self.calc.calculate_shipping(99.0), 15.0)

    def test_init_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.calculate_tax(100.0), 100.0)

    def test_init_boundary_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(0.0), 0.0)

    def test_init_value_error_tax_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_value_error_tax_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_value_error_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_value_error_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 2.0, 1)

    def test_add_item_value_error_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)

    def test_add_item_value_error_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 0)

    def test_add_item_value_error_conflicting_price(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0, 1)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_value_error_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_value_error_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_boundary_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_boundary_one(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_boundary_subtotal_zero(self):
        self.assertEqual(self.calc.apply_discount(0.0, 0.5), 0.0)

    def test_apply_discount_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_value_error_out_of_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, 'high')

    def test_calculate_shipping_paid(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 15.0)

    def test_calculate_shipping_free_above(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_free_exact(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping([100])

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(200.0), 40.0)

    def test_calculate_tax_boundary_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('200')

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertEqual(self.calc.calculate_total(0.0), 78.0)

    def test_calculate_total_with_discount_triggering_shipping(self):
        self.calc.add_item('Item', 120.0, 1)
        self.assertEqual(self.calc.calculate_total(0.25), 126.0)

    def test_calculate_total_free_shipping_flow(self):
        self.calc.add_item('Item', 100.0, 2)
        self.assertEqual(self.calc.calculate_total(0.1), 216.0)

    def test_calculate_total_value_error_invalid_discount(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_value_error_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.0)

    def test_calculate_total_type_error(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_content(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('B', 1.0, 2)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_lifecycle(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())