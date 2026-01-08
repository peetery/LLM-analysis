import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

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

    def test_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_tax_rate_wrong_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_tax_rate_wrong_type_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_free_shipping_threshold_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_shipping_cost_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_explicit_quantity(self):
        self.calc.add_item('Banana', 2.0, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_same_price(self):
        self.calc.add_item('Orange', 3.0, 2)
        self.calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.items), 3)

    def test_add_item_with_float_price(self):
        self.calc.add_item('Grape', 19.99)
        self.assertEqual(self.calc.items[0]['price'], 19.99)

    def test_add_item_with_integer_price(self):
        self.calc.add_item('Watermelon', 5)
        self.assertEqual(self.calc.items[0]['price'], 5)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_name_wrong_type_none(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.0)

    def test_name_wrong_type_integer(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_price_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 0)

    def test_price_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -1.0)

    def test_price_wrong_type_string(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10')

    def test_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, 0)

    def test_quantity_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, -1)

    def test_quantity_wrong_type_float(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 1.0, 1.5)

    def test_quantity_wrong_type_string(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 1.0, '1')

    def test_same_name_different_price_conflict(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 20.0)

    def test_same_name_same_price_multiple_additions(self):
        self.calc.add_item('Item', 10.0, 2)
        self.calc.add_item('Item', 10.0, 3)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_one_of_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.calc.remove_item('Banana')
        self.assertEqual(len(self.calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in self.calc.items])

    def test_remove_non_existent_item(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Item')

    def test_name_wrong_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_remove_item_added_multiple_times(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(self.calc.get_subtotal(), 6.5)

    def test_subtotal_with_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_empty_order_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_subtotal_after_adding_and_removing(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.get_subtotal(), 2.0)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_no_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_partial_discount(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_full_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_discount_on_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_integer_discount(self):
        result = self.calc.apply_discount(100.0, 0)
        self.assertEqual(result, 100.0)

    def test_discount_below_zero(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_discount_above_one(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_subtotal_wrong_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_discount_wrong_type(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_at_threshold_exactly(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_zero_discounted_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_discounted_subtotal_wrong_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_tax_on_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_integer_amount(self):
        result = self.calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_amount_wrong_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_no_discount_below_shipping_threshold(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_no_discount_above_shipping_threshold(self):
        self.calc.add_item('Item', 150.0)
        total = self.calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_below_threshold(self):
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total(discount=0.5)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_discount_above_threshold(self):
        self.calc.add_item('Item', 200.0)
        total = self.calc.calculate_total(discount=0.2)
        expected = 160.0 + 0.0 + 160.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_default_discount_parameter(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_discount_bringing_total_below_threshold(self):
        self.calc.add_item('Item', 150.0)
        total = self.calc.calculate_total(discount=0.5)
        expected = 75.0 + 10.0 + 85.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_empty_order_total(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_invalid_discount_in_calculate_total(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_discount_wrong_type_in_calculate_total(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_with_exact_threshold_boundary(self):
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total()
        expected = 100.0 + 0.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_verify_tax_calculation_order(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

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
        self.calc.add_item('Orange', 3.0, 1)
        self.assertEqual(self.calc.total_items(), 6)

    def test_after_adding_and_removing_items(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_non_empty_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_already_empty_order(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_verify_state_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_single_item(self):
        self.calc.add_item('Apple', 1.5)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('Apple', result)

    def test_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        result = self.calc.list_items()
        self.assertEqual(len(result), 3)
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertIn('Orange', result)

    def test_no_duplicates_in_list(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertEqual(result.count('Apple'), 1)

    def test_after_removing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        result = self.calc.list_items()
        self.assertNotIn('Apple', result)
        self.assertIn('Banana', result)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_initially_empty(self):
        self.assertTrue(self.calc.is_empty())

    def test_not_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_empty_after_clearing(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_empty_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestIntegrationScenarios(unittest.TestCase):

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 1.5, 10)
        calc.add_item('Banana', 2.0, 5)
        calc.add_item('Orange', 3.0, 3)
        total = calc.calculate_total(discount=0.1)
        subtotal = 1.5 * 10 + 2.0 * 5 + 3.0 * 3
        discounted = subtotal * 0.9
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_persistence(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        first_subtotal = calc.get_subtotal()
        calc.add_item('Banana', 2.0, 3)
        second_subtotal = calc.get_subtotal()
        self.assertEqual(first_subtotal, 3.0)
        self.assertEqual(second_subtotal, 9.0)

    def test_float_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 0.1, 1)
        calc.add_item('Item2', 0.2, 1)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.0, 1000000)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 1000000.0)

    def test_many_items(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0)
        self.assertEqual(len(calc.items), 100)
        self.assertEqual(calc.total_items(), 100)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_complex_discount_scenario(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 111.11)
        total = calc.calculate_total(discount=0.1)
        discounted = 111.11 * 0.9
        self.assertAlmostEqual(discounted, 100.0, places=1)
        shipping = 0.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)