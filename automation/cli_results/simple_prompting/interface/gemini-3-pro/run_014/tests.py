import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 40.0)
        self.assertFalse(calc.is_empty())

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_cumulative_quantity(self):
        self.calc.add_item('Orange', 1.0, 2)
        self.calc.add_item('Orange', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_invalid_input(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQtyNegative', 5.0, -1)
        with self.assertRaises(ValueError):
            self.calc.add_item('', 5.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('WrongType', '10.0')

    def test_remove_item_existing(self):
        self.calc.add_item('Tablet', 300.0)
        self.calc.remove_item('Tablet')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('NonExistentItem')

    def test_get_subtotal_mixed_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.5)

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(50.0, 0.0)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(50.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(100.01)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-50.0)

    def test_calculate_tax(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total(discount=0.0)
        subtotal = 50.0
        shipping = self.calc.calculate_shipping(subtotal)
        expected_tax = self.calc.calculate_tax(subtotal + shipping)
        expected_total = subtotal + shipping + expected_tax
        self.assertAlmostEqual(total, expected_total)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calc.add_item('ExpensiveItem', 200.0)
        total = self.calc.calculate_total(discount=0.1)
        subtotal = 200.0
        discounted = self.calc.apply_discount(subtotal, 0.1)
        shipping = self.calc.calculate_shipping(discounted)
        tax = self.calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_discount_drops_below_threshold(self):
        self.calc.add_item('BorderlineItem', 110.0)
        total = self.calc.calculate_total(discount=0.2)
        discounted = 88.0
        shipping = 10.0
        tax = self.calc.calculate_tax(discounted + shipping)
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_empty(self):
        self.assertEqual(self.calc.calculate_total(), 0.0)

    def test_total_items_mixed(self):
        self.calc.add_item('A', 1, 5)
        self.calc.add_item('B', 2, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items(self):
        self.calc.add_item('Apples', 1.0)
        self.calc.add_item('Bananas', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apples', items)
        self.assertIn('Bananas', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Something', 1.0)
        self.assertFalse(self.calc.is_empty())