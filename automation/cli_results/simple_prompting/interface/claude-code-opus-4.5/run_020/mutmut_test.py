import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        self.assertTrue(calc.is_empty())

    def test_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        calc.add_item('item', 100.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_custom_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('item', 60.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('item', 10.0)
        self.assertEqual(calc.calculate_shipping(10.0), 15.0)

class TestAddItem(unittest.TestCase):

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertEqual(calc.total_items(), 1)
        self.assertFalse(calc.is_empty())

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        self.assertEqual(calc.total_items(), 2)

    def test_add_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 2)
        calc.add_item('apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.add_item('item', -5.0)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.add_item('item', 0.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.add_item('item', 10.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.add_item('item', 10.0, -1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.add_item('', 10.0)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError, Exception)):
            calc.add_item('item', 'invalid')

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises((TypeError, ValueError, Exception)):
            calc.add_item('item', 10.0, 1.5)

class TestRemoveItem(unittest.TestCase):

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        self.assertTrue(calc.is_empty())

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError, Exception)):
            calc.remove_item('nonexistent')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises((KeyError, ValueError, Exception)):
            calc.remove_item('item')

    def test_remove_one_of_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        calc.remove_item('apple')
        self.assertEqual(calc.total_items(), 1)

class TestGetSubtotal(unittest.TestCase):

    def test_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_subtotal_single_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0, 3)
        self.assertEqual(calc.get_subtotal(), 30.0)

    def test_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0, 2)
        calc.add_item('banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)

    def test_subtotal_with_floats(self):
        calc = OrderCalculator()
        calc.add_item('item1', 10.99)
        calc.add_item('item2', 5.01)
        self.assertAlmostEqual(calc.get_subtotal(), 16.0)

class TestApplyDiscount(unittest.TestCase):

    def test_apply_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeding_100(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.apply_discount(100.0, 150.0)

class TestCalculateShipping(unittest.TestCase):

    def test_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_shipping_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.calculate_shipping(49.99), 10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

class TestCalculateTax(unittest.TestCase):

    def test_tax_default_rate(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises((ValueError, Exception)):
            calc.calculate_tax(-50.0)

class TestCalculateTotal(unittest.TestCase):

    def test_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 100.0)
        result = calc.calculate_total()
        self.assertEqual(result, 123.0)

    def test_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('item', 150.0)
        result = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('item', 100.0)
        with self.assertRaises((ValueError, Exception)):
            calc.calculate_total(discount=-10.0)

class TestTotalItems(unittest.TestCase):

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_quantities(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 2)
        calc.add_item('banana', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def test_clear_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

class TestListItems(unittest.TestCase):

    def test_list_items_empty(self):
        calc = OrderCalculator()
        result = calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        result = calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('apple', result[0])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.add_item('banana', 2.0)
        result = calc.list_items()
        self.assertEqual(len(result), 2)

class TestIsEmpty(unittest.TestCase):

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.remove_item('apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_order_just_below_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('item', 99.99)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 10.0)

    def test_order_exactly_at_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('item', 100.0)
        self.assertEqual(calc.calculate_shipping(calc.get_subtotal()), 0.0)