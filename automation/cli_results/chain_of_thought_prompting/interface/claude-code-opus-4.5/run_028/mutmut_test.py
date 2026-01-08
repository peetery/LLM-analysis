import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(100), 10.0)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)
        self.assertEqual(calc.calculate_shipping(49), 10.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(50), 15.0)

    def test_init_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.calculate_tax(100), 5.0)
        self.assertEqual(calc.calculate_shipping(199), 20.0)
        self.assertEqual(calc.calculate_shipping(200), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.calculate_shipping(0), 0.0)

    def test_add_item_single_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_add_item_single_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Orange', 3.0)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(len(calc.list_items()), 3)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('NegativeItem', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.5, -1)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.total_items(), 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 1000000.0)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError)):
            calc.add_item('Apple', 2.5, 1.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_empty_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_then_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Orange', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.list_items()), 2)
        self.assertNotIn('Banana', calc.list_items())

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.get_subtotal(), 2.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Orange', 3.0)
        self.assertEqual(calc.get_subtotal(), 7.0)

    def test_get_subtotal_items_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_get_subtotal_after_adding_and_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10)

    def test_apply_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 110)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(-50.0), 10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=4)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_paid_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_custom_constructor_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=200.0, shipping_cost=25.0)
        calc.add_item('Item', 150.0)
        total = calc.calculate_total(0)
        expected = 150.0 + 25.0 + 175.0 * 0.05
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-10)

    def test_calculate_total_discount_greater_than_hundred(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(110)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Orange', 3.0)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_adding(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.total_items(), 1)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_removing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 2)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_verify_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.remove_item('Apple')
        self.assertNotIn('Apple', calc.list_items())
        self.assertIn('Banana', calc.list_items())

    def test_is_empty_empty_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_add_item(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 2.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_remove_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.add_item('Banana', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_remove_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5)
        calc.remove_item('Apple')
        calc.add_item('Apple', 3.0)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_multiple_operations_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0, 2)
        calc.remove_item('A')
        calc.add_item('C', 5.0)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 45.0)
        self.assertEqual(len(calc.list_items()), 2)

    def test_order_modification_after_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total1 = calc.calculate_total()
        calc.add_item('Banana', 25.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_boundary_at_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)