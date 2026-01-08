import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_with_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_with_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_with_minimum_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_with_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_with_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_with_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_with_tax_rate_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_with_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_with_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_with_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_with_non_numeric_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_with_non_numeric_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_with_non_numeric_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item_with_default_quantity(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        self.calc.add_item('Banana', 2.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_duplicate_item_increases_quantity(self):
        self.calc.add_item('Orange', 3.0, 2)
        self.calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(len(self.calc.items), 3)

    def test_add_item_with_very_large_quantity(self):
        self.calc.add_item('Grape', 0.5, 10000)
        self.assertEqual(self.calc.items[0]['quantity'], 10000)

    def test_add_item_with_float_price(self):
        self.calc.add_item('Peach', 2.99)
        self.assertEqual(self.calc.items[0]['price'], 2.99)

    def test_add_item_with_integer_price(self):
        self.calc.add_item('Pear', 5)
        self.assertEqual(self.calc.items[0]['price'], 5)

    def test_add_item_with_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_add_item_with_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Free Item', 0.0)

    def test_add_item_with_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative', -1.0)

    def test_add_item_with_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Zero Qty', 1.0, 0)

    def test_add_item_with_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Qty', 1.0, -1)

    def test_add_item_with_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_with_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_add_item_with_non_numeric_price_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '1.0')

    def test_add_item_with_non_integer_quantity_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 1.0, 2.5)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_from_multi_item_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        self.calc.remove_item('Banana')
        self.assertEqual(len(self.calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in self.calc.items])

    def test_remove_non_existent_item_raises_value_error(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_from_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_with_non_string_name_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_get_subtotal_with_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.get_subtotal(), 4.5)

    def test_get_subtotal_with_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_get_subtotal_with_items_different_quantities(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 5)
        self.calc.add_item('Orange', 3.0, 10)
        self.assertEqual(self.calc.get_subtotal(), 41.0)

    def test_get_subtotal_with_large_quantity(self):
        self.calc.add_item('Grape', 0.1, 1000)
        self.assertEqual(self.calc.get_subtotal(), 100.0)

    def test_get_subtotal_on_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

class TestApplyDiscount(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_apply_valid_discount(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_zero_discount(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_full_discount(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_on_zero_subtotal(self):
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_small_discount_percentage(self):
        result = self.calc.apply_discount(100.0, 0.01)
        self.assertEqual(result, 99.0)

    def test_apply_discount_below_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_on_negative_subtotal_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_with_non_numeric_subtotal_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)

    def test_apply_discount_with_non_numeric_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

class TestCalculateShipping(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(shipping_cost=10.0, free_shipping_threshold=100.0)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_with_zero_discounted_subtotal(self):
        shipping = self.calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_with_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

class TestCalculateTax(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2)

    def test_calculate_tax_on_positive_amount(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertEqual(tax, 20.0)

    def test_calculate_tax_on_zero_amount(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_on_very_large_amount(self):
        tax = self.calc.calculate_tax(1000000.0)
        self.assertEqual(tax, 200000.0)

    def test_calculate_tax_on_negative_amount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_with_non_numeric_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, shipping_cost=10.0, free_shipping_threshold=100.0)

    def test_calculate_total_no_discount_below_shipping_threshold(self):
        self.calc.add_item('Apple', 10.0, 5)
        total = self.calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_no_discount_above_shipping_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_with_discount_below_shipping_threshold(self):
        self.calc.add_item('Apple', 20.0, 5)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 100.0 * 0.9
        expected = discounted + 10.0 + (discounted + 10.0) * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_with_discount_above_shipping_threshold(self):
        self.calc.add_item('Apple', 50.0, 3)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 150.0 * 0.9
        expected = discounted + 0.0 + discounted * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_discount_brings_below_threshold(self):
        self.calc.add_item('Apple', 110.0, 1)
        total = self.calc.calculate_total(discount=0.2)
        discounted = 110.0 * 0.8
        expected = discounted + 10.0 + (discounted + 10.0) * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_discount_keeps_above_threshold(self):
        self.calc.add_item('Apple', 200.0, 1)
        total = self.calc.calculate_total(discount=0.3)
        discounted = 200.0 * 0.7
        expected = discounted + 0.0 + discounted * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_with_zero_discount_explicitly(self):
        self.calc.add_item('Apple', 50.0, 2)
        total = self.calc.calculate_total(0.0)
        expected = 100.0 + 0.0 + 100.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_on_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_with_invalid_discount_raises_value_error(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_with_non_numeric_discount_raises_type_error(self):
        self.calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_on_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_with_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_with_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 5)
        self.calc.add_item('Orange', 3.0, 1)
        self.assertEqual(self.calc.total_items(), 8)

    def test_total_items_with_varying_quantities(self):
        self.calc.add_item('Apple', 1.0, 10)
        self.calc.add_item('Banana', 2.0, 1)
        self.calc.add_item('Orange', 3.0, 100)
        self.assertEqual(self.calc.total_items(), 111)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_non_empty_order(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.calc.add_item('Banana', 2.0, 2)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_already_empty_order(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_order_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_non_empty_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty_order(self):
        items = self.calc.list_items()
        self.assertEqual(items, [])

    def test_list_items_uniqueness(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_unique_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.add_item('Orange', 3.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 3)

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_on_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_adding_items(self):
        self.calc.add_item('Apple', 1.5)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_adding_and_removing_all_items(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_clear_order(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestIntegrationWorkflows(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.1, shipping_cost=5.0, free_shipping_threshold=50.0)

    def test_complete_order_workflow(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 4)
        subtotal = self.calc.get_subtotal()
        self.assertEqual(subtotal, 40.0)
        total = self.calc.calculate_total(discount=0.1)
        discounted = 40.0 * 0.9
        shipping = 5.0
        tax = (discounted + shipping) * 0.1
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_add_remove_add_same_item(self):
        self.calc.add_item('Apple', 10.0, 3)
        self.calc.remove_item('Apple')
        self.calc.add_item('Apple', 10.0, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_discount_affects_shipping_determination(self):
        self.calc.add_item('Item', 55.0, 1)
        total_no_discount = self.calc.calculate_total(discount=0.0)
        discounted_subtotal_no_disc = 55.0
        shipping_no_disc = 0.0
        tax_no_disc = (discounted_subtotal_no_disc + shipping_no_disc) * 0.1
        expected_no_disc = discounted_subtotal_no_disc + shipping_no_disc + tax_no_disc
        self.assertEqual(total_no_discount, expected_no_disc)
        self.calc.clear_order()
        self.calc.add_item('Item', 55.0, 1)
        total_with_discount = self.calc.calculate_total(discount=0.2)
        discounted_subtotal = 55.0 * 0.8
        shipping = 5.0
        tax = (discounted_subtotal + shipping) * 0.1
        expected_with_disc = discounted_subtotal + shipping + tax
        self.assertEqual(total_with_discount, expected_with_disc)

    def test_tax_calculation_on_final_amount(self):
        self.calc.add_item('Item', 30.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        discounted = 30.0
        shipping = 5.0
        tax = (discounted + shipping) * 0.1
        expected = discounted + shipping + tax
        self.assertEqual(total, expected)

    def test_order_state_after_failed_add_item(self):
        self.calc.add_item('Apple', 10.0, 2)
        try:
            self.calc.add_item('Apple', 15.0, 3)
        except ValueError:
            pass
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['price'], 10.0)
        self.assertEqual(self.calc.items[0]['quantity'], 2)