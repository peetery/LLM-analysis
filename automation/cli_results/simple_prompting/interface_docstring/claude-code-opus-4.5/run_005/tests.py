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

    def test_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_tax_rate_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_free_shipping_threshold_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_shipping_cost_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_same_item_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_different_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 4)
        self.assertEqual(self.calc.total_items(), 6)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5, 1)

    def test_add_item_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0, 1)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5, 1)

    def test_add_item_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 1)

    def test_add_item_name_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5, 1)

    def test_add_item_price_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5', 1)

    def test_add_item_quantity_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 1.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()
        self.calc.add_item('Apple', 1.5, 3)

    def test_remove_existing_item(self):
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_nonexistent_item_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_from_empty_order_raises_value_error(self):
        self.calc.clear_order()
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_full_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_partial_discount(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_subtotal_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_shipping_below_threshold(self):
        result = self.calc.calculate_shipping(99.99)
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

    def test_shipping_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23)

    def test_calculate_tax_positive_amount(self):
        result = self.calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_no_discount_below_free_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        result = self.calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_no_discount_above_free_shipping(self):
        self.calc.add_item('Item', 50.0, 3)
        result = self.calc.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount(self):
        self.calc.add_item('Item', 100.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = (80.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_with_discount_free_shipping(self):
        self.calc.add_item('Item', 125.0, 1)
        result = self.calc.calculate_total(0.2)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(result, expected, places=2)

    def test_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_invalid_discount_raises_value_error(self):
        self.calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_total_negative_discount_raises_value_error(self):
        self.calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_total_discount_wrong_type_raises_type_error(self):
        self.calc.add_item('Item', 50.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()
        self.calc.add_item('Apple', 1.5, 3)
        self.calc.add_item('Banana', 0.75, 2)

    def test_clear_order(self):
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_clear_already_empty_order(self):
        self.calc.clear_order()
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 0.75, 3)
        result = self.calc.list_items()
        self.assertIn('Apple', result)
        self.assertIn('Banana', result)
        self.assertEqual(len(result), 2)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_removing_item(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())