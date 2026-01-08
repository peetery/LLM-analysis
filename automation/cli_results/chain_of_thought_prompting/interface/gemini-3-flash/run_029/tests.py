import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 5.0)

    def test_init_zero_values(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_init_negative_tax(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single_qty_1(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.0)

    def test_add_item_single_qty_greater_1(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 8.0)

    def test_add_item_zero_price(self):
        self.calc.add_item('Freebie', 0.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_duplicate_name(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Error', -1.0, 1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Error', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Error', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item(self):
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('Nonexistent')

    def test_remove_only_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_from_empty_order(self):
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('Apple')

    def test_get_subtotal_normal(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.5, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_get_subtotal_after_removal(self):
        self.calc.add_item('Item1', 10.0, 1)
        self.calc.add_item('Item2', 20.0, 1)
        self.calc.remove_item('Item1')
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_apply_discount_normal(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_equal_to_subtotal(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_greater_than_subtotal(self):
        result = self.calc.apply_discount(100.0, 150.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(self.calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calc.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_normal(self):
        self.calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_rate(self):
        self.calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(self.calc.calculate_tax(100.0), 0.0)

    def test_calculate_total_standard(self):
        self.calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        self.calc.add_item('Item', 50.0, 1)
        self.assertEqual(self.calc.calculate_total(0.0), 65.0)

    def test_calculate_total_free_shipping(self):
        self.calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        self.calc.add_item('Item', 150.0, 1)
        self.assertEqual(self.calc.calculate_total(50.0), 110.0)

    def test_calculate_total_empty(self):
        self.calc = OrderCalculator(tax_rate=0.2, shipping_cost=10.0)
        self.assertEqual(self.calc.calculate_total(), 10.0)

    def test_calculate_total_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-10.0)

    def test_total_items_normal(self):
        self.calc.add_item('A', 1.0, 2)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_normal(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items_normal(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 1.0, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])