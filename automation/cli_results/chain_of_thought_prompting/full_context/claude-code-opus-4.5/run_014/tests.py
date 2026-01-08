import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_items_list_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

    def test_init_tax_rate_zero_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_free_shipping_threshold_zero_boundary(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_free_shipping_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_zero_boundary(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_shipping_cost_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_integer_values_accepted(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.assertEqual(len(self.calc.items), 2)

    def test_add_item_same_name_same_price_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_price_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)

    def test_add_item_price_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_quantity_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_quantity_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_name_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.5)

    def test_add_item_price_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.50')

    def test_add_item_quantity_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_quantity_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, '2')

    def test_add_item_integer_price_accepted(self):
        self.calc.add_item('Apple', 2)
        self.assertEqual(self.calc.items[0]['price'], 2)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_verify_removal(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.remove_item('Apple')
        names = [item['name'] for item in self.calc.items]
        self.assertNotIn('Apple', names)
        self.assertIn('Banana', names)

    def test_remove_item_nonexistent_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_name_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_item_others_remain(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.add_item('Orange', 2.0)
        self.calc.remove_item('Banana')
        self.assertEqual(len(self.calc.items), 2)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_get_subtotal_calculation_verification(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 3)
        expected = 10.0 * 2 + 5.0 * 3
        self.assertEqual(self.calc.get_subtotal(), expected)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_zero_percent(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_typical(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_lower_boundary(self):
        result = self.calc.apply_discount(50.0, 0.0)
        self.assertEqual(result, 50.0)

    def test_apply_discount_upper_boundary(self):
        result = self.calc.apply_discount(50.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_subtotal_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_integer_values_accepted(self):
        result = self.calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_shipping_custom_threshold_and_cost(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.0), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_integer_amount_accepted(self):
        result = self.calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_total_no_discount_shipping_applies(self):
        self.calc.add_item('Item', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_no_discount_free_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_shipping_applies(self):
        self.calc.add_item('Item', 80.0, 1)
        result = self.calc.calculate_total(0.5)
        discounted = 40.0
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_discount_achieves_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        result = self.calc.calculate_total(0.4)
        discounted = 120.0
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        result = self.calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_greater_than_one(self):
        self.calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.1)

    def test_calculate_total_invalid_discount_negative(self):
        self.calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_discount_string_raises_type_error(self):
        self.calc.add_item('Item', 100.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_calculate_total_formula_verification(self):
        self.calc.add_item('Item', 80.0, 1)
        result = self.calc.calculate_total(0.1)
        discounted_subtotal = 80.0 * 0.9
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_default_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertEqual(self.calc.total_items(), 6)

    def test_total_items_after_adding_same_item_twice(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_non_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_empty(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_is_empty_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_total_items_returns_zero(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        result = self.calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_list_items_no_duplicates(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Apple', 1.5, 2)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'Apple')

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_full_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 130.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 117.0)
        total = calc.calculate_total(0.1)
        expected = 117.0 * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_add_calculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        calc.remove_item('Apple')
        calc.add_item('Banana', 50.0, 2)
        total = calc.calculate_total()
        expected = (100.0 + 0.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_applied_to_discounted_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=20.0)
        calc.add_item('Item', 80.0, 1)
        total = calc.calculate_total(0.0)
        discounted_subtotal = 80.0
        shipping = 20.0
        tax = (discounted_subtotal + shipping) * 0.1
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_values(self):
        calc = OrderCalculator()
        calc.add_item('ExpensiveItem', 10000.0, 1000)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 10000000.0)
        total = calc.calculate_total()
        expected = 10000000.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.07)
        calc.add_item('Item', 0.1, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_multiple_operations_workflow(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0)
        calc.remove_item('A')
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        calc.add_item('C', 150.0)
        total = calc.calculate_total(0.2)
        discounted = 150.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)