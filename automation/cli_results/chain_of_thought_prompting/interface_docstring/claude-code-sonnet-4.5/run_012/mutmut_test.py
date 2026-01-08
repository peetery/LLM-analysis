import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_lower_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_upper_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_non_numeric_tax_rate_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_non_numeric_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_non_numeric_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_none_as_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_add_item_single_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_single_with_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_same_item_twice_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Candy', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Bulk Item', 1.0, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Free Item', 0.0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Item', -1.0)

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

    def test_add_item_non_string_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_non_numeric_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', '1.0')

    def test_add_item_non_integer_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.0, '5')

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Item', 1.0, 2.5)

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_verify_order_state(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_non_string_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_none_as_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 4)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_different_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 1)
        calc.add_item('Item2', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 4)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.5)
        self.assertEqual(result, 50.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.2)

    def test_apply_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_non_numeric_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_non_numeric_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_discounted_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_very_large_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(10000.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_non_numeric_input(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(1000.0)
        self.assertEqual(result, 230.0)

    def test_calculate_tax_non_numeric_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_hundred_percent_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_below_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 50.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount_above_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 150.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 150.0 * 0.8
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total(discount=1.0)
        expected = 10.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_negative(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_above_one(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_non_numeric_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 125.0 * 0.8
        self.assertEqual(discounted, 100.0)
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_just_below_threshold_after_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 124.0, 1)
        total = calc.calculate_total(discount=0.2)
        discounted = 124.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_adding_same_item_twice(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_verify_is_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_verify_subtotal_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.5)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items, ['Apple'])

    def test_is_empty_on_initialization(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add_then_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_complete_order_workflow(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        calc.add_item('Banana', 0.5, 20)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 25.0)
        total = calc.calculate_total(discount=0.2)
        discounted = 25.0 * 0.8
        expected = (discounted + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_multiple_discount_applications(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total1 = calc.calculate_total(discount=0.1)
        total2 = calc.calculate_total(discount=0.2)
        self.assertNotEqual(total1, total2)
        self.assertGreater(total1, total2)

    def test_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_order_with_exactly_free_shipping_threshold(self):
        calc = OrderCalculator()
        calc.add_item('Item', 100.0, 1)
        total = calc.calculate_total()
        expected = 100.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_order_with_multiple_items_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        calc.add_item('Item2', 30.0, 3)
        calc.add_item('Item3', 20.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 210.0)
        total = calc.calculate_total(discount=0.1)
        discounted = 210.0 * 0.9
        expected = discounted * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_single_cheap_item_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Candy', 2.0, 1)
        total = calc.calculate_total()
        expected = (2.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_zero_tax_scenario(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Item', 50.0, 1)
        total = calc.calculate_total()
        expected = 50.0 + 10.0
        self.assertEqual(total, expected)

    def test_very_long_item_name(self):
        calc = OrderCalculator()
        long_name = 'A' * 1000
        calc.add_item(long_name, 1.0)
        self.assertEqual(calc.items[0]['name'], long_name)

    def test_special_characters_in_item_name(self):
        calc = OrderCalculator()
        special_name = 'Ăśbër-ĂŻtÄ™m đź§Ą'
        calc.add_item(special_name, 1.0)
        self.assertEqual(calc.items[0]['name'], special_name)

    def test_floating_point_precision_in_calculations(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.1, 3)
        subtotal = calc.get_subtotal()
        self.assertAlmostEqual(subtotal, 0.3, places=10)

    def test_add_item_multiple_times_vs_single_add_large_quantity(self):
        calc1 = OrderCalculator()
        calc1.add_item('Apple', 1.5, 1)
        calc1.add_item('Apple', 1.5, 1)
        calc1.add_item('Apple', 1.5, 1)
        calc2 = OrderCalculator()
        calc2.add_item('Apple', 1.5, 3)
        self.assertEqual(calc1.get_subtotal(), calc2.get_subtotal())
        self.assertEqual(calc1.total_items(), calc2.total_items())