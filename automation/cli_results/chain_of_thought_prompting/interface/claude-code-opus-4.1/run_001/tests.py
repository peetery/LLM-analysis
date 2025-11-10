import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        self.assertEqual(calc.tax_rate, 0.15)

    def test_init_with_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        self.assertEqual(calc.free_shipping_threshold, 200.0)

    def test_init_with_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_init_with_all_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=150.0, shipping_cost=20.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 150.0)
        self.assertEqual(calc.shipping_cost, 20.0)

    def test_init_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_with_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_with_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_with_negative_tax_rate_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_with_negative_free_shipping_threshold_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_negative_shipping_cost_raises_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_non_numeric_tax_rate_raises_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_non_numeric_free_shipping_threshold_raises_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_non_numeric_shipping_cost_raises_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

class TestOrderCalculatorAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_multiple_quantity(self):
        self.calc.add_item('Orange', 2.0, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 2)
        self.calc.add_item('Orange', 2.0, 3)
        self.assertEqual(len(self.calc.items), 3)

    def test_add_same_item_increases_quantity(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_with_float_price(self):
        self.calc.add_item('Milk', 3.99, 1)
        self.assertEqual(self.calc.items[0]['price'], 3.99)

    def test_add_item_with_int_price(self):
        self.calc.add_item('Bread', 5, 1)
        self.assertEqual(self.calc.items[0]['price'], 5)

    def test_add_item_with_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_add_item_with_zero_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free Item', 0.0, 1)

    def test_add_item_with_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Invalid', -1.0, 1)

    def test_add_item_with_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_with_negative_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_with_non_string_name_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)

    def test_add_item_with_non_numeric_price_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0', 1)

    def test_add_item_with_non_int_quantity_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, 1.5)

    def test_add_item_same_name_different_price_raises_error(self):
        self.calc.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 1)

class TestOrderCalculatorRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_one_of_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 2)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_nonexistent_item_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_from_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Anything')

    def test_remove_item_with_non_string_name_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestOrderCalculatorGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 1.0)

    def test_get_subtotal_single_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 4)
        self.assertEqual(self.calc.get_subtotal(), 4.0)

    def test_get_subtotal_with_decimal_prices(self):
        self.calc.add_item('Milk', 3.99, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.98, places=2)

    def test_get_subtotal_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestOrderCalculatorApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_no_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_ten_percent_discount(self):
        result = self.calc.apply_discount(100.0, 0.1)
        self.assertEqual(result, 90.0)

    def test_apply_fifty_percent_discount(self):
        result = self.calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_hundred_percent_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_with_decimal_values(self):
        result = self.calc.apply_discount(123.45, 0.2)
        self.assertAlmostEqual(result, 98.76, places=2)

    def test_apply_discount_negative_subtotal_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_negative_discount_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_non_numeric_subtotal_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_non_numeric_discount_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

class TestOrderCalculatorCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        shipping = self.calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_zero_amount(self):
        shipping = self.calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_with_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_calculate_shipping_with_custom_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_non_numeric_input_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

class TestOrderCalculatorCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_tax_on_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_on_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_decimal_amount(self):
        tax = self.calc.calculate_tax(123.45)
        self.assertAlmostEqual(tax, 28.3935, places=4)

    def test_calculate_tax_with_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.1)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 10.0)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_non_numeric_amount_raises_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

class TestOrderCalculatorCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_calculate_total_single_item_no_discount(self):
        self.calc.add_item('Apple', 10.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 24.6, places=2)

    def test_calculate_total_single_item_with_discount(self):
        self.calc.add_item('Apple', 100.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 110.7, places=2)

    def test_calculate_total_above_free_shipping_threshold(self):
        self.calc.add_item('Expensive Item', 150.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 184.5, places=2)

    def test_calculate_total_at_free_shipping_threshold(self):
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_multiple_items(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 3)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 55.25, places=2)

    def test_calculate_total_with_fifty_percent_discount(self):
        self.calc.add_item('Item', 200.0, 1)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_empty_order_raises_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_non_numeric_discount_raises_error(self):
        self.calc.add_item('Apple', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

class TestOrderCalculatorTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item_single_quantity(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertEqual(self.calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 0.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_after_adding_same_item(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestOrderCalculatorClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 2)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_empty_order(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_resets_to_empty_list(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])

class TestOrderCalculatorListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items[0])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 0.5, 2)
        self.calc.add_item('Orange', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertTrue(any(('Apple' in item for item in items)))
        self.assertTrue(any(('Banana' in item for item in items)))
        self.assertTrue(any(('Orange' in item for item in items)))

    def test_list_items_no_duplicates(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)

class TestOrderCalculatorIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_on_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_item(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())