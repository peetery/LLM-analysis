import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_float_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

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

    def test_init_items_list_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

    def test_init_tax_rate_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_free_shipping_threshold_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_tax_rate_negative_raises_value_error(self):
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

class TestOrderCalculatorAddItem(unittest.TestCase):

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
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(len(self.calc.items), 3)

    def test_add_same_item_quantity_accumulates(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_integer_price(self):
        self.calc.add_item('Apple', 2, 1)
        self.assertEqual(self.calc.items[0]['price'], 2)

    def test_add_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_price_just_above_zero(self):
        self.calc.add_item('Apple', 0.01)
        self.assertEqual(self.calc.items[0]['price'], 0.01)

    def test_add_item_name_not_string_raises_type_error(self):
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

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

class TestOrderCalculatorRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_verify_gone(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertFalse(any((item['name'] == 'Apple' for item in self.calc.items)))

    def test_remove_item_others_remain(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_name_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_remove_item_name_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_remove_nonexistent_item_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

class TestOrderCalculatorGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_multiple(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_get_subtotal_calculation_correct(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 3)
        expected = 10.0 * 2 + 5.0 * 3
        self.assertEqual(self.calc.get_subtotal(), expected)

    def test_get_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestOrderCalculatorApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_zero_percent(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_twenty_percent(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_fifty_percent(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_subtotal_zero(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_integer_inputs(self):
        result = self.calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_apply_discount_subtotal_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_apply_discount_subtotal_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(None, 0.2)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

class TestOrderCalculatorCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_threshold_zero_always_free(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

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
        self.assertEqual(result, 23.0)

    def test_calculate_tax_calculation_correct(self):
        result = self.calc.calculate_tax(50.0)
        self.assertEqual(result, 50.0 * 0.23)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

class TestOrderCalculatorCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_calculate_total_no_discount_below_threshold(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total(0.2)
        discounted = 50.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_free_shipping_no_discount(self):
        self.calc.add_item('Item', 150.0)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_free_shipping_with_discount(self):
        self.calc.add_item('Item', 200.0)
        result = self.calc.calculate_total(0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_full_calculation(self):
        self.calc.add_item('Item1', 30.0, 2)
        self.calc.add_item('Item2', 20.0, 1)
        subtotal = 80.0
        discounted = subtotal * 0.9
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        result = self.calc.calculate_total(0.1)
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_default_discount_zero(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_calculate_total_discount_string_raises_type_error(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

    def test_calculate_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_raises_value_error(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

class TestOrderCalculatorTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_item_quantity_multiple(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items_sum(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.calc.add_item('Orange', 2.0, 4)
        self.assertEqual(self.calc.total_items(), 9)

class TestOrderCalculatorClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_non_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_already_empty(self):
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
        self.calc.add_item('Orange', 2.0)
        result = self.calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana', 'Orange'})

    def test_list_items_no_duplicates(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        result = self.calc.list_items()
        self.assertEqual(result, ['Apple'])

class TestOrderCalculatorIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_true_for_empty_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false_for_non_empty_order(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_add_and_remove(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestOrderCalculatorIntegration(unittest.TestCase):

    def test_full_order_lifecycle(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item1', 20.0, 2)
        calc.add_item('Item2', 15.0, 1)
        self.assertEqual(calc.get_subtotal(), 55.0)
        self.assertEqual(calc.total_items(), 3)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 55.0 * 1.1, places=2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_add_remove_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.75, 2)
        self.assertEqual(calc.total_items(), 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)
        self.assertEqual(calc.list_items(), ['Banana'])

    def test_discount_brings_below_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0)
        self.assertEqual(calc.calculate_shipping(120.0), 0.0)
        discounted = calc.apply_discount(120.0, 0.2)
        self.assertEqual(discounted, 96.0)
        self.assertEqual(calc.calculate_shipping(discounted), 10.0)