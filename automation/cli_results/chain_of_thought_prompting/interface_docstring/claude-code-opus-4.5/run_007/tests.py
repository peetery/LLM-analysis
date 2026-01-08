import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
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
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_tax_rate_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

class TestOrderCalculatorAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_add_same_item_twice_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_quantity_one_explicitly(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_very_small_price(self):
        self.calc.add_item('Penny Item', 0.01)
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
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

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
            self.calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.5)

class TestOrderCalculatorRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_verify_not_in_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_nonexistent_item_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_name_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

class TestOrderCalculatorGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.0)

    def test_get_subtotal_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)

    def test_get_subtotal_small_price_quantity_one(self):
        self.calc.add_item('Penny', 0.01, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestOrderCalculatorApplyDiscount(unittest.TestCase):

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

    def test_apply_discount_subtotal_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(None, 0.2)

class TestOrderCalculatorCalculateShipping(unittest.TestCase):

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

    def test_calculate_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        result = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 0.0)

    def test_calculate_shipping_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_shipping_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

class TestOrderCalculatorCalculateTax(unittest.TestCase):

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

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Item', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_no_discount_above_threshold(self):
        self.calc.add_item('Item', 150.0, 1)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_with_discount_below_threshold(self):
        self.calc.add_item('Item', 80.0, 1)
        result = self.calc.calculate_total(0.5)
        expected = (40.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_with_discount_above_threshold(self):
        self.calc.add_item('Item', 200.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = 160.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_default_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_discount_crosses_threshold(self):
        self.calc.add_item('Item', 120.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = (96.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        self.calc.add_item('Item', 125.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_full_calculation(self):
        self.calc.add_item('Item1', 50.0, 2)
        self.calc.add_item('Item2', 25.0, 2)
        result = self.calc.calculate_total(0.1)
        subtotal = 150.0
        discounted = 135.0
        shipping = 0.0
        expected = (discounted + shipping) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_negative_discount_raises_value_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_discount_greater_than_one_raises_value_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_discount_string_raises_type_error(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

class TestOrderCalculatorTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_after_adding_same_item_twice(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestOrderCalculatorClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_non_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_already_empty(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_is_empty_returns_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_total_items_returns_zero(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_get_subtotal_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestOrderCalculatorListItems(unittest.TestCase):

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
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertEqual(len(result), 2)

    def test_list_items_no_duplicates(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        result = self.calc.list_items()
        self.assertEqual(result.count('Apple'), 1)

    def test_list_items_order_consistency(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.add_item('Cherry', 2.0)
        result = self.calc.list_items()
        self.assertEqual(len(result), 3)

class TestOrderCalculatorIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removing_only_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestOrderCalculatorIntegration(unittest.TestCase):

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Widget', 25.0, 4)
        calc.add_item('Gadget', 15.0, 2)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 130.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertAlmostEqual(discounted, 117.0)
        total = calc.calculate_total(0.1)
        expected = 117.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_add_remove_add_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Banana', 0.75, 3)
        self.assertEqual(calc.list_items(), ['Banana'])
        self.assertEqual(calc.total_items(), 3)

    def test_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        calc.add_item('Item1', 0.1, 10)
        calc.add_item('Item2', 0.2, 5)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 2.0, places=2)

    def test_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 10.0, 1)
        self.assertEqual(calc.total_items(), 100)
        self.assertAlmostEqual(calc.get_subtotal(), 1000.0)