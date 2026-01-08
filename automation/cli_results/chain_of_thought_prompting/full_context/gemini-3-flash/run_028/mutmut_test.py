import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success_default_quantity(self):
        self.calculator.add_item('Apple', 2.0)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_success_custom_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_increment_quantity(self):
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Apple', 2.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 2.0)

    def test_add_item_price_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '2.0')

    def test_add_item_quantity_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 2.0, 1.5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 0)

    def test_add_item_different_price_for_same_name(self):
        self.calculator.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 3.0)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_from_multiple(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.add_item('Banana', 1.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(None)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Apple')

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 1.5, 4)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_zero(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_standard(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_subtotal_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)

    def test_apply_discount_rate_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_apply_discount_out_of_range(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax(None)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_total_no_discount_paid_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        expected_tax = (subtotal + shipping) * 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.0), subtotal + shipping + expected_tax)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        discounted_subtotal = 160.0
        shipping = 0.0
        expected_tax = (discounted_subtotal + shipping) * 0.23
        self.assertAlmostEqual(self.calculator.calculate_total(0.2), discounted_subtotal + shipping + expected_tax)

    def test_calculate_total_discount_type_error(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('0.1')

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_multiple_quantities(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items_success(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.add_item('Banana', 1.0)
        self.calculator.add_item('Apple', 2.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty_true_on_init(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false_after_add(self):
        self.calculator.add_item('Apple', 2.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_true_after_remove(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())