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

    def test_tax_rate_at_lower_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_tax_rate_at_upper_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_tax_rate_mid_range(self):
        calc = OrderCalculator(tax_rate=0.5)
        self.assertEqual(calc.tax_rate, 0.5)

    def test_free_shipping_threshold_at_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_shipping_cost_at_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_integer_values_for_float_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_large_valid_values(self):
        calc = OrderCalculator(tax_rate=0.99, free_shipping_threshold=10000.0, shipping_cost=500.0)
        self.assertEqual(calc.tax_rate, 0.99)
        self.assertEqual(calc.free_shipping_threshold, 10000.0)
        self.assertEqual(calc.shipping_cost, 500.0)

    def test_tax_rate_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_tax_rate_slightly_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.001)

    def test_tax_rate_slightly_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.001)

    def test_tax_rate_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_tax_rate_as_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_tax_rate_as_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=[0.23])

    def test_free_shipping_threshold_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_free_shipping_threshold_as_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_shipping_cost_as_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_shipping_cost_as_none_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_all_parameters_as_wrong_types_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23', free_shipping_threshold='100', shipping_cost='10')

    def test_empty_items_list_on_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.items, [])

class TestItemManagement(unittest.TestCase):

    def test_add_single_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_single_item_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, 5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Cherry', 3.0, 1)
        self.assertEqual(len(calc.items), 3)

    def test_add_same_item_twice_accumulates_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_with_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 10.0, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_with_quantity_exactly_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 5.0, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_very_high_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 99999.99, 1)
        self.assertEqual(calc.items[0]['price'], 99999.99)

    def test_add_item_with_minimal_valid_price(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_multiple_items_then_add_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Apple', 1.5, 1)
        apple_item = [item for item in calc.items if item['name'] == 'Apple'][0]
        self.assertEqual(apple_item['quantity'], 3)

    def test_empty_item_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_price_of_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0, 1)

    def test_negative_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -1.5, 1)

    def test_quantity_of_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 1.5, 0)

    def test_negative_quantity_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 1.5, -1)

    def test_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_name_as_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_name_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(None, 1.5, 1)

    def test_name_as_list_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(['Item'], 1.5, 1)

    def test_price_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '1.5', 1)

    def test_price_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', None, 1)

    def test_quantity_as_float_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.5, 1.5)

    def test_quantity_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.5, '1')

    def test_quantity_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.5, None)

    def test_remove_existing_item_from_single_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_existing_item_from_multi_item_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_leaves_other_items_intact(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Cherry', 3.0, 1)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        names = [item['name'] for item in calc.items]
        self.assertIn('Apple', names)
        self.assertIn('Cherry', names)
        self.assertNotIn('Banana', names)

    def test_remove_item_that_was_added_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_non_existent_item_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_with_similar_but_not_exact_name_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('apple')

    def test_remove_item_name_as_integer_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_name_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_name_as_empty_string_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

class TestCalculations(unittest.TestCase):

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_items_with_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 1.99, 1)
        calc.add_item('Item2', 2.49, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 6.97, places=2)

    def test_get_subtotal_large_order(self):
        calc = OrderCalculator()
        for i in range(10):
            calc.add_item(f'Item{i}', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 200.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_on_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_at_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_small_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_apply_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_slightly_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.001)

    def test_apply_discount_slightly_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.001)

    def test_apply_discount_subtotal_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100.0', 0.2)

    def test_apply_discount_subtotal_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(None, 0.2)

    def test_apply_discount_discount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_discount_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold_exactly(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_very_large_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(10000.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_subtotal_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100.0')

    def test_calculate_shipping_subtotal_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping(None)

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(10000.0)
        self.assertEqual(result, 2300.0)

    def test_calculate_tax_small_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_tax_amount_with_many_decimal_places(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(10.123456)
        self.assertAlmostEqual(result, 2.328395, places=6)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_amount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100.0')

    def test_calculate_tax_amount_as_none_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

class TestTotalCalculation(unittest.TestCase):

    def test_single_item_no_discount_shipping_charged(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_single_item_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 1)
        calc.add_item('Item2', 60.0, 1)
        total = calc.calculate_total(0.0)
        expected = (110.0 + 0.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_single_item_with_discount_shipping_charged(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 80.0
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_single_item_with_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 120.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_full_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(1.0)
        expected = (0.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_brings_order_below_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 120.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_calculated_on_discounted_subtotal_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        base = 50.0 + 10.0
        tax = base * 0.1
        expected = base + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_tax_rate_scenario(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        expected = 50.0 + 10.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        base = 50.0 + 10.0
        expected = base * 2.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_exactly_at_free_shipping_threshold_after_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 100.0
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_very_large_order(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 1000.0, 10)
        total = calc.calculate_total(0.0)
        expected = 10000.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_items_with_complex_discount(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 40.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 100.0
        discounted = 90.0
        expected = (discounted + 10.0) * 1.15
        self.assertAlmostEqual(total, expected, places=2)

    def test_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_invalid_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_invalid_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_discount_as_string_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.2')

    def test_discount_as_none_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(None)

class TestUtilityMethods(unittest.TestCase):

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_with_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        calc.add_item('Item3', 30.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_adding_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 2)
        calc.add_item('Item', 10.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 20.0, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_then_verify_is_empty_returns_true(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_then_verify_total_items_returns_zero(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 20.0, 1)
        calc.add_item('Cherry', 30.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_same_item_added_twice_appears_once(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Apple', 10.0, 3)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_return_type_is_list(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertIsInstance(calc.list_items(), list)

    def test_list_items_order_contains_all_expected_names(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 1)
        calc.add_item('B', 20.0, 1)
        calc.add_item('C', 30.0, 1)
        items = calc.list_items()
        self.assertEqual(set(items), {'A', 'B', 'C'})

    def test_is_empty_new_instance(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_one_item(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_adding_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_then_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

class TestIntegrationAndEdgeCases(unittest.TestCase):

    def test_add_calculate_total_add_more_recalculate(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 1)
        total1 = calc.calculate_total(0.0)
        calc.add_item('Item2', 60.0, 1)
        total2 = calc.calculate_total(0.0)
        self.assertNotEqual(total1, total2)
        self.assertGreater(total2, total1)

    def test_add_item_remove_it_verify_empty(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        calc.remove_item('Item')
        self.assertTrue(calc.is_empty())

    def test_add_multiple_clear_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 20.0, 1)
        calc.clear_order()
        calc.add_item('Item3', 30.0, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Item3')

    def test_calculate_subtotal_multiple_times(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 2)
        subtotal1 = calc.get_subtotal()
        subtotal2 = calc.get_subtotal()
        self.assertEqual(subtotal1, subtotal2)

    def test_order_value_exactly_at_free_shipping_threshold_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(0.0)
        expected = 100.0 * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_value_just_below_vs_at_threshold(self):
        calc1 = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc1.add_item('Item', 99.99, 1)
        total1 = calc1.calculate_total(0.0)
        calc2 = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc2.add_item('Item', 100.0, 1)
        total2 = calc2.calculate_total(0.0)
        self.assertGreater(total1, total2)

    def test_maximum_float_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=1000000.0, shipping_cost=100.0)
        calc.add_item('Item', 999999.99, 1)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_minimum_positive_float_values(self):
        calc = OrderCalculator(tax_rate=0.01, free_shipping_threshold=1.0, shipping_cost=0.1)
        calc.add_item('Item', 0.01, 1)
        total = calc.calculate_total(0.0)
        self.assertGreater(total, 0)

    def test_multi_item_order_with_discount_crossing_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 60.0, 1)
        calc.add_item('Item2', 60.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 96.0
        expected = (discounted + 10.0) * 1.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_ten_different_items_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=100.0, shipping_cost=10.0)
        for i in range(10):
            calc.add_item(f'Item{i}', 10.0, 1)
        total = calc.calculate_total(0.1)
        subtotal = 100.0
        discounted = 90.0
        expected = (discounted + 10.0) * 1.15
        self.assertAlmostEqual(total, expected, places=2)

    def test_verify_tax_calculation_order(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(0.2)
        discounted = 80.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.1
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_tax_zero_shipping_cost_configuration(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 50.0)

    def test_maximum_tax_high_shipping_cost_configuration(self):
        calc = OrderCalculator(tax_rate=1.0, free_shipping_threshold=1000.0, shipping_cost=50.0)
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total(0.0)
        base = 100.0 + 50.0
        expected = base * 2.0
        self.assertAlmostEqual(total, expected, places=2)

    def test_verify_subtotal_precision_with_repeating_decimals(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0 / 3, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 10.0, places=2)

    def test_verify_discount_precision(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0 / 3)
        expected = 100.0 * (2.0 / 3)
        self.assertAlmostEqual(result, expected, places=2)

    def test_verify_tax_precision(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_verify_total_precision_with_all_components(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 99.99, 1)
        total = calc.calculate_total(0.15)
        discounted = 84.9915
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_verify_items_list_not_modified_by_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 2)
        items_before = calc.items.copy()
        calc.get_subtotal()
        calc.calculate_total(0.1)
        self.assertEqual(calc.items, items_before)

    def test_verify_configuration_parameters_not_modified(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        calc.calculate_total(0.2)
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_multiple_calculate_total_calls_dont_modify_state(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.1)
        self.assertEqual(total1, total2)

    def test_failed_add_item_doesnt_modify_order(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        try:
            calc.add_item('Item', 20.0, 1)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['price'], 10.0)

    def test_failed_remove_item_doesnt_modify_order(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        try:
            calc.remove_item('Item2')
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Item1')