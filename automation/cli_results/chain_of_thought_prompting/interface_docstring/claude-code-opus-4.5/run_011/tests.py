import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

class TestOrderCalculatorAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_add_same_item_twice_aggregates_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_quantity_one_minimum_valid(self):
        self.calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_small_valid_price(self):
        self.calc.add_item('Candy', 0.01)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_whitespace_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('   ', 1.5)

    def test_add_item_price_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_quantity_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_name_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_price_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.50')

    def test_add_item_quantity_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, quantity=2.5)

class TestOrderCalculatorRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_verifies_order_state(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.list_items(), ['Banana'])

    def test_remove_nonexistent_item_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_name_integer_raises_type_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

class TestOrderCalculatorGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Banana', 2.0, quantity=3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 9.0)

    def test_get_subtotal_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 10.0, quantity=5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_get_subtotal_small_price(self):
        self.calc.add_item('Candy', 0.01, quantity=1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestOrderCalculatorApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_twenty_percent(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_zero_no_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_subtotal_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

class TestOrderCalculatorCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_shipping_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

class TestOrderCalculatorCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_calculate_tax_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

class TestOrderCalculatorCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_total_full_calculation(self):
        self.calc.add_item('Item', 50.0, quantity=2)
        result = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(result, 123.0)

    def test_calculate_total_no_discount_default(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_qualifies_for_free_shipping(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(result, 123.0)

    def test_calculate_total_not_qualifies_for_free_shipping(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_tax_on_discounted_plus_shipping(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=0.5)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_zero_discount(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(result, 123.0)

    def test_calculate_total_full_discount(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_greater_than_one_raises_value_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_discount_string_raises_type_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.2')

class TestOrderCalculatorTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_sum_quantities(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, quantity=10)
        self.assertEqual(self.calc.total_items(), 10)

    def test_total_items_multiple_items_various_quantities(self):
        self.calc.add_item('Apple', 1.5, quantity=1)
        self.calc.add_item('Banana', 2.0, quantity=5)
        self.calc.add_item('Cherry', 3.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 9)

    def test_total_items_empty_order_returns_zero(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_after_adding_same_item_twice(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

class TestOrderCalculatorClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_non_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_total_items_zero(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestOrderCalculatorListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_returns_item_names(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        result = self.calc.list_items()
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertEqual(len(result), 2)

    def test_list_items_empty_order_returns_empty_list(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_same_item_added_twice_no_duplicates(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.list_items(), ['Apple'])

class TestOrderCalculatorIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order_returns_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_order_with_items_returns_false(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear_order_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_removing_last_item_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestOrderCalculatorIntegration(unittest.TestCase):

    def test_integration_full_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 500.0, quantity=1)
        calc.add_item('Mouse', 25.0, quantity=2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 550.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 495.0)
        total = calc.calculate_total(discount=0.1)
        expected = 495.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_integration_add_remove_add_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        calc.add_item('Banana', 2.0)
        self.assertEqual(calc.list_items(), ['Banana'])
        self.assertFalse(calc.is_empty())

    def test_integration_float_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Item1', 0.1, quantity=3)
        calc.add_item('Item2', 0.2, quantity=3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.9, places=5)