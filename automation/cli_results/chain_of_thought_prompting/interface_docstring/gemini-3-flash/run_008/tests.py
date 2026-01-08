import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_params(self):
        self.assertEqual(self.calc.is_empty(), True)
        self.calc.add_item('Test', 10.0, 1)
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_init_custom_valid_params(self):
        custom_calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.calculate_tax(100.0), 8.0)
        self.assertEqual(custom_calc.calculate_shipping(49.0), 5.0)
        self.assertEqual(custom_calc.calculate_shipping(50.0), 0.0)

    def test_init_tax_rate_low_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_high_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost_exception(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types_exception(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_new_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertIn('Apple', self.calc.list_items())
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_increment_existing_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_multiple_different_items_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 10)
        self.assertEqual(len(self.calc.list_items()), 2)
        self.assertEqual(self.calc.total_items(), 15)

    def test_add_empty_name_exception(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 2.0, 1)

    def test_add_invalid_price_exception(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)

    def test_add_invalid_quantity_exception(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 0)

    def test_add_price_mismatch_exception(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0, 1)

    def test_add_invalid_types_exception(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '2.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.0, 1.5)

    def test_remove_existing_item_success(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item_exception(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_invalid_type_exception(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_clear_non_empty_order_success(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_already_empty_order_success(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_initial_state_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.list_items(), [])

    def test_state_with_items_not_empty(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_total_items_count_correct(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_list_items_unique_names(self):
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        self.assertEqual(sorted(self.calc.list_items()), ['Apple', 'Banana'])

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 10)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_get_subtotal_empty_order_exception(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_hundred_percent(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_partial(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_negative_subtotal_exception(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_out_of_range_exception(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type_exception(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100.0')

    def test_calculate_tax_success(self):
        self.assertEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_on_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_exception(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type_exception(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100.0')

    def test_calculate_total_standard(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 123.0)

    def test_calculate_total_empty_order_exception(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_exception(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)