import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_minimum_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_maximum_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_free_shipping_threshold_zero(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_shipping_cost_zero(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_tax_rate_invalid_type_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_invalid_type_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_shipping_cost_invalid_type_list(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_item_single_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_duplicate_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, 2)
        calc.add_item('Orange', 3.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_with_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Grape', 5, 2)
        self.assertEqual(calc.items[0]['price'], 5)

    def test_add_item_quantity_boundary_one(self):
        calc = OrderCalculator()
        calc.add_item('Mango', 4.5, 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Watermelon', 10.0, 10000)
        self.assertEqual(calc.items[0]['quantity'], 10000)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Candy', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -5.0)

    def test_add_item_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 1.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', 1.0, -1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_name_invalid_type_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_price_invalid_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '1.0')

    def test_add_item_quantity_invalid_type_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.0, 1.5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_only_item_in_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_order_state_after_removal(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 2.0, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_invalid_type_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_varying_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.add_item('Banana', 2.5, 4)
        calc.add_item('Orange', 3.0, 2)
        self.assertEqual(calc.get_subtotal(), 17.5)

    def test_get_subtotal_decimal_accuracy(self):
        calc = OrderCalculator()
        calc.add_item('Item', 1.99, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 5.97, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_decimal_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(123.45, 0.15)
        self.assertAlmostEqual(result, 104.9325, places=4)

    def test_apply_discount_minimum_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_maximum_boundary(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.2)

    def test_apply_discount_subtotal_invalid_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100.0', 0.2)

    def test_apply_discount_discount_invalid_type_none(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, None)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_invalid_type_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100.0')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(10000.0)
        self.assertEqual(result, 2300.0)

    def test_calculate_tax_decimal_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(123.45)
        self.assertAlmostEqual(result, 28.3935, places=4)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_tax_invalid_type_list(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax([100.0])

    def test_calculate_total_without_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=0.2)
        discounted = 50.0 * 0.8
        expected = discounted + 10.0 + (discounted + 10.0) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 25.0, 5)
        total = calc.calculate_total()
        expected = 125.0 + 125.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_paid_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_at_shipping_threshold_boundary(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_maximum_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_calculate_total_order_of_operations(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=0.5)
        subtotal = 100.0
        discounted = 50.0
        shipping = 10.0
        tax = 60.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_below_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.1)

    def test_calculate_total_discount_invalid_type_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.add_item('Orange', 3.0, 1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 2.0, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_state_verification(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Orange', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Orange', items)

    def test_list_items_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Apple', items)

    def test_list_items_after_adding_duplicate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Apple', 1.5, 2)
        items = calc.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_initially(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_full_order_lifecycle(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.total_items(), 5)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)
        total = calc.calculate_total(discount=0.1)
        self.assertGreater(total, 0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_multiple_discount_scenarios_affect_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('Item', 60.0, 1)
        total_no_discount = calc.calculate_total(discount=0.0)
        total_with_discount = calc.calculate_total(discount=0.2)
        self.assertNotEqual(total_no_discount, total_with_discount)

    def test_precision_with_many_decimals(self):
        calc = OrderCalculator(tax_rate=0.123456)
        calc.add_item('Item', 9.876543, 7)
        total = calc.calculate_total(discount=0.111111)
        self.assertIsInstance(total, float)
        self.assertGreater(total, 0)

    def test_state_consistency_after_modifications(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        items_count = calc.total_items()
        items_list = calc.list_items()
        is_empty_status = calc.is_empty()
        self.assertEqual(items_count, 5)
        self.assertEqual(len(items_list), 2)
        self.assertFalse(is_empty_status)

    def test_shipping_threshold_edge_case_just_above(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Item', 110.0, 1)
        total_no_discount = calc.calculate_total(discount=0.0)
        calc2 = OrderCalculator(free_shipping_threshold=100.0)
        calc2.add_item('Item', 110.0, 1)
        total_with_discount = calc2.calculate_total(discount=0.1)
        shipping1 = calc.calculate_shipping(110.0)
        shipping2 = calc2.calculate_shipping(99.0)
        self.assertEqual(shipping1, 0.0)
        self.assertGreater(shipping2, 0.0)