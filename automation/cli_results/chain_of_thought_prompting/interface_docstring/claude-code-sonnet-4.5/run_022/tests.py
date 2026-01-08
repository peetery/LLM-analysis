import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_valid_parameters(self):
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

    def test_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_empty_items_list(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_string_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_string_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_string_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_none_parameters(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_list_parameters(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

class TestAddRemoveItems(unittest.TestCase):

    def test_add_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.8)
        self.assertEqual(calc.total_items(), 3)

    def test_add_duplicate_item_same_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_float_price_values(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, quantity=1)
        self.assertAlmostEqual(calc.get_subtotal(), 19.99)

    def test_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, quantity=1000)
        self.assertEqual(calc.total_items(), 1000)

    def test_empty_name_string(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_whitespace_only_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('   ', 10.0)

    def test_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0.0)

    def test_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=0)

    def test_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 10.0, quantity=-1)

    def test_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 10.0)

    def test_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10')

    def test_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 10.0, quantity=1.5)

    def test_none_as_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', None)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 1)
        self.assertIn('Banana', calc.list_items())

    def test_remove_item_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_already_removed_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_case_sensitive_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_none_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_list_as_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(['item'])

class TestCalculations(unittest.TestCase):

    def test_single_item_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertAlmostEqual(calc.get_subtotal(), 1.5)

    def test_multiple_items_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 9.0)

    def test_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=10)
        self.assertAlmostEqual(calc.get_subtotal(), 50.0)

    def test_multiple_items_with_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, quantity=2)
        calc.add_item('B', 5.0, quantity=5)
        calc.add_item('C', 2.5, quantity=4)
        self.assertAlmostEqual(calc.get_subtotal(), 55.0)

    def test_floating_point_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item', 19.99, quantity=3)
        self.assertAlmostEqual(calc.get_subtotal(), 59.97)

    def test_empty_order_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_hundred_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_fifty_percent_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertAlmostEqual(result, 99.0)

    def test_negative_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.5)

    def test_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_string_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.5)

    def test_string_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_none_as_subtotal_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.5)

    def test_none_as_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_far_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(1000.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_shipping_just_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

    def test_shipping_string_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_shipping_none_as_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_shipping_list_as_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping([100.0])

    def test_tax_positive_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_tax_various_tax_rates(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 15.0)

    def test_tax_large_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(10000.0)
        self.assertAlmostEqual(tax, 2300.0)

    def test_tax_small_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023)

    def test_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_tax_string_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_tax_none_as_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

class TestTotalCalculation(unittest.TestCase):

    def test_total_with_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 80.0
        with_shipping = 80.0
        expected = with_shipping * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_shipping_cost(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_single_item_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, quantity=1)
        total = calc.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_multiple_items_total(self):
        calc = OrderCalculator()
        calc.add_item('A', 30.0, quantity=1)
        calc.add_item('B', 20.0, quantity=1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_zero_discount_default(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, quantity=1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_hundred_percent_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=1)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_high_discount_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 200.0, quantity=1)
        total = calc.calculate_total(discount=0.5)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_empty_order_total(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_invalid_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_negative_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_discount_above_hundred_percent(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_string_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_none_as_discount_total(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount=None)

class TestUtilityMethods(unittest.TestCase):

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=10)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 8)

    def test_total_items_after_removing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_state_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 1.8)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_order_of_names(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        items = calc.list_items()
        self.assertEqual(set(items), {'Apple', 'Banana'})

    def test_list_items_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add_then_remove_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

class TestIntegrationWorkflows(unittest.TestCase):

    def test_full_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('A', 20.0, quantity=2)
        calc.add_item('B', 30.0, quantity=1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 70.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 63.0)
        total = calc.calculate_total(discount=0.1)
        expected = (63.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_shipping_threshold_edge_case(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_multiple_operations(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0)
        calc.remove_item('A')
        calc.add_item('C', 30.0)
        total = calc.calculate_total()
        subtotal = 50.0
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_quantity_accumulation_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 5.0, quantity=2)
        calc.add_item('Apple', 5.0, quantity=3)
        calc.add_item('Apple', 5.0, quantity=5)
        self.assertEqual(calc.total_items(), 10)
        self.assertAlmostEqual(calc.get_subtotal(), 50.0)

    def test_tax_calculation_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 80.0
        expected = 80.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_free_shipping_qualification(self):
        calc = OrderCalculator()
        calc.add_item('A', 50.0, quantity=1)
        calc.add_item('B', 50.0, quantity=1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, quantity=2)
        calc.add_item('B', 20.0, quantity=3)
        calc.remove_item('A')
        self.assertEqual(calc.total_items(), 3)
        self.assertIn('B', calc.list_items())
        self.assertNotIn('A', calc.list_items())
        self.assertFalse(calc.is_empty())

    def test_floating_point_precision(self):
        calc = OrderCalculator()
        calc.add_item('A', 19.99, quantity=3)
        calc.add_item('B', 5.49, quantity=2)
        subtotal = calc.get_subtotal()
        expected_subtotal = 19.99 * 3 + 5.49 * 2
        self.assertAlmostEqual(subtotal, expected_subtotal, places=2)

    def test_large_order_calculation(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, quantity=100)
        calc.add_item('B', 5.0, quantity=200)
        calc.add_item('C', 2.5, quantity=50)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 2125.0)
        total = calc.calculate_total()
        expected = 2125.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_discount_impact_on_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item', 120.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 96.0
        expected = (96.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_exact_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, quantity=1)
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_tax_on_zero_with_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, quantity=1)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_minimal_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.01, quantity=1)
        total = calc.calculate_total()
        expected = (0.01 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=4)