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

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_same_item_twice(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('', 1.5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises((TypeError, ValueError)):
            self.calc.add_item('Apple', 'invalid')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises((TypeError, ValueError)):
            self.calc.add_item('Apple', 1.5, quantity='two')

    def test_add_item_none_name(self):
        with self.assertRaises((TypeError, ValueError)):
            self.calc.add_item(None, 1.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Nonexistent')

    def test_remove_from_empty_order(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Apple')

    def test_remove_one_of_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_remove_item_case_sensitive(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('apple')

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_empty_order(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 10.0)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_subtotal_single_item_with_quantity(self):
        self.calc.add_item('Apple', 10.0, quantity=3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 10.0, quantity=2)
        self.calc.add_item('Banana', 5.0, quantity=3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_subtotal_with_decimal_prices(self):
        self.calc.add_item('Apple', 1.99, quantity=2)
        self.calc.add_item('Banana', 2.49)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.47, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_valid_discount(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_full_discount(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_greater_than_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 150.0)

    def test_apply_discount_to_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_decimal_values(self):
        result = self.calc.apply_discount(99.99, 10.5)
        self.assertAlmostEqual(result, 89.49, places=2)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

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

    def test_shipping_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.0), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_tax_on_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_decimal_amount(self):
        result = self.calc.calculate_tax(50.5)
        self.assertAlmostEqual(result, 11.615, places=2)

    def test_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_empty_order(self):
        result = self.calc.calculate_total()
        self.assertEqual(result, 10.0)

    def test_total_single_item_below_threshold(self):
        self.calc.add_item('Apple', 50.0)
        result = self.calc.calculate_total()
        expected = 50.0 * 1.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_above_free_shipping_threshold(self):
        self.calc.add_item('Laptop', 150.0)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=20.0)
        expected = 80.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount_below_threshold(self):
        self.calc.add_item('Item', 110.0)
        result = self.calc.calculate_total(discount=20.0)
        expected = 90.0 * 1.23 + 10.0
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_negative_discount(self):
        self.calc.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_discount_exceeds_subtotal(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=60.0)

    def test_total_multiple_items(self):
        self.calc.add_item('Apple', 30.0, quantity=2)
        self.calc.add_item('Banana', 20.0, quantity=2)
        result = self.calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.calc.add_item('Banana', 2.0, quantity=2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_after_remove(self):
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.calc.add_item('Banana', 2.0, quantity=2)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 2)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_resets_subtotal(self):
        self.calc.add_item('Apple', 10.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_clear_resets_total_items(self):
        self.calc.add_item('Apple', 10.0, quantity=5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty(self):
        result = self.calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('Apple', result[0])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        result = self.calc.list_items()
        self.assertEqual(len(result), 2)

    def test_list_items_returns_list_type(self):
        self.calc.add_item('Apple', 1.5)
        result = self.calc.list_items()
        self.assertIsInstance(result, list)

    def test_list_items_contains_strings(self):
        self.calc.add_item('Apple', 1.5)
        result = self.calc.list_items()
        for item in result:
            self.assertIsInstance(item, str)

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

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Laptop', 500.0)
        calc.add_item('Mouse', 25.0, quantity=2)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 550.0)
        total = calc.calculate_total(discount=50.0)
        expected = 500.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_workflow_with_clear_and_reuse(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0)
        calc.clear_order()
        calc.add_item('Item2', 75.0)
        self.assertEqual(calc.get_subtotal(), 75.0)
        self.assertEqual(calc.total_items(), 1)

    def test_boundary_free_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 99.99)
        shipping = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping, 10.0)
        calc.add_item('Extra', 0.02)
        shipping = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping, 0.0)