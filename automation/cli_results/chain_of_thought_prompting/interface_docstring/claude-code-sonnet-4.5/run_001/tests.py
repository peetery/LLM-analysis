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

    def test_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_non_numeric_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_single_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 1.0)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_same_item_accumulates_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_very_small_price(self):
        self.calc.add_item('Penny', 0.01)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01)

    def test_add_item_large_quantity(self):
        self.calc.add_item('Bulk Item', 10.0, 1000)
        self.assertEqual(self.calc.total_items(), 1000)

    def test_empty_string_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_whitespace_only_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('   ', 1.5)

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free Item', 0.0)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', -5.0)

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_same_name_different_price(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_non_string_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_non_numeric_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5')

    def test_non_integer_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 2.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_from_multi_item_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.list_items(), ['Banana'])

    def test_remove_all_items_one_by_one(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.calc.remove_item('Banana')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_already_removed_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_non_string_name(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 9.0)

    def test_subtotal_varying_quantities(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 5)
        self.calc.add_item('Orange', 3.0, 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 41.0)

    def test_subtotal_accumulated_quantities(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.5)

    def test_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_subtotal_very_small_prices(self):
        self.calc.add_item('Penny', 0.01, 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.1, places=2)

    def test_subtotal_large_quantities(self):
        self.calc.add_item('Bulk', 10.0, 1000)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10000.0)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_twenty_percent_discount(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_fifty_percent_discount(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertAlmostEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_discount_below_zero(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_non_numeric_subtotal(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_non_numeric_discount(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_very_small_discount(self):
        result = self.calc.apply_discount(100.0, 0.001)
        self.assertAlmostEqual(result, 99.9)

    def test_discount_very_close_to_one(self):
        result = self.calc.apply_discount(100.0, 0.999)
        self.assertAlmostEqual(result, 0.1, places=1)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_at_threshold_exactly(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_zero_discounted_subtotal(self):
        shipping = self.calc.calculate_shipping(0.0)
        self.assertAlmostEqual(shipping, 10.0)

    def test_very_large_discounted_subtotal(self):
        shipping = self.calc.calculate_shipping(10000.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_non_numeric_input(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_just_below_threshold(self):
        shipping = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_just_above_threshold(self):
        shipping = self.calc.calculate_shipping(100.01)
        self.assertAlmostEqual(shipping, 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_tax_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_different_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 15.0)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_non_numeric_amount(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_very_small_amount(self):
        tax = self.calc.calculate_tax(0.01)
        self.assertAlmostEqual(tax, 0.0023)

    def test_large_amount(self):
        tax = self.calc.calculate_tax(10000.0)
        self.assertAlmostEqual(tax, 2300.0)

    def test_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 100.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_no_discount_below_threshold(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_no_discount_above_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 2)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 100.0 * 0.9
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_with_discount_above_threshold(self):
        self.calc.add_item('Apple', 60.0, 2)
        total = self.calc.calculate_total(discount=0.05)
        discounted = 120.0 * 0.95
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_zero_discount_default(self):
        self.calc.add_item('Apple', 50.0, 3)
        total1 = self.calc.calculate_total()
        total2 = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total1, total2)

    def test_total_hundred_percent_discount(self):
        self.calc.add_item('Apple', 50.0, 2)
        total = self.calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected)

    def test_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_invalid_discount_negative(self):
        self.calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_total_invalid_discount_above_one(self):
        self.calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.1)

    def test_total_non_numeric_discount(self):
        self.calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_discount_brings_to_threshold_exactly(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total(discount=0.333333)
        discounted = 150.0 * (1 - 0.333333)
        if discounted >= 100.0:
            expected = discounted * 1.23
        else:
            expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=1)

    def test_discount_brings_just_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total(discount=0.34)
        discounted = 150.0 * 0.66
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_discount_brings_just_above_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total(discount=0.32)
        discounted = 150.0 * 0.68
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected)

    def test_subtotal_at_threshold_before_discount(self):
        self.calc.add_item('Apple', 100.0)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 100.0 * 0.9
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

    def test_multiple_items_with_discount_and_shipping(self):
        self.calc.add_item('Apple', 20.0, 2)
        self.calc.add_item('Banana', 15.0, 2)
        total = self.calc.calculate_total(discount=0.2)
        subtotal = 70.0
        discounted = subtotal * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_accumulated_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_after_removing_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

    def test_large_quantities(self):
        self.calc.add_item('Bulk1', 1.0, 500)
        self.calc.add_item('Bulk2', 2.0, 500)
        self.assertEqual(self.calc.total_items(), 1000)

    def test_after_clear_order(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_non_empty_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_then_add_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_clear_multiple_times(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_total_items_after_clear(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertEqual(self.calc.list_items(), [])

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        items = self.calc.list_items()
        self.assertEqual(sorted(items), sorted(['Apple', 'Banana', 'Orange']))

    def test_no_duplicates(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_after_removing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.list_items(), ['Banana'])

    def test_items_with_similar_names(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Apple Juice', 3.0)
        items = self.calc.list_items()
        self.assertEqual(sorted(items), sorted(['Apple', 'Apple Juice']))

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_after_adding_items(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_after_clearing_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.calc.remove_item('Banana')
        self.assertTrue(self.calc.is_empty())

    def test_after_adding_then_removing_same_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_complex_workflow(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.calc.add_item('Banana', 5.0, 4)
        total1 = self.calc.calculate_total()
        self.calc.remove_item('Apple')
        total2 = self.calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_add_clear_add_different(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.list_items(), ['Banana'])

    def test_multiple_discount_calculations(self):
        result1 = self.calc.apply_discount(100.0, 0.2)
        result2 = self.calc.apply_discount(100.0, 0.3)
        self.assertNotEqual(result1, result2)

    def test_subtotal_unchanged_after_discount(self):
        self.calc.add_item('Apple', 10.0, 5)
        subtotal1 = self.calc.get_subtotal()
        self.calc.calculate_total(discount=0.5)
        subtotal2 = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal1, subtotal2)

    def test_build_calculate_clear_build_new(self):
        self.calc.add_item('Apple', 10.0, 2)
        total1 = self.calc.calculate_total()
        self.calc.clear_order()
        self.calc.add_item('Banana', 5.0, 4)
        total2 = self.calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_add_items_crossing_threshold(self):
        self.calc.add_item('Apple', 30.0, 3)
        shipping1 = self.calc.calculate_shipping(self.calc.get_subtotal())
        self.calc.add_item('Banana', 5.0, 2)
        shipping2 = self.calc.calculate_shipping(self.calc.get_subtotal())
        self.assertNotEqual(shipping1, shipping2)

    def test_discount_crossing_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total_no_discount = self.calc.calculate_total(discount=0.0)
        total_with_discount = self.calc.calculate_total(discount=0.5)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_item_quantities_consistent(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.calc.calculate_total()
        self.assertEqual(self.calc.total_items(), 8)

    def test_price_conflicts_detected(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_removed_items_dont_affect_calculations(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.calc.add_item('Banana', 5.0, 2)
        self.calc.remove_item('Banana')
        subtotal = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 50.0)

class TestFloatingPointPrecision(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_floating_point_addition(self):
        self.calc.add_item('Item1', 0.1, 1)
        self.calc.add_item('Item2', 0.2, 1)
        subtotal = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=2)

    def test_tax_calculation_precision(self):
        tax = self.calc.calculate_tax(10.123456789)
        expected = 10.123456789 * 0.23
        self.assertAlmostEqual(tax, expected, places=5)

    def test_discount_calculation_precision(self):
        result = self.calc.apply_discount(33.33, 0.333)
        expected = 33.33 * (1 - 0.333)
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_calculation_precision(self):
        self.calc.add_item('Item', 9.99, 3)
        total = self.calc.calculate_total(discount=0.15)
        subtotal = 29.97
        discounted = subtotal * 0.85
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)