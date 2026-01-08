import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='invalid')

    def test_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='invalid')

    def test_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='invalid')

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_duplicate_item_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, 2)
        calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Watermelon', 10.0, 100)
        self.assertEqual(calc.items[0]['quantity'], 100)

    def test_empty_item_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 5.0, 1)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 5.0, 0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 5.0, -2)

    def test_duplicate_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 5.0, 1)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'invalid', 1)

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 5.0, 2.5)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_from_multi_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_only_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_subtotal_with_varied_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        calc.add_item('Banana', 3.0, 5)
        calc.add_item('Orange', 1.0, 10)
        self.assertEqual(calc.get_subtotal(), 27.0)

    def test_subtotal_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 3.98)

    def test_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.0)

    def test_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_negative_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.2)

    def test_non_numeric_subtotal_for_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('invalid', 0.2)

    def test_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, 'invalid')

    def test_free_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_paid_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_shipping_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('invalid')

    def test_tax_on_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 15.0)

    def test_tax_on_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('invalid')

    def test_total_without_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected)

    def test_total_without_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 3)
        total = calc.calculate_total()
        expected = 150.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=0.2)
        discounted = 50.0 * 0.8
        expected = discounted + 10.0 + (discounted + 10.0) * 0.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 3)
        total = calc.calculate_total(discount=0.1)
        discounted = 150.0 * 0.9
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected)

    def test_total_at_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 2)
        total = calc.calculate_total()
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected)

    def test_complex_total_calculation(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item('Apple', 25.0, 4)
        calc.add_item('Banana', 10.0, 5)
        total = calc.calculate_total(discount=0.15)
        subtotal = 100.0 + 50.0
        discounted = subtotal * 0.85
        shipping = 15.0
        tax = (discounted + shipping) * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_empty_order_total(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_with_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.5)

    def test_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='invalid')

    def test_empty_order_items_count(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_single_item_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_multiple_items_count(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        calc.add_item('Banana', 2.0, 5)
        calc.add_item('Orange', 3.0, 2)
        self.assertEqual(calc.total_items(), 10)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        calc.add_item('Banana', 2.0, 2)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_and_verify_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 3)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_from_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.add_item('Orange', 3.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_with_duplicate_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Apple', 5.0, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items, ['Apple'])

    def test_empty_order_check(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_non_empty_order_check(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        self.assertFalse(calc.is_empty())

    def test_empty_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_full_order_lifecycle(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        total = calc.calculate_total()
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_discount_affecting_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Apple', 60.0, 2)
        total_with_discount = calc.calculate_total(discount=0.2)
        discounted = 120.0 * 0.8
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total_with_discount, expected)

    def test_discount_affecting_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Apple', 60.0, 2)
        total_no_discount = calc.calculate_total(discount=0.0)
        discounted = 120.0
        shipping = 0.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total_no_discount, expected)

    def test_multiple_add_remove_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        calc.add_item('Banana', 3.0, 1)
        calc.remove_item('Apple')
        calc.add_item('Orange', 4.0, 3)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Orange')

    def test_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_large_quantities_and_prices(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 999999.99, 1000)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 999999990.0)

    def test_item_persistence_after_failed_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        try:
            calc.add_item('Apple', 10.0, 1)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['price'], 5.0)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_parameter_persistence(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item('Apple', 10.0, 5)
        calc.calculate_total()
        calc.clear_order()
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_order_state_after_exceptions(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, 2)
        initial_count = len(calc.items)
        try:
            calc.add_item('', 10.0, 1)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), initial_count)