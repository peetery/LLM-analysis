import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.tax_rate, 0.1)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_negative_tax_rate_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_single_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_explicit_quantity_greater_than_one(self):
        self.calc.add_item('Banana', 0.75, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_add_item_quantity_one_explicitly(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_very_large_quantity(self):
        self.calc.add_item('Bulk Item', 0.01, 1000000)
        self.assertEqual(self.calc.total_items(), 1000000)

    def test_add_item_very_large_price(self):
        self.calc.add_item('Expensive', 999999.99)
        self.assertAlmostEqual(self.calc.get_subtotal(), 999999.99, places=2)

    def test_add_item_price_many_decimal_places(self):
        self.calc.add_item('Precise', 1.23456789)
        self.assertGreater(self.calc.get_subtotal(), 0)

    def test_add_same_item_twice(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad', -1.0)

    def test_add_item_zero_price_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free', 0.0)

    def test_add_item_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad', 1.0, -1)

    def test_add_item_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('None', 1.0, 0)

    def test_add_item_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_add_item_none_name_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item(None, 1.0)

    def test_add_item_non_string_name_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item(123, 1.0)

    def test_add_item_non_numeric_price_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('Item', 'ten')

    def test_add_item_non_integer_quantity_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('Item', 1.0, 2.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_leaves_others_intact(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.remove_item('Apple')
        self.assertIn('Banana', self.calc.list_items())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_last_item_makes_order_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_non_existent_item_raises(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Apple')

    def test_remove_empty_string_name_raises(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('')

    def test_remove_none_name_raises(self):
        with self.assertRaises((ValueError, KeyError, TypeError)):
            self.calc.remove_item(None)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0, places=2)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.0, places=2)

    def test_get_subtotal_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 10.0, 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0, places=2)

    def test_get_subtotal_float_precision(self):
        self.calc.add_item('Item1', 0.1, 3)
        self.calc.add_item('Item2', 0.2, 3)
        subtotal = self.calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.9, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_zero_percent(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_apply_discount_negative_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_hundred_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_negative_subtotal_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 10.0)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        result = self.calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_very_large_subtotal(self):
        result = self.calc.calculate_shipping(1000000.0)
        self.assertEqual(result, 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_accuracy(self):
        result = self.calc.calculate_tax(50.0)
        self.assertAlmostEqual(result, 11.5, places=2)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_very_small_amount(self):
        result = self.calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_calculate_tax_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Apple', 50.0, 1)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_includes_shipping_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 1)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_above_threshold(self):
        self.calc.add_item('Expensive', 150.0, 1)
        total = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_includes_correct_tax(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total()
        subtotal_with_shipping = 100.0
        expected = subtotal_with_shipping * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount_raises(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_calculate_total_discount_over_hundred_raises(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=110.0)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_sum_across_multiple(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.calc.add_item('Orange', 2.0, 4)
        self.assertEqual(self.calc.total_items(), 9)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_makes_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.list_items()), 0)

    def test_clear_already_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_single(self):
        self.calc.add_item('Apple', 1.5)
        items = self.calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_multiple(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 0.75)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_independent_no_mutation(self):
        self.calc.add_item('Apple', 1.5)
        items = self.calc.list_items()
        items.append('Fake')
        self.assertEqual(len(self.calc.list_items()), 1)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removing_all(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_items_persist_after_calculate_total(self):
        self.calc.add_item('Apple', 10.0)
        self.calc.add_item('Banana', 20.0)
        self.calc.calculate_total()
        self.assertEqual(len(self.calc.list_items()), 2)