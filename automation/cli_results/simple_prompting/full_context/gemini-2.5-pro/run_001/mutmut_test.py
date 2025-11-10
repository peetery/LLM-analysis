from order_calculator import OrderCalculator, Item
import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200, shipping_cost=15)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200)
        self.assertEqual(calc.shipping_cost, 15)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')

    def test_init_invalid_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-100)

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10)

    def test_add_item_new(self):
        self.calculator.add_item('Laptop', 1200.0, 1)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Laptop', 'price': 1200.0, 'quantity': 1})

    def test_add_item_existing(self):
        self.calculator.add_item('Mouse', 25.0, 1)
        self.calculator.add_item('Mouse', 25.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 3)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Keyboard', 75.0)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', 'invalid')

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', -10.0)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Book', 10.0, 'one')

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Book', 10.0, -1)

    def test_add_item_conflicting_price(self):
        self.calculator.add_item('USB-C Cable', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('USB-C Cable', 12.0)

    def test_remove_item_existing(self):
        self.calculator.add_item('Monitor', 300.0)
        self.calculator.remove_item('Monitor')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_non_existing(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('DoesNotExist')

    def test_remove_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(12345)

    def test_get_subtotal_with_items(self):
        self.calculator.add_item('Item A', 10.0, 2)
        self.calculator.add_item('Item B', 5.5, 4)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 42.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10%')

    def test_apply_discount_invalid_discount_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calculator.calculate_shipping(50.0)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('ninety')

    def test_calculate_tax_positive_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('one hundred')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_no_discount_no_free_shipping(self):
        self.calculator.add_item('Product', 80.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 110.7)

    def test_calculate_total_with_discount_no_free_shipping(self):
        self.calculator.add_item('Product', 120.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 130.38)

    def test_calculate_total_with_free_shipping(self):
        self.calculator.add_item('Product', 150.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 184.5)

    def test_calculate_total_with_discount_and_free_shipping(self):
        selfcustom = OrderCalculator(free_shipping_threshold=80)
        selfcustom.add_item('Product', 100.0)
        self.assertAlmostEqual(selfcustom.calculate_total(discount=0.1), 110.7)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Product', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='ten percent')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Item', 1.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_multiple(self):
        self.calculator.add_item('Item A', 1.0, 3)
        self.calculator.add_item('Item B', 1.0, 4)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_clear_order(self):
        self.calculator.add_item('Item A', 1.0)
        self.calculator.add_item('Item B', 2.0)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])
        self.assertTrue(self.calculator.is_empty())

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_with_duplicates(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.add_item('B', 2.0)
        self.calculator.add_item('A', 1.0)
        self.assertEqual(sorted(self.calculator.list_items()), ['A', 'B'])

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())