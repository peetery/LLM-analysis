import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=25.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 25.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0)
        self.assertEqual(calc.free_shipping_threshold, 0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0)
        self.assertEqual(calc.shipping_cost, 0)

    def test_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_negative_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_single_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_add_duplicate_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_with_float_price(self):
        self.calc.add_item('Item', 19.99)
        self.assertAlmostEqual(self.calc.get_subtotal(), 19.99, places=2)

    def test_add_item_with_large_quantity(self):
        self.calc.add_item('Bulk', 1.0, 1000)
        self.assertEqual(self.calc.total_items(), 1000)

    def test_add_item_with_very_small_price(self):
        self.calc.add_item('Penny', 0.01)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.01, places=2)

    def test_empty_item_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free', 0)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', -5.0)

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.5, 0)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.5, -1)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_from_multi_item_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())
        self.assertIn('Banana', self.calc.list_items())

    def test_remove_last_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_case_sensitivity(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('apple')

    def test_remove_item_twice(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_empty_string_name(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_single_item_subtotal(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.5, places=2)

    def test_multiple_items_subtotal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 9.0, places=2)

    def test_subtotal_with_various_quantities(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 5.0, 4)
        self.calc.add_item('C', 2.5, 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 55.0, places=2)

    def test_floating_point_precision(self):
        self.calc.add_item('A', 0.1, 1)
        self.calc.add_item('B', 0.2, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3, places=2)

    def test_large_subtotal(self):
        self.calc.add_item('Expensive', 1000.0, 100)
        self.assertAlmostEqual(self.calc.get_subtotal(), 100000.0, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_0_percent_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_discount_over_100_percent(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 150.0)

    def test_negative_subtotal_parameter(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 10.0)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_just_above_threshold(self):
        result = self.calc.calculate_shipping(100.01)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_custom_threshold_verification(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertAlmostEqual(result, 0.0, places=2)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_on_zero(self):
        result = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_tax_with_default_rate(self):
        result = self.calc.calculate_tax(50.0)
        self.assertAlmostEqual(result, 11.5, places=2)

    def test_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 10.0, places=2)

    def test_tax_precision(self):
        result = self.calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_tax_on_small_amount(self):
        result = self.calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_tax_on_large_amount(self):
        result = self.calc.calculate_tax(10000.0)
        self.assertAlmostEqual(result, 2300.0, places=2)

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_with_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_at_free_shipping_threshold(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_default_discount_parameter(self):
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_negative_discount_to_calculate_total(self):
        self.calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-10.0)

    def test_discount_over_100_to_calculate_total(self):
        self.calc.add_item('Item', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(150.0)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_single_item_count(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_single_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_multiple_items_count(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_empty_order_count(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_after_adding_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_after_removing_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_populated_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_already_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_single_item(self):
        self.calc.add_item('Apple', 1.5)
        items = self.calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_after_removal(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        items = self.calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_new_order_is_empty(self):
        self.assertTrue(self.calc.is_empty())

    def test_non_empty_order(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_after_add_then_remove(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_equals_threshold_exactly(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 100.0)
        shipping = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0, places=2)

    def test_order_state_consistency(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 4)
        self.assertEqual(self.calc.total_items(), 6)
        self.assertAlmostEqual(self.calc.get_subtotal(), 40.0, places=2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_recalculation_after_modification(self):
        self.calc.add_item('Item', 50.0, 1)
        total1 = self.calc.calculate_total()
        self.calc.add_item('Item2', 100.0, 1)
        total2 = self.calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_boundary_value_analysis_99_99(self):
        self.calc.add_item('Item', 99.99, 1)
        shipping = self.calc.calculate_shipping(self.calc.get_subtotal())
        self.assertAlmostEqual(shipping, 10.0, places=2)

    def test_boundary_value_analysis_100_00(self):
        self.calc.add_item('Item', 100.0, 1)
        shipping = self.calc.calculate_shipping(self.calc.get_subtotal())
        self.assertAlmostEqual(shipping, 0.0, places=2)

    def test_boundary_value_analysis_100_01(self):
        self.calc.add_item('Item', 100.01, 1)
        shipping = self.calc.calculate_shipping(self.calc.get_subtotal())
        self.assertAlmostEqual(shipping, 0.0, places=2)