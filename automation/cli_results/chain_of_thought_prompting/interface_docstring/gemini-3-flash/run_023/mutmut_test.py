import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 40.0, 1)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)

    def test_init_tax_rate_boundaries(self):
        calc_min = OrderCalculator(tax_rate=0.0)
        calc_max = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_min.calculate_tax(100.0), 0.0)
        self.assertEqual(calc_max.calculate_tax(100.0), 100.0)

    def test_init_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(0.0), 0.0)

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.total_items(), 8)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(set(calc.list_items()), {'Apple', 'Banana'})

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.0, 1)

    def test_add_item_non_positive_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 0)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0, 1)

    def test_add_item_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0, 1)
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '2.0', 1)
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 2.0, 1.5)

    def test_remove_item_typical(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.is_empty(), True)

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_typical(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Banana', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_typical(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_full_flow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 2)
        total = calc.calculate_total(discount=0.2)
        subtotal = 100.0
        discounted = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.1
        expected = 80.0 + 10.0 + 9.0
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        total = calc.calculate_total(discount=0.1)
        discounted = 180.0
        shipping = 0.0
        tax = 180.0 * 0.1
        expected = 180.0 + 18.0
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_paid_shipping(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 60.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_type(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 10)
        calc.add_item('B', 1.0, 5)
        self.assertEqual(calc.total_items(), 15)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.clear_order()
        self.assertEqual(calc.is_empty(), True)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.add_item('B', 2.0, 1)
        self.assertEqual(set(calc.list_items()), {'A', 'B'})

    def test_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('A', 1.0, 1)
        self.assertFalse(calc.is_empty())