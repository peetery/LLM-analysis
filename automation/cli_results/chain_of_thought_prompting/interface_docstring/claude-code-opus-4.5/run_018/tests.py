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

    def test_init_tax_rate_zero_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one_boundary(self):
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

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_with_explicit_quantity(self):
        self.calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_add_same_item_twice_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_minimum_valid_price(self):
        self.calc.add_item('Cheap', 0.01)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_add_item_quantity_one_minimum(self):
        self.calc.add_item('Item', 10.0, quantity=1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_very_large_quantity(self):
        self.calc.add_item('Bulk', 1.0, quantity=1000000)
        self.assertEqual(self.calc.total_items(), 1000000)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_price_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -5.0)

    def test_add_item_quantity_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, quantity=0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 10.0, quantity=-1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_name_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_price_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0')

    def test_add_item_quantity_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, quantity=2.5)

    def test_add_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 10.0)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item_successfully(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_verify_not_in_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())
        self.assertIn('Banana', self.calc.list_items())

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

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 2.5, quantity=4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 2.0, quantity=3)
        self.calc.add_item('Banana', 1.5, quantity=2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 9.0)

    def test_get_subtotal_item_quantity_greater_than_one(self):
        self.calc.add_item('Item', 5.0, quantity=10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_get_subtotal_minimum_price_quantity(self):
        self.calc.add_item('Cheap', 0.01, quantity=1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_zero_percent(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_twenty_percent(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_boundary_zero(self):
        result = self.calc.apply_discount(50.0, 0.0)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_discount_boundary_one(self):
        result = self.calc.apply_discount(50.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_subtotal_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_subtotal_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(None, 0.1)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_shipping_zero_threshold_always_free(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_shipping_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 10.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 100.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_string_amount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_total_without_discount(self):
        self.calc.add_item('Item', 50.0, quantity=1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_with_twenty_percent_discount(self):
        self.calc.add_item('Item', 100.0, quantity=1)
        result = self.calc.calculate_total(discount=0.2)
        expected = (80.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_qualifying_for_free_shipping(self):
        self.calc.add_item('Item', 120.0, quantity=1)
        result = self.calc.calculate_total()
        expected = 120.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_not_qualifying_for_free_shipping(self):
        self.calc.add_item('Item', 50.0, quantity=1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_verify_formula(self):
        self.calc.add_item('Item', 200.0, quantity=1)
        result = self.calc.calculate_total(discount=0.1)
        discounted = 200.0 * 0.9
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_discount_zero_boundary(self):
        self.calc.add_item('Item', 50.0, quantity=1)
        result = self.calc.calculate_total(discount=0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_discount_one_boundary(self):
        self.calc.add_item('Item', 50.0, quantity=1)
        result = self.calc.calculate_total(discount=1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_exactly_at_threshold(self):
        self.calc.add_item('Item', 100.0, quantity=1)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_below_threshold_after_discount(self):
        self.calc.add_item('Item', 110.0, quantity=1)
        result = self.calc.calculate_total(discount=0.2)
        discounted = 110.0 * 0.8
        shipping = 10.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_greater_than_one_raises_value_error(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_non_numeric_discount_raises_type_error(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_same_item_added_twice(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_after_removing_item(self):
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.calc.add_item('Banana', 2.0, quantity=2)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 2)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_is_empty_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_total_items_returns_zero(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_already_empty_idempotent(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_returns_all_names(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_list_items_same_item_added_twice_unique(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        items = self.calc.list_items()
        self.assertEqual(items.count('Apple'), 1)

    def test_list_items_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_after_remove_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        items = self.calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_empty_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_order_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestIntegrationWorkflows(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_workflow_add_discount_calculate_total(self):
        self.calc.add_item('Item1', 50.0, quantity=2)
        self.calc.add_item('Item2', 30.0, quantity=1)
        subtotal = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 130.0)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 130.0 * 0.9
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_workflow_add_remove_verify_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_workflow_add_clear_add_new_verify_state(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Orange', self.calc.list_items())

    def test_workflow_full_order_lifecycle(self):
        self.calc.add_item('Apple', 2.0, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)
        self.calc.add_item('Apple', 2.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 8)
        self.calc.add_item('Banana', 1.5, quantity=4)
        self.assertEqual(self.calc.total_items(), 12)
        subtotal = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 22.0)
        self.calc.remove_item('Banana')
        self.assertEqual(self.calc.total_items(), 8)
        total = self.calc.calculate_total(discount=0.0)
        expected = (16.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)