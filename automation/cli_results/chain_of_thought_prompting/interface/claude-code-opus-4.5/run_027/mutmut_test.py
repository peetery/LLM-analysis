import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc.tax_rate, 0.15)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_all_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_add_item_high_price(self):
        self.calc.add_item('Luxury Item', 10000.0)
        self.assertEqual(self.calc.get_subtotal(), 10000.0)

    def test_add_item_high_quantity(self):
        self.calc.add_item('Bulk Item', 1.0, 1000)
        self.assertEqual(self.calc.total_items(), 1000)

    def test_add_item_quantity_one_explicit(self):
        self.calc.add_item('Item', 5.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_very_small_price(self):
        self.calc.add_item('Penny Item', 0.01)
        self.assertEqual(self.calc.get_subtotal(), 0.01)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free Item', 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Item', -5.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Zero Qty', 5.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Qty', 5.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 5.0)

    def test_add_item_none_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item(None, 5.0)

    def test_add_item_non_string_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item(123, 5.0)

    def test_add_item_non_numeric_price(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('Item', 'five')

    def test_add_item_non_integer_quantity(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('Item', 5.0, 2.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_verify_gone(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_single_item_becomes_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_first_of_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_remove_last_of_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.calc.remove_item('Orange')
        self.assertNotIn('Orange', self.calc.list_items())

    def test_remove_non_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_case_sensitive(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('apple')

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_subtotal_single_item_quantity_multiple(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 4.5)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_subtotal_precision(self):
        self.calc.add_item('Item1', 0.1, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3, places=2)

    def test_subtotal_updates_after_adding(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.get_subtotal(), 3.5)

    def test_subtotal_updates_after_removing(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.get_subtotal(), 2.0)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_discount_zero_percent(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_100(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 10.0)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_shipping_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_shipping_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_shipping_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 15.0)

    def test_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_shipping_just_above_threshold(self):
        result = self.calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_default_rate(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_precision(self):
        result = self.calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

    def test_tax_very_small_amount(self):
        result = self.calc.calculate_tax(0.01)
        self.assertAlmostEqual(result, 0.0023, places=4)

    def test_tax_very_large_amount(self):
        result = self.calc.calculate_tax(1000000.0)
        self.assertEqual(result, 230000.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_without_discount(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_free_shipping(self):
        self.calc.add_item('Item', 150.0)
        total = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_with_paid_shipping(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_at_shipping_threshold(self):
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_negative_discount(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_discount_greater_than_100(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=110.0)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_single_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_quantity_multiple(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_different(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_updates_after_add(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_updates_after_remove(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_sum_of_quantities(self):
        self.calc.add_item('A', 1.0, 10)
        self.calc.add_item('B', 2.0, 20)
        self.calc.add_item('C', 3.0, 30)
        self.assertEqual(self.calc.total_items(), 60)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_is_empty_true(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_total_items_zero(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order_list_items_empty(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertEqual(self.calc.list_items(), [])

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_multiple(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_single(self):
        self.calc.add_item('Apple', 1.5)
        items = self.calc.list_items()
        self.assertEqual(items, ['Apple'])

    def test_list_items_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_correct_names(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_updates_after_add(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(len(self.calc.list_items()), 1)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(len(self.calc.list_items()), 2)

    def test_list_items_updates_after_remove(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        items = self.calc.list_items()
        self.assertEqual(items, ['Banana'])

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_order_modification(self):
        self.calc.add_item('Item1', 50.0)
        self.calc.add_item('Item2', 30.0)
        self.assertEqual(self.calc.get_subtotal(), 80.0)
        self.calc.remove_item('Item1')
        self.assertEqual(self.calc.get_subtotal(), 30.0)
        self.calc.add_item('Item3', 40.0)
        self.assertEqual(self.calc.get_subtotal(), 70.0)

    def test_multiple_orders_same_calculator(self):
        self.calc.add_item('Order1Item', 50.0)
        total1 = self.calc.calculate_total()
        self.calc.clear_order()
        self.calc.add_item('Order2Item', 100.0)
        total2 = self.calc.calculate_total()
        self.assertNotEqual(total1, total2)

    def test_state_consistency(self):
        self.calc.add_item('Item1', 25.0, 2)
        self.calc.add_item('Item2', 50.0)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 100.0)
        self.assertEqual(len(self.calc.list_items()), 2)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Item1')
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 50.0)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_large_order(self):
        for i in range(100):
            self.calc.add_item(f'Item{i}', 10.0, 5)
        self.assertEqual(self.calc.total_items(), 500)
        self.assertEqual(self.calc.get_subtotal(), 5000.0)
        self.assertEqual(len(self.calc.list_items()), 100)