import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_add_item_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        self.assertEqual(len(calc.list_items()), 2)

    def test_add_item_duplicate_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)
        self.assertAlmostEqual(calc.get_subtotal(), 4.5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        calc.add_item('Free Item', 0.0)
        self.assertAlmostEqual(calc.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, -2)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_none_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item(None, 10.0)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk', 1.0, 100000)
        self.assertEqual(calc.total_items(), 100000)

    def test_add_item_float_price_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 59.97, places=2)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        with self.assertRaises(KeyError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('Apple')

    def test_remove_item_last_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(KeyError):
            calc.remove_item('')

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 7.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 2)
        calc.add_item('Banana', 3.0, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 7.0)

    def test_get_subtotal_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 4)
        calc.add_item('Banana', 2.5, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 11.0)

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        calc.add_item('Item2', 0.2, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 0.7, places=2)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_partial(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 10.0)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_exceeds_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 150.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 10.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_negative_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(-10.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=2)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(-100.0)
        self.assertAlmostEqual(tax, -23.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0)
        total = calc.calculate_total(20.0)
        discounted = 80.0
        shipping = 10.0
        tax = 90.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 150.0)
        total = calc.calculate_total(0.0)
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_integration(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 40.0, 2)
        calc.add_item('Item2', 30.0, 1)
        total = calc.calculate_total(10.0)
        subtotal = 110.0
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_affects_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 105.0)
        total = calc.calculate_total(10.0)
        discounted = 95.0
        shipping = 10.0
        tax = 105.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, 3)
        total = calc.calculate_total(5.5)
        subtotal = 59.97
        discounted = 54.47
        shipping = 10.0
        tax = 64.47 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_tax_calculation_base(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        total = calc.calculate_total(0.0)
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 2.0, 2)
        calc.add_item('Orange', 1.5, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_resets_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        calc.clear_order()
        self.assertAlmostEqual(calc.get_subtotal(), 0.0)
        self.assertEqual(calc.total_items(), 0)
        self.assertAlmostEqual(calc.calculate_total(), 0.0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.5)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)
        self.assertEqual(len(items), 3)

    def test_list_items_order_preservation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.5)
        items = calc.list_items()
        self.assertEqual(items, ['Apple', 'Banana', 'Orange'])

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_workflow_add_calculate_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        calc.add_item('Banana', 30.0)
        total1 = calc.calculate_total(0.0)
        self.assertGreater(total1, 0.0)
        calc.remove_item('Banana')
        total2 = calc.calculate_total(0.0)
        self.assertLess(total2, total1)

    def test_workflow_discount_scenario(self):
        calc = OrderCalculator()
        calc.add_item('Laptop', 800.0)
        calc.add_item('Mouse', 20.0)
        calc.add_item('Keyboard', 50.0)
        total_no_discount = calc.calculate_total(0.0)
        total_with_discount = calc.calculate_total(100.0)
        self.assertLess(total_with_discount, total_no_discount)

    def test_workflow_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 60.0)
        calc.add_item('Item2', 40.0)
        total1 = calc.calculate_total(0.0)
        calc.remove_item('Item2')
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)

    def test_workflow_clear_and_reuse(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.calculate_total(0.0)
        calc.clear_order()
        calc.add_item('Banana', 20.0)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0.0)
        self.assertEqual(calc.total_items(), 1)