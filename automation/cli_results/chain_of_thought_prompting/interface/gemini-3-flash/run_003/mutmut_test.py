import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(49.0), 5.0)
        self.assertEqual(calc.calculate_shipping(51.0), 0.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)
        self.assertEqual(calc.calculate_shipping(10.0), 0.0)

    def test_add_item_normal(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Laptop', self.calc.list_items())

    def test_add_item_specific_quantity(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_existing_item_updates_quantity(self):
        self.calc.add_item('Mouse', 25.0, 1)
        self.calc.add_item('Mouse', 25.0, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -10.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, -5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_in_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_get_subtotal_single_item(self):
        self.calc.add_item('A', 10.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount_zero_discount(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_negative_discount_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_for_zero_subtotal(self):
        self.assertEqual(self.calc.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_positive_amount(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_total_items_multiple_entries(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_returns_names(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_empty_order_returns_empty_list(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clearing(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())