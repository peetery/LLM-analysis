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

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_same_name_multiple_times(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_zero_quantity(self):
        self.calculator.add_item('Apple', 1.5, 0)
        self.assertEqual(self.calculator.total_items(), 0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.5)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, -1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, '2')

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Apple')

    def test_remove_item_after_multiple_adds(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 3)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 10.0)

    def test_apply_discount_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 110.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100.0', 10.0)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10.0')

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        shipping = self.calculator.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-50.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50.0')

    def test_calculate_tax_positive_amount(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100.0')

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_total_empty_order(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calculator.add_item('Apple', 10.0, 1)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 22.3, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calculator.add_item('Apple', 100.0, 1)
        total = self.calculator.calculate_total()
        self.assertEqual(total, 123.0)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Apple', 100.0, 1)
        total = self.calculator.calculate_total(discount=20.0)
        self.assertEqual(total, 98.4)

    def test_calculate_total_discount_affects_shipping(self):
        self.calculator.add_item('Apple', 95.0, 1)
        total_no_discount = self.calculator.calculate_total()
        total_with_discount = self.calculator.calculate_total(discount=10.0)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-10.0)

    def test_calculate_total_discount_exceeds_subtotal(self):
        self.calculator.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=60.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='10.0')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single_item_single_quantity(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        self.calculator.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.calculator.add_item('Cherry', 3.0, 1)
        self.assertEqual(self.calculator.total_items(), 6)

    def test_total_items_after_removal(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 3)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_subtotal_zero(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_clear_order_list_items_empty(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single_item(self):
        self.calculator.add_item('Apple', 1.5, 2)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_list_items_multiple_items(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_format(self):
        self.calculator.add_item('Apple', 1.5, 2)
        items = self.calculator.list_items()
        self.assertTrue(isinstance(items, list))
        self.assertTrue(all((isinstance(item, str) for item in items)))

    def test_is_empty_initially(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_with_zero_quantity_item(self):
        self.calculator.add_item('Apple', 1.5, 0)
        self.assertTrue(self.calculator.is_empty())

    def test_complex_workflow(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.calculator.add_item('Cherry', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertEqual(self.calculator.get_subtotal(), 45.0)
        self.calculator.remove_item('Banana')
        self.assertEqual(self.calculator.total_items(), 7)
        self.assertEqual(self.calculator.get_subtotal(), 30.0)
        total = self.calculator.calculate_total(discount=5.0)
        self.assertGreater(total, 0)

    def test_floating_point_precision(self):
        self.calculator.add_item('Apple', 0.1, 3)
        subtotal = self.calculator.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_large_quantities(self):
        self.calculator.add_item('Apple', 1.0, 1000000)
        self.assertEqual(self.calculator.total_items(), 1000000)
        self.assertEqual(self.calculator.get_subtotal(), 1000000.0)

    def test_large_prices(self):
        self.calculator.add_item('Diamond', 1000000.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 1000000.0)

    def test_very_small_price(self):
        self.calculator.add_item('Penny', 0.01, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.01)

    def test_shipping_threshold_boundary(self):
        self.calculator.add_item('Apple', 99.99, 1)
        shipping = self.calculator.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)
        shipping_free = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping_free, 0.0)

    def test_discount_boundary(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

    def test_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)