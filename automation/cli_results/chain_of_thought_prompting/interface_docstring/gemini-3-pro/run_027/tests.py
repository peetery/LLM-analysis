import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.total_items(), 0)

    def test_init_custom(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calculator.is_empty())

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='high')

    def test_add_item_new(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(calculator.total_items(), 10)
        self.assertIn('Apple', calculator.list_items())

    def test_add_item_duplicate_merge(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        calculator.add_item('Apple', 1.5, 5)
        self.assertEqual(calculator.total_items(), 15)
        self.assertEqual(len(calculator.list_items()), 1)

    def test_add_item_name_conflict(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 2.0, 5)

    def test_add_item_invalid_name(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('', 1.5, 1)

    def test_add_item_invalid_price(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            calculator.add_item('Orange', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.add_item('Apple', 1.5, 0)

    def test_remove_item_existing(self):
        calculator = OrderCalculator()
        calculator.add_item('Apple', 1.5, 10)
        calculator.remove_item('Apple')
        self.assertTrue(calculator.is_empty())

    def test_remove_item_non_existent(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        calculator = OrderCalculator()
        with self.assertRaises(TypeError):
            calculator.remove_item(123)

    def test_total_items(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10, 2)
        calculator.add_item('B', 20, 3)
        self.assertEqual(calculator.total_items(), 5)

    def test_list_items(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10, 1)
        calculator.add_item('B', 20, 1)
        items = calculator.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_is_empty_true(self):
        calculator = OrderCalculator()
        self.assertTrue(calculator.is_empty())

    def test_is_empty_false(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10, 1)
        self.assertFalse(calculator.is_empty())

    def test_clear_order(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10, 1)
        calculator.clear_order()
        self.assertTrue(calculator.is_empty())
        self.assertEqual(calculator.total_items(), 0)

    def test_get_subtotal_success(self):
        calculator = OrderCalculator()
        calculator.add_item('A', 10.0, 2)
        calculator.add_item('B', 5.5, 4)
        self.assertAlmostEqual(calculator.get_subtotal(), 42.0)

    def test_get_subtotal_empty(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.get_subtotal()

    def test_apply_discount_success(self):
        calculator = OrderCalculator()
        result = calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_edges(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_rate(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_on_threshold(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_success(self):
        calculator = OrderCalculator()
        self.assertAlmostEqual(calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_tax(-50.0)

    def test_calculate_total_standard_with_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calculator.calculate_total(), 246.0)

    def test_calculate_total_empty_order(self):
        calculator = OrderCalculator()
        with self.assertRaises(ValueError):
            calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calculator = OrderCalculator()
        calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calculator.calculate_total(discount=1.5)