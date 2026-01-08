import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_success_default_qty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_add_item_success_custom_qty(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5, quantity=10)
        self.assertEqual(calc.total_items(), 10)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_accumulate_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2.0, quantity=3)
        calc.add_item('Orange', 2.0, quantity=2)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_add_item_name_conflict_diff_price(self):
        calc = OrderCalculator()
        calc.add_item('Milk', 3.0)
        with self.assertRaises(ValueError):
            calc.add_item('Milk', 4.0)

    def test_add_item_invalid_name_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_invalid_price_zero_or_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('FreeItem', 0.0)
        with self.assertRaises(ValueError):
            calc.add_item('NegativePrice', -5.0)

    def test_add_item_invalid_quantity_zero_or_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=0)

    def test_add_item_type_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Book', 15.0)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        subtotal = 100.0
        discounted = calc.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(discounted, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        subtotal = 100.0
        discounted = calc.apply_discount(subtotal, 0.0)
        self.assertAlmostEqual(discounted, 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        subtotal = 100.0
        discounted = calc.apply_discount(subtotal, 1.0)
        self.assertAlmostEqual(discounted, 0.0)

    def test_apply_discount_invalid_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50.0')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100.0')

    def test_calculate_total_standard_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 66.0)

    def test_calculate_total_free_shipping_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('ExpensiveItem', 200.0)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_total_items_sum(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.add_item('B', 1.0)
        items = calc.list_items()
        self.assertEqual(set(items), {'A', 'B'})
        self.assertEqual(len(items), 2)

    def test_is_empty_state_check(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Item', 1.0)
        self.assertFalse(calc.is_empty())

    def test_clear_order_reset(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)