import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
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

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 1000.0, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Laptop')
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Mouse', 25.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 1.0, 5)
        calc.add_item('Pen', 1.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 8)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 1.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Pen', 1.5, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_type_error_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_type_error_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_add_item_type_error_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, 1.5)

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0)
        calc.remove_item('Item1')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Ghost')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 20.0)

    def test_get_subtotal_multiple(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_none(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_partial(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_range_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_standard(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        tax = (50.0 + 10.0) * 0.1
        expected = 50.0 + 10.0 + tax
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), expected)

    def test_calculate_total_discounted_paid_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        discounted_subtotal = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.1
        expected = 80.0 + 10.0 + tax
        self.assertAlmostEqual(calc.calculate_total(discount=0.2), expected)

    def test_calculate_total_discounted_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        discounted_subtotal = 160.0
        shipping = 0.0
        tax = 160.0 * 0.1
        expected = 160.0 + tax
        self.assertAlmostEqual(calc.calculate_total(discount=0.2), expected)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_type_error_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='high')

    def test_total_items_metadata(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_list_items_unique(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        calc.add_item('B', 10.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_new(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_filled(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        self.assertFalse(calc.is_empty())

    def test_clear_order_logic(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(len(calc.items), 0)

    def test_precision_floats(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Widget', 9.99, 3)
        subtotal = 9.99 * 3
        expected_tax = (subtotal + 10.0) * 0.23
        expected_total = subtotal + 10.0 + expected_tax
        self.assertAlmostEqual(calc.calculate_total(), expected_total)