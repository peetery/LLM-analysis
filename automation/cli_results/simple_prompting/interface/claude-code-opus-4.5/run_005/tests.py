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

    def test_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_all_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=200.0, shipping_cost=25.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 25.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calc.add_item('apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_empty_name(self):
        with self.assertRaises((ValueError, TypeError)):
            self.calc.add_item('', 1.5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', -1.5)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', 1.5, quantity=-1)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', 1.5, quantity=0)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('apple', 'invalid')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('apple', 1.5, quantity='invalid')

    def test_add_item_none_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 1.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('apple', 1.5)
        self.calc.remove_item('apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('nonexistent')

    def test_remove_from_multiple_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        self.calc.remove_item('apple')
        self.assertEqual(self.calc.total_items(), 1)

    def test_remove_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_empty_order(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_subtotal_single_item(self):
        self.calc.add_item('apple', 10.0)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_subtotal_single_item_with_quantity(self):
        self.calc.add_item('apple', 10.0, quantity=3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('apple', 10.0)
        self.calc.add_item('banana', 5.0, quantity=2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_subtotal_float_precision(self):
        self.calc.add_item('item1', 0.1)
        self.calc.add_item('item2', 0.2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_percentage_discount(self):
        result = self.calc.apply_discount(100.0, 10.0)
        self.assertEqual(result, 90.0)

    def test_apply_full_discount(self):
        result = self.calc.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_100(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 150.0)

    def test_apply_discount_to_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

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

    def test_shipping_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_shipping_custom_cost(self):
        calc = OrderCalculator(shipping_cost=20.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 20.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_tax_default_rate(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_tax_float_precision(self):
        result = self.calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_empty_order(self):
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 12.3, places=2)

    def test_total_single_item_no_discount(self):
        self.calc.add_item('item', 100.0)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 123.0, places=2)

    def test_total_with_discount(self):
        self.calc.add_item('item', 100.0)
        result = self.calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(result, 110.7, places=2)

    def test_total_below_free_shipping(self):
        self.calc.add_item('item', 50.0)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 73.8, places=2)

    def test_total_at_free_shipping_threshold(self):
        self.calc.add_item('item', 100.0)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 123.0, places=2)

    def test_total_above_free_shipping(self):
        self.calc.add_item('item', 150.0)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 184.5, places=2)

    def test_total_negative_discount(self):
        self.calc.add_item('item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_discount_over_100(self):
        self.calc.add_item('item', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=110.0)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_with_quantity(self):
        self.calc.add_item('apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('apple', 1.5, quantity=2)
        self.calc.add_item('banana', 2.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_with_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_resets_subtotal(self):
        self.calc.add_item('apple', 10.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_clear_order_resets_total_items(self):
        self.calc.add_item('apple', 1.5, quantity=5)
        self.calc.clear_order()
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty(self):
        result = self.calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single_item(self):
        self.calc.add_item('apple', 1.5)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('apple', result[0])

    def test_list_items_multiple_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        result = self.calc.list_items()
        self.assertEqual(len(result), 2)

    def test_list_items_returns_list(self):
        result = self.calc.list_items()
        self.assertIsInstance(result, list)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_item(self):
        self.calc.add_item('apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_remove(self):
        self.calc.add_item('apple', 1.5)
        self.calc.remove_item('apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_complete_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('item1', 20.0, quantity=2)
        calc.add_item('item2', 15.0)
        self.assertEqual(calc.get_subtotal(), 55.0)
        self.assertEqual(calc.total_items(), 3)
        self.assertFalse(calc.is_empty())
        total = calc.calculate_total(discount=10.0)
        self.assertAlmostEqual(total, 59.4, places=2)

    def test_order_modification(self):
        calc = OrderCalculator()
        calc.add_item('apple', 10.0)
        calc.add_item('banana', 5.0)
        self.assertEqual(calc.get_subtotal(), 15.0)
        calc.remove_item('banana')
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_multiple_clears_and_adds(self):
        calc = OrderCalculator()
        calc.add_item('item', 10.0)
        calc.clear_order()
        calc.add_item('new_item', 20.0)
        self.assertEqual(calc.get_subtotal(), 20.0)
        self.assertEqual(calc.total_items(), 1)