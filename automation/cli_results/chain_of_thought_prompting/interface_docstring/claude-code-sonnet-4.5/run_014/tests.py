import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_wrong_type_tax_rate_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_wrong_type_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_wrong_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_multiple_different(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_add_item_duplicate_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 10.0, 150)
        self.assertEqual(calc.total_items(), 150)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Free Item', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Negative', -1.5, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Zero Qty', 1.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Negative Qty', 1.5, -1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_wrong_type_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_add_item_wrong_type_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_add_item_wrong_type_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Penny Item', 0.01, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 0.01)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 999999.99, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 999999.99)

    def test_add_item_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 1.5, 1)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_after_multiple_adds(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_wrong_type_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_item_then_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_remove_item_case_sensitivity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('apple', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertAlmostEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.3)

    def test_get_subtotal_large_amount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 100.0, 10)
        calc.add_item('Item2', 200.0, 5)
        self.assertAlmostEqual(calc.get_subtotal(), 2000.0)

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_maximum(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_wrong_type_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_wrong_type_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(123.45, 0.15)
        self.assertAlmostEqual(result, 104.9325)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_equals_threshold(self):
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

    def test_calculate_shipping_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_precision(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(123.45)
        self.assertAlmostEqual(tax, 28.3935)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=0.2)
        expected = 80.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 200.0, 1)
        total = calc.calculate_total()
        expected = 200.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_shipping_cost(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_complete_chain(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 60.0, 2)
        calc.add_item('Item2', 40.0, 1)
        total = calc.calculate_total(discount=0.1)
        subtotal = 160.0
        discounted = subtotal * 0.9
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_wrong_type_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_calculate_total_at_free_shipping_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        shipping = 0.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_just_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 99.99, 1)
        total = calc.calculate_total()
        expected = (99.99 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_just_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.01, 1)
        total = calc.calculate_total()
        expected = 100.01 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_affecting_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(discount=0.25)
        discounted = 93.75
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.add_item('Orange', 2.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_operations_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 0.5, 1)
        calc.add_item('Orange', 2.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Apple')

    def test_list_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 0.5, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_calculator(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add_then_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        total = calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_multiple_discounts(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(discount=0.1)
        total2 = calc.calculate_total(discount=0.2)
        self.assertGreater(total1, total2)

    def test_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_discount_brings_total_below_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(discount=0.25)
        discounted = 93.75
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_discount_brings_total_to_exactly_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_precision_in_complete_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 3)
        calc.add_item('Item2', 0.2, 2)
        total = calc.calculate_total(discount=0.1)
        subtotal = 0.7
        discounted = subtotal * 0.9
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_very_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 10.0, 5)
        total = calc.calculate_total()
        self.assertGreater(total, 0)

    def test_multiple_calculators_independence(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Apple', 1.5, 1)
        calc2.add_item('Banana', 0.5, 1)
        self.assertEqual(calc1.total_items(), 1)
        self.assertEqual(calc2.total_items(), 1)
        self.assertNotEqual(calc1.list_items(), calc2.list_items())

    def test_parameter_immutability(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 100.0, 1)
        calc.calculate_total()
        self.assertEqual(calc.tax_rate, 0.2)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)