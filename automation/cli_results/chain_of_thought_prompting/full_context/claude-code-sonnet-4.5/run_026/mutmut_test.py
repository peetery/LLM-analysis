import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_custom_parameters(self):
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

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_string_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_string_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_string_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_none_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_list_as_parameter_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_with_default_quantity(self):
        self.calc.add_item('Apple', 1.0)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        self.calc.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_same_name_and_price(self):
        self.calc.add_item('Orange', 2.0, 3)
        self.calc.add_item('Orange', 2.0, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(len(self.calc.items), 3)

    def test_add_item_with_float_price(self):
        self.calc.add_item('Grape', 19.99)
        self.assertEqual(self.calc.items[0]['price'], 19.99)

    def test_add_item_with_large_quantity(self):
        self.calc.add_item('Watermelon', 5.0, 1000)
        self.assertEqual(self.calc.items[0]['quantity'], 1000)

    def test_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_non_numeric_price_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')

    def test_float_quantity_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, 5.5)

    def test_none_as_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.0)

    def test_empty_string_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)

    def test_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -10.0)

    def test_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_whitespace_only_name(self):
        self.calc.add_item('   ', 1.0)
        self.assertEqual(self.calc.items[0]['name'], '   ')

    def test_very_small_positive_price(self):
        self.calc.add_item('Penny Candy', 0.0001)
        self.assertEqual(self.calc.items[0]['price'], 0.0001)

    def test_incrementing_quantity_multiple_times(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.items[0]['quantity'], 3)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_from_multiple_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.add_item('Orange', 2.0)
        self.calc.remove_item('Banana')
        self.assertEqual(len(self.calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in self.calc.items])

    def test_remove_last_remaining_item(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_none_as_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_item_does_not_exist_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_single_item_subtotal(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_multiple_items_subtotal(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 4.0)

    def test_item_with_quantity_greater_than_one(self):
        self.calc.add_item('Orange', 3.0, 10)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_multiple_quantities(self):
        self.calc.add_item('Apple', 2.0, 3)
        self.calc.add_item('Banana', 1.5, 2)
        self.calc.add_item('Orange', 4.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 13.0)

    def test_empty_order_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_very_large_subtotal(self):
        self.calc.add_item('Expensive Item', 999.99, 100)
        self.assertEqual(self.calc.get_subtotal(), 99999.0)

    def test_fractional_prices(self):
        self.calc.add_item('Item1', 19.99, 2)
        self.calc.add_item('Item2', 9.99, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 69.95, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_no_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_partial_discount_twenty_percent(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_full_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_discount_on_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_fifty_percent_discount(self):
        result = self.calc.apply_discount(200.0, 0.5)
        self.assertEqual(result, 100.0)

    def test_string_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_string_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_none_values_raise_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(None, 0.2)

    def test_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.2)

    def test_very_small_discount(self):
        result = self.calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_integer_parameters(self):
        result = self.calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_zero_subtotal(self):
        shipping = self.calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_just_below_threshold(self):
        shipping = self.calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_string_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50.0')

    def test_none_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_different_tax_rates(self):
        calc1 = OrderCalculator(tax_rate=0.0)
        calc2 = OrderCalculator(tax_rate=0.1)
        calc3 = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc1.calculate_tax(100.0), 0.0)
        self.assertEqual(calc2.calculate_tax(100.0), 10.0)
        self.assertEqual(calc3.calculate_tax(100.0), 100.0)

    def test_string_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100.0')

    def test_none_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-50.0)

    def test_very_large_amount(self):
        tax = self.calc.calculate_tax(10000.0)
        self.assertEqual(tax, 2300.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_no_discount_no_free_shipping(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_with_discount_no_free_shipping(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total(discount=0.2)
        expected = (40.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_no_discount_free_shipping(self):
        self.calc.add_item('Apple', 10.0, 15)
        total = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_with_discount_free_shipping(self):
        self.calc.add_item('Apple', 10.0, 20)
        total = self.calc.calculate_total(discount=0.1)
        expected = 180.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_complex_scenario(self):
        self.calc.add_item('Apple', 5.0, 10)
        self.calc.add_item('Banana', 2.5, 8)
        total = self.calc.calculate_total(discount=0.15)
        subtotal = 70.0
        discounted = 59.5
        shipping = 10.0
        tax = (59.5 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_default_discount(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_string_discount_raises_type_error(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.2')

    def test_none_discount_raises_type_error(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount=None)

    def test_invalid_discount_raises_value_error(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_discount_affects_free_shipping(self):
        self.calc.add_item('Apple', 11.0, 10)
        total = self.calc.calculate_total(discount=0.15)
        discounted_subtotal = 93.5
        self.assertLess(discounted_subtotal, 100.0)
        expected = (93.5 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_calculated_on_subtotal_plus_shipping(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total()
        base = 50.0 + 10.0
        tax = base * 0.23
        expected = base + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_full_discount_with_shipping(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total(discount=1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_boundary_discount(self):
        calc = OrderCalculator(free_shipping_threshold=80.0)
        calc.add_item('Apple', 10.0, 10)
        total = calc.calculate_total(discount=0.2)
        discounted_subtotal = 80.0
        self.assertEqual(discounted_subtotal, 80.0)
        expected = 80.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 3)
        self.calc.add_item('Banana', 0.5, 2)
        self.calc.add_item('Orange', 2.0, 4)
        self.assertEqual(self.calc.total_items(), 9)

    def test_after_adding_duplicate(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_after_removing_item(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Banana', 0.5, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

    def test_after_clearing_order(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_non_empty_order(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_and_verify_state(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_then_add(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_multiple_clears(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.calc.clear_order()
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_single_item(self):
        self.calc.add_item('Apple', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_multiple_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.add_item('Orange', 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_duplicate_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_after_removal(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.remove_item('Apple')
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_order_of_names(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_initially_empty(self):
        self.assertTrue(self.calc.is_empty())

    def test_after_adding_item(self):
        self.calc.add_item('Apple', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_after_clearing(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_multiple_items_then_clear(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 0.5)
        self.calc.add_item('Orange', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_full_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 2)
        total = calc.calculate_total(discount=0.1)
        subtotal = 40.0
        discounted = 36.0
        shipping = 5.0
        tax = (36.0 + 5.0) * 0.2
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 0.5, 3)
        calc.remove_item('Apple')
        calc.add_item('Orange', 2.0, 2)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 2)

    def test_calculation_chain(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 20.0, 3)
        total = calc.calculate_total(discount=0.25)
        subtotal = calc.get_subtotal()
        discounted = calc.apply_discount(subtotal, 0.25)
        shipping = calc.calculate_shipping(discounted)
        tax = calc.calculate_tax(discounted + shipping)
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_edge_case_totals(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Apple', 20.0, 5)
        total = calc.calculate_total()
        discounted_subtotal = 100.0
        self.assertEqual(discounted_subtotal, 100.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_type_coercion_consistency(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        calc.add_item('Apple', 10, 5)
        total = calc.calculate_total(discount=0)
        expected = 50 + 10
        self.assertEqual(total, expected)

    def test_multiple_item_types(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1000)
        calc.add_item('Expensive', 999.99, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1009.99, places=2)