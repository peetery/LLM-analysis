import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_params(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)

    def test_init_custom_params(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.tax_rate, 0.1)
        self.assertEqual(custom_calc.free_shipping_threshold, 200.0)
        self.assertEqual(custom_calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_non_numeric_params(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_single(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_multiple(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 15)
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_add_item_existing_increment(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_add_item_mismatched_price(self):
        self.calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0, 1)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Orange')

    def test_get_subtotal_calculation(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 10)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_get_subtotal_after_removal(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 1.0, 10)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_partial(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_too_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 15.0
        self.assertEqual(self.calc.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_at_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 15.0
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 15.0
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_positive(self):
        self.calc.tax_rate = 0.2
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_rate(self):
        self.calc.tax_rate = 0.0
        self.assertEqual(self.calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.calc.tax_rate = 0.2
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 10.0
        expected = (50.0 + 10.0) * 1.2
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        self.calc.tax_rate = 0.1
        self.calc.free_shipping_threshold = 150.0
        self.calc.shipping_cost = 10.0
        discounted_subtotal = 100.0 * 0.8
        expected = (discounted_subtotal + 10.0) * 1.1
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected)

    def test_calculate_total_qualify_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.calc.tax_rate = 0.1
        self.calc.free_shipping_threshold = 150.0
        self.calc.shipping_cost = 10.0
        expected = 200.0 * 1.1
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_items_count(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removal(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.remove_item('A')
        self.assertTrue(self.calc.is_empty())

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_clear_order_resets_state(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)