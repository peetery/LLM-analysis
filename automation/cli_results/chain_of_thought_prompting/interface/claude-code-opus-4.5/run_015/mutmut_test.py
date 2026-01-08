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
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=200.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 20.0)

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
        self.assertIn('Apple', self.calc.list_items())

    def test_add_single_item_explicit_quantity(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.list_items()), 3)

    def test_add_item_same_name_twice(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_with_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_with_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_with_very_large_price(self):
        self.calc.add_item('Expensive', 1000000.0)
        self.assertEqual(self.calc.get_subtotal(), 1000000.0)

    def test_add_item_with_very_large_quantity(self):
        self.calc.add_item('Bulk', 1.0, 1000000)
        self.assertEqual(self.calc.total_items(), 1000000)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_from_cart_with_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertNotIn('Apple', self.calc.list_items())
        self.assertIn('Banana', self.calc.list_items())

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_with_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_subtotal_with_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 4.5)

    def test_subtotal_with_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_subtotal_precision_with_decimals(self):
        self.calc.add_item('Item1', 0.1, 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.3, places=2)

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_negative_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_below_threshold(self):
        result = self.calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_subtotal_exactly_at_threshold(self):
        result = self.calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_subtotal_above_threshold(self):
        result = self.calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_subtotal_just_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_subtotal_just_above_threshold(self):
        result = self.calc.calculate_shipping(100.01)
        self.assertEqual(result, 0.0)

    def test_zero_subtotal(self):
        result = self.calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_tax_on_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_on_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_with_default_rate(self):
        result = self.calc.calculate_tax(200.0)
        self.assertEqual(result, 46.0)

    def test_tax_with_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 10.0)

    def test_tax_with_zero_rate(self):
        calc = OrderCalculator(tax_rate=0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_precision_with_decimals(self):
        result = self.calc.calculate_tax(33.33)
        self.assertAlmostEqual(result, 7.6659, places=2)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_no_discount_below_shipping_threshold(self):
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_no_discount_above_shipping_threshold(self):
        self.calc.add_item('Item', 150.0)
        total = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_cart(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_item_quantity_greater_than_one(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_after_adding_and_removing(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_cart_with_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_already_empty_cart(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_list_items_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertEqual(self.calc.list_items(), [])

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty_cart(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_returns_names_only(self):
        self.calc.add_item('Apple', 1.5, 3)
        items = self.calc.list_items()
        self.assertEqual(items, ['Apple'])

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_on_new_cart(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_add_get_subtotal_remove_verify_subtotal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        self.assertEqual(calc.get_subtotal(), 20.0)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 15.0)

    def test_recalculate_total_after_modifying_cart(self):
        calc = OrderCalculator()
        calc.add_item('Item', 80.0)
        total1 = calc.calculate_total()
        calc.add_item('Extra', 30.0)
        total2 = calc.calculate_total()
        self.assertNotEqual(total1, total2)
        self.assertGreater(total2, total1)

    def test_cart_state_isolation(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Apple', 10.0)
        self.assertEqual(calc1.total_items(), 1)
        self.assertEqual(calc2.total_items(), 0)