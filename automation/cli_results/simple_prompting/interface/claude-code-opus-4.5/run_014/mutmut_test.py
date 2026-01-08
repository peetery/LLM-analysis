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

    def test_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.08)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_negative_tax_rate_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_negative_shipping_threshold_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_negative_shipping_cost_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_with_quantity(self):
        self.calc.add_item('apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_same_item_twice_increases_quantity(self):
        self.calc.add_item('apple', 1.5, quantity=2)
        self.calc.add_item('apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', -1.5)

    def test_add_item_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', 1.5, quantity=0)

    def test_add_item_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('apple', 1.5, quantity=-1)

    def test_add_item_non_string_name_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_non_numeric_price_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('apple', 'expensive')

    def test_add_item_non_integer_quantity_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('apple', 1.5, quantity=2.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('apple', 1.5)
        self.calc.remove_item('apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_from_multiple(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        self.calc.remove_item('apple')
        self.assertEqual(self.calc.total_items(), 1)

    def test_remove_item_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item(self):
        self.calc.add_item('apple', 10.0)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_subtotal_single_item_with_quantity(self):
        self.calc.add_item('apple', 10.0, quantity=3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('apple', 10.0, quantity=2)
        self.calc.add_item('banana', 5.0, quantity=3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_subtotal_with_float_precision(self):
        self.calc.add_item('item', 0.1, quantity=3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_100_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_negative_subtotal_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 10.0)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)

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

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_tax_on_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_different_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_tax_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_single_item_below_threshold(self):
        self.calc.add_item('apple', 50.0)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_single_item_above_threshold(self):
        self.calc.add_item('apple', 150.0)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_negative_discount_raises(self):
        self.calc.add_item('apple', 100.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_discount_over_100_raises(self):
        self.calc.add_item('apple', 100.0)
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
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('apple', 1.5)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('apple', items[0])

    def test_list_items_multiple_items(self):
        self.calc.add_item('apple', 1.5)
        self.calc.add_item('banana', 2.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)

    def test_list_items_returns_list_of_strings(self):
        self.calc.add_item('apple', 1.5)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        for item in items:
            self.assertIsInstance(item, str)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_item(self):
        self.calc.add_item('apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removal(self):
        self.calc.add_item('apple', 1.5)
        self.calc.remove_item('apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_order_with_free_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0, tax_rate=0.0)
        calc.add_item('item', 150.0)
        total = calc.calculate_total()
        self.assertEqual(total, 150.0)

    def test_order_with_paid_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0, tax_rate=0.0)
        calc.add_item('item', 50.0)
        total = calc.calculate_total()
        self.assertEqual(total, 60.0)