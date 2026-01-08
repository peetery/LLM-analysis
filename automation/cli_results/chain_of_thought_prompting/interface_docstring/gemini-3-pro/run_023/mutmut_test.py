import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.tax_rate, 0.23)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calculator.tax_rate, 0.05)
        self.assertAlmostEqual(calculator.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        self.assertFalse(calculator.is_empty())
        self.assertEqual(calculator.total_items(), 10)
        self.assertIn('Apple', calculator.list_items())

    def test_add_item_existing_update_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 5)
        calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(calculator.total_items(), 8)

    def test_add_item_default_quantity(self):
        calculator = OrderCalculator()
        calculator.add_item('Banana', 0.5)
        self.assertEqual(calculator.total_items(), 1)

    def test_add_item_empty_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 1.0, -5)

    def test_add_item_duplicate_name_diff_price(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            calculator.add_item('Apple', '1.0')

    def test_remove_item_existing(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5)
        calculator.remove_item('Apple')
        self.assertTrue(calculator.is_empty())

    def test_remove_item_non_existent(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item('Ghost')

    def test_remove_item_type_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_get_subtotal_calculation(self):
        calculator = OrderCalculator()
        calculator.add_item('Item1', 10.0, 2)
        calculator.add_item('Item2', 5.0, 3)
        self.assertAlmostEqual(calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_valid(self):
        calculator = OrderCalculator()
        discounted = calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(discounted, 80.0)

    def test_apply_discount_zero(self):
        calculator = OrderCalculator()
        discounted = calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(discounted, 100.0)

    def test_apply_discount_full(self):
        calculator = OrderCalculator()
        discounted = calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(discounted, 0.0)

    def test_apply_discount_invalid_negative(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_too_high(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.apply_discount('100', 0.1)

    def test_calculate_shipping_standard(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(99.9)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_free(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(101.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calculator = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calculator.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_type_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calculator = OrderCalculator(tax_rate=0.23)
        tax = calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        calculator = OrderCalculator(tax_rate=0.23)
        tax = calculator.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.calculate_tax('100')

    def test_calculate_total_standard(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 50.0, 1)
        total = calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 72.0)

    def test_calculate_total_free_shipping(self):
        calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calculator.add_item('Item', 100.0, 1)
        total = calculator.calculate_total()
        self.assertAlmostEqual(total, 120.0)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=-0.1)

    def test_total_items_multiple(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 1.0, 2)
        calculator.add_item('B', 1.0, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_total_items_empty(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.total_items(), 0)

    def test_list_items_populated(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 1.0)
        calculator.add_item('B', 2.0)
        items = calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.list_items(), [])

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 1.0)
        self.assertFalse(calculator.is_empty())

    def test_clear_order(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 1.0)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.total_items(), 0)