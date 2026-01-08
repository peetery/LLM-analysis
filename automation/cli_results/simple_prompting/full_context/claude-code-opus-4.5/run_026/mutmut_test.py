import unittest
from order_calculator import OrderCalculator

class TestOrderCalculatorInit(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_as_int(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_init_tax_rate_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_free_shipping_threshold_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_free_shipping_threshold_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_shipping_cost_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_shipping_cost_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

class TestAddItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_add_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 1.5)
        self.assertEqual(self.calc.items[0]['quantity'], 3)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_same_name_same_price_increases_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 1)

    def test_add_multiple_different_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 1)
        self.assertEqual(len(self.calc.items), 2)

    def test_add_item_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5, 1)

    def test_add_item_zero_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -1)

    def test_add_item_zero_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0, 1)

    def test_add_item_negative_price_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5, 1)

    def test_add_item_name_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5, 1)

    def test_add_item_price_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5', 1)

    def test_add_item_quantity_not_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 1.5)

    def test_add_item_price_as_int(self):
        self.calc.add_item('Apple', 2, 1)
        self.assertEqual(self.calc.items[0]['price'], 2)

class TestRemoveItem(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_remove_existing_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_from_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 1)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_nonexistent_item_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Apple')

    def test_remove_item_name_not_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

class TestGetSubtotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_subtotal_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_subtotal_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 9.0)

    def test_subtotal_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_subtotal_single_item_quantity_one(self):
        self.calc.add_item('Apple', 10.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

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
            self.calc.apply_discount(-100.0, 0.1)

    def test_apply_discount_negative_discount_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_greater_than_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_subtotal_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_discount_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_with_int_inputs(self):
        result = self.calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

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

    def test_shipping_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_shipping_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 0.0)

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

    def test_calculate_tax_not_number_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_full_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

class TestCalculateTotal(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_total_no_discount_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total(0.0)
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_no_discount_above_threshold(self):
        self.calc.add_item('Apple', 150.0, 1)
        result = self.calc.calculate_total(0.0)
        expected = 150.0 * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_with_discount_below_threshold(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total(0.2)
        discounted = 50.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_with_discount_above_threshold(self):
        self.calc.add_item('Apple', 200.0, 1)
        result = self.calc.calculate_total(0.2)
        discounted = 200.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_empty_order_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.0)

    def test_total_invalid_discount_raises_value_error(self):
        self.calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_total_negative_discount_raises_value_error(self):
        self.calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_total_discount_not_number_raises_type_error(self):
        self.calc.add_item('Apple', 50.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_default_discount(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_at_threshold_with_discount(self):
        self.calc.add_item('Apple', 125.0, 1)
        result = self.calc.calculate_total(0.2)
        discounted = 125.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(result, expected)

    def test_total_full_discount(self):
        self.calc.add_item('Apple', 50.0, 1)
        result = self.calc.calculate_total(1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(result, expected)

class TestTotalItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_total_items_empty_order(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_after_adding_same_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

class TestClearOrder(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_clear_order_with_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 1)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_empty_order(self):
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)

    def test_clear_order_resets_to_empty(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

class TestListItems(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_list_items_empty_order(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items_single_item(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Banana', 2.0, 1)
        result = self.calc.list_items()
        self.assertEqual(set(result), {'Apple', 'Banana'})

    def test_list_items_no_duplicates(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.list_items(), ['Apple'])

class TestIsEmpty(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_is_empty_new_order(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_with_items(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_after_clear(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_remove_all_items(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

class TestIntegration(unittest.TestCase):

    def test_workflow_with_item_removal(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 1)
        calc.add_item('Item2', 30.0, 2)
        calc.remove_item('Item1')
        self.assertEqual(calc.get_subtotal(), 60.0)
        self.assertEqual(calc.total_items(), 2)

    def test_workflow_add_remove_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.remove_item('Apple')
        calc.add_item('Banana', 5.0, 2)
        self.assertEqual(calc.list_items(), ['Banana'])
        self.assertEqual(calc.total_items(), 2)