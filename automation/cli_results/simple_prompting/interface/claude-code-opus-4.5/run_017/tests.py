import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_default_initialization(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_custom_initialization(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_negative_tax_rate_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_negative_shipping_cost_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_negative_threshold_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

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

    def test_add_item_empty_name_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)

    def test_add_item_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5)

    def test_add_item_zero_price(self):
        self.calc.add_item('Free Sample', 0.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_invalid_name_type_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)

    def test_add_item_invalid_price_type_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'expensive')

    def test_add_item_invalid_quantity_type_raises(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, quantity='five')

    def test_add_same_item_twice_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item_raises(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Apple')

    def test_remove_from_empty_order_raises(self):
        with self.assertRaises(KeyError):
            self.calc.remove_item('Apple')

    def test_remove_one_of_multiple_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 1)

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
        self.calc.add_item('Item1', 1.99, quantity=2)
        self.calc.add_item('Item2', 3.49)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.47, places=2)

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

    def test_apply_negative_discount_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_over_100_raises(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_apply_discount_to_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 50.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_fractional(self):
        result = self.calc.apply_discount(100.0, 15.5)
        self.assertAlmostEqual(result, 84.5, places=2)

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

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_decimal_amount(self):
        result = self.calc.calculate_tax(50.5)
        self.assertAlmostEqual(result, 11.615, places=3)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_empty_order(self):
        result = self.calc.calculate_total()
        self.assertEqual(result, 0.0)

    def test_total_single_item_below_threshold(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_above_threshold_free_shipping(self):
        self.calc.add_item('Item', 150.0)
        result = self.calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount(self):
        self.calc.add_item('Item', 100.0)
        result = self.calc.calculate_total(discount=10.0)
        expected = 90.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount_and_shipping(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total(discount=10.0)
        discounted = 45.0
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_negative_discount_raises(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-10.0)

    def test_total_100_percent_discount(self):
        self.calc.add_item('Item', 50.0)
        result = self.calc.calculate_total(discount=100.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_with_quantity(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, quantity=2)
        self.calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(self.calc.total_items(), 5)

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

    def test_clear_order_resets_subtotal(self):
        self.calc.add_item('Apple', 10.0)
        self.calc.clear_order()
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_clear_order_resets_total_items(self):
        self.calc.add_item('Apple', 1.5, quantity=5)
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

    def test_list_items_returns_list(self):
        self.calc.add_item('Apple', 1.5)
        result = self.calc.list_items()
        self.assertIsInstance(result, list)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_item(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())