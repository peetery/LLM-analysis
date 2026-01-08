import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_parameters_create_valid_instance(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_valid_values_accepted(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_tax_rate_zero_accepted(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_tax_rate_one_accepted(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_free_shipping_threshold_zero_accepted(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_shipping_cost_zero_accepted(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_integer_values_accepted_for_all_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_string_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_none_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_string_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_string_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_items_list_initialized_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_with_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(len(self.calc.items), 2)

    def test_adding_same_name_price_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_price_as_integer_accepted(self):
        self.calc.add_item('Apple', 2)
        self.assertEqual(self.calc.items[0]['price'], 2)

    def test_quantity_of_exactly_one_is_valid(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_very_small_positive_price_is_valid(self):
        self.calc.add_item('Apple', 0.01)
        self.assertEqual(self.calc.items[0]['price'], 0.01)

    def test_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_quantity_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_price_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_name_as_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_name_as_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.5)

    def test_price_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.50')

    def test_quantity_as_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 2.5)

    def test_quantity_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, '2')

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item_successfully(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_one_item_others_remain(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_nonexistent_item_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_name_as_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_name_as_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_single_item_calculates_correctly(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_multiple_items_sums_correctly(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_items_with_quantity_greater_than_one_multiply_correctly(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.assertEqual(self.calc.get_subtotal(), 50.0)

    def test_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_float_precision_maintained(self):
        self.calc.add_item('Apple', 1.99, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 5.97, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_twenty_percent_discount_applied_correctly(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_fifty_percent_discount_halves_subtotal(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_zero_discount_returns_original_subtotal(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_hundred_percent_discount_returns_zero(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_subtotal_zero_with_discount_returns_zero(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_integer_subtotal_accepted(self):
        result = self.calc.apply_discount(100, 0.2)
        self.assertEqual(result, 80.0)

    def test_integer_discount_accepted(self):
        result = self.calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_string_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_string_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_none_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(None, 0.2)

    def test_none_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, None)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_below_threshold_returns_shipping_cost(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_exactly_at_threshold_returns_free_shipping(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_above_threshold_returns_free_shipping(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_zero_subtotal_with_positive_threshold_returns_shipping_cost(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_integer_input_accepted(self):
        result = self.calc.calculate_shipping(50)
        self.assertEqual(result, 10.0)

    def test_string_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_none_input_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_threshold_zero_always_gives_free_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_positive_amount_calculates_tax_correctly(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_zero_amount_returns_zero_tax(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_integer_amount_accepted(self):
        result = self.calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_tax_rate_zero_returns_zero_tax(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_string_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_none_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_without_discount_calculated_correctly(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount_calculated_correctly(self):
        self.calc.add_item('Apple', 100.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = (80.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_includes_shipping_when_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_excludes_shipping_when_above_threshold(self):
        self.calc.add_item('Apple', 150.0, 1)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_at_exact_threshold_gets_free_shipping(self):
        self.calc.add_item('Apple', 100.0, 1)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_default_discount_works(self):
        self.calc.add_item('Apple', 100.0, 1)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_integer_discount_accepted(self):
        self.calc.add_item('Apple', 100.0, 1)
        result = self.calc.calculate_total(0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_invalid_discount_propagates_value_error(self):
        self.calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_string_discount_raises_type_error(self):
        self.calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

    def test_verify_formula_discounted_subtotal_plus_shipping_times_tax(self):
        self.calc.add_item('Apple', 80.0, 1)
        result = self.calc.calculate_total(0.25)
        discounted = 80.0 * 0.75
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(result, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order_returns_zero(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_single_item_returns_its_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_multiple_items_sums_all_quantities(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_after_adding_same_item_twice_quantity_accumulated(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clears_non_empty_order(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clearing_empty_order_does_not_raise_error(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_after_clear_is_empty_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_after_clear_total_items_returns_zero(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order_returns_empty_list(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_returns_all_unique_item_names(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        result = self.calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_adding_same_item_twice_returns_single_name(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        result = self.calc.list_items()
        self.assertEqual(result, ['Apple'])

    def test_multiple_different_items_returns_all_names(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Cherry', 3.0)
        result = self.calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana', 'Cherry'})

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_new_order_is_empty(self):
        self.assertTrue(self.calc.is_empty())

    def test_order_with_items_returns_false(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_after_adding_and_removing_all_items_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_after_clear_order_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_full_order_lifecycle(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Apple', 10.0, 3)
        calc.add_item('Banana', 5.0, 4)
        self.assertEqual(calc.total_items(), 7)
        self.assertEqual(calc.get_subtotal(), 50.0)
        total = calc.calculate_total(0.1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_item_remove_it_verify_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_multiple_discounts_and_shipping_combinations(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Item', 80.0, 1)
        total_no_discount = calc.calculate_total(0.0)
        expected_no_discount = (80.0 + 15.0) * 1.2
        self.assertAlmostEqual(total_no_discount, expected_no_discount, places=2)
        calc.clear_order()
        calc.add_item('Item', 150.0, 1)
        total_with_discount = calc.calculate_total(0.5)
        expected_with_discount = (75.0 + 15.0) * 1.2
        self.assertAlmostEqual(total_with_discount, expected_with_discount, places=2)

    def test_tax_applied_to_discounted_subtotal_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=100.0, shipping_cost=20.0)
        calc.add_item('Product', 80.0, 1)
        total = calc.calculate_total(0.0)
        discounted_subtotal = 80.0
        shipping = 20.0
        tax = (discounted_subtotal + shipping) * 0.25
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_order_with_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 10.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 1000.0)
        self.assertEqual(len(calc.list_items()), 100)

    def test_floating_point_precision_in_final_total(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 33.33, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 99.99, places=2)
        total = calc.calculate_total()
        expected = (99.99 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)