import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calc.is_empty(), True)
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(150.0), 15.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_tax_rate_out_of_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new_entry(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertIn('Apple', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 10)

    def test_add_item_quantity_merge(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 15)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_add_item_invalid_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5, 1)

    def test_add_item_invalid_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_price_conflict_raises_value_error(self):
        self.calc.add_item('Apple', 1.5, 10)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 5)

    def test_add_item_invalid_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5', 1)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_missing_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_correct_calculation(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Bread', 2.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 19.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_normal(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_out_of_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_normal(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_paid_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 67.65)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive', 120.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.1), 132.84)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.1)

    def test_calculate_total_invalid_discount_raises_value_error(self):
        self.calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_total_items_sum(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Bread', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 12)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique_names(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Bread', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Bread', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_state_tracking(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.5, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())