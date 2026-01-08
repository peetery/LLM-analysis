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

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_with_large_quantity(self):
        self.calc.add_item('Widget', 10.0, 100)
        self.assertEqual(self.calc.total_items(), 100)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'expensive')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 2.5)

    def test_add_duplicate_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_from_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_empty_order(self):
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_subtotal_after_removal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.get_subtotal(), 3.0)

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
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 10.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
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

    def test_shipping_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_shipping(-50.0)

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_tax_with_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_tax_decimal_amount(self):
        result = self.calc.calculate_tax(50.5)
        self.assertAlmostEqual(result, 11.615, places=2)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, shipping_cost=10.0, free_shipping_threshold=100.0)

    def test_total_empty_order(self):
        result = self.calc.calculate_total()
        self.assertEqual(result, 10.0)

    def test_total_single_item_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 50.0 + 10.0 + (50.0 + 10.0) * 0.23, places=2)

    def test_total_above_free_shipping_threshold(self):
        self.calc.add_item('Widget', 120.0, 1)
        result = self.calc.calculate_total()
        self.assertAlmostEqual(result, 120.0 + 120.0 * 0.23, places=2)

    def test_total_with_discount(self):
        self.calc.add_item('Widget', 100.0, 1)
        result = self.calc.calculate_total(discount=10.0)
        subtotal_after_discount = 90.0
        self.assertAlmostEqual(result, subtotal_after_discount + subtotal_after_discount * 0.23, places=2)

    def test_total_negative_discount(self):
        self.calc.add_item('Widget', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_discount_over_100(self):
        self.calc.add_item('Widget', 100.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=110.0)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 5)
        self.assertEqual(self.calc.total_items(), 7)

    def test_total_items_after_removal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 5)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty(self):
        result = self.calc.list_items()
        self.assertEqual(result, [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        result = self.calc.list_items()
        self.assertEqual(len(result), 1)
        self.assertIn('Apple', result[0])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        result = self.calc.list_items()
        self.assertEqual(len(result), 2)

    def test_list_items_returns_list(self):
        self.calc.add_item('Apple', 1.5, 2)
        result = self.calc.list_items()
        self.assertIsInstance(result, list)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_calculator(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removal(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_full_order_workflow(self):
        calc = OrderCalculator(tax_rate=0.2, shipping_cost=15.0, free_shipping_threshold=200.0)
        calc.add_item('Laptop', 999.99, 1)
        calc.add_item('Mouse', 29.99, 2)
        calc.add_item('Keyboard', 79.99, 1)
        self.assertEqual(calc.total_items(), 4)
        self.assertFalse(calc.is_empty())
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 1139.96, places=2)
        total = calc.calculate_total(discount=5.0)
        self.assertGreater(total, 0)

    def test_order_below_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, shipping_cost=5.0, free_shipping_threshold=50.0)
        calc.add_item('Book', 20.0, 1)
        total = calc.calculate_total()
        expected = (20.0 + 5.0) * 1.1
        self.assertAlmostEqual(total, expected, places=2)

    def test_order_at_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.1, shipping_cost=5.0, free_shipping_threshold=50.0)
        calc.add_item('Book', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 * 1.1
        self.assertAlmostEqual(total, expected, places=2)