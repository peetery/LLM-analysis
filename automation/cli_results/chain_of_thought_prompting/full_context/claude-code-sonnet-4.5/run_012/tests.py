import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_valid_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_valid_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_maximum_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_tax_rate_below_minimum(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_maximum(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_tax_rate_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_tax_rate_none(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate=None)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_free_shipping_threshold_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_shipping_cost_wrong_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_duplicate_same_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_then_add_more_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2.5, quantity=2)
        calc.add_item('Orange', 2.5, quantity=3)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_with_float_price(self):
        calc = OrderCalculator()
        calc.add_item('Grapes', 9.99)
        self.assertEqual(calc.items[0]['price'], 9.99)

    def test_add_item_with_int_price(self):
        calc = OrderCalculator()
        calc.add_item('Watermelon', 10)
        self.assertEqual(calc.items[0]['price'], 10)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_name_not_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_price_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, quantity=-1)

    def test_add_item_quantity_as_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, quantity=1.5)

    def test_add_item_quantity_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, quantity='2')

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        calc.remove_item('Banana')
        self.assertEqual(len(calc.items), 2)
        self.assertNotIn('Banana', [item['name'] for item in calc.items])

    def test_remove_item_with_merged_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=3)
        calc.add_item('Apple', 1.5, quantity=2)
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

    def test_remove_item_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_empty_string(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_large_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, quantity=100)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_get_subtotal_decimal_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 9.99, quantity=1)
        calc.add_item('Banana', 12.49, quantity=2)
        self.assertAlmostEqual(calc.get_subtotal(), 34.97, places=2)

    def test_get_subtotal_after_merging_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, quantity=3)
        calc.add_item('Apple', 2.0, quantity=2)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_twenty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_fifty_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(200.0, 0.5)
        self.assertEqual(result, 100.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_integer_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_below_minimum(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_above_maximum(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.2)

    def test_apply_discount_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_subtotal_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_exactly_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_large_discounted_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(10000.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('150')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_hundred_percent_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_calculate_tax_decimal_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        tax = calc.calculate_tax(99.99)
        self.assertAlmostEqual(tax, 22.9977, places=4)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator(tax_rate=0.23)
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_amount_wrong_type(self):
        calc = OrderCalculator(tax_rate=0.23)
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_twenty_percent_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 80.0
        shipping = 10.0
        tax = (80.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 150.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = 150.0 + 0.0 + 150.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_not_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, quantity=1)
        total = calc.calculate_total(discount=0.0)
        expected = 50.0 + 10.0 + 60.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_hundred_percent_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, quantity=1)
        total = calc.calculate_total(discount=1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_multiple_items(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 20.0, quantity=2)
        calc.add_item('Banana', 30.0, quantity=1)
        calc.add_item('Cherry', 10.0, quantity=3)
        total = calc.calculate_total(discount=0.0)
        subtotal = 40.0 + 30.0 + 30.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_exactly_at_threshold_after_discount(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 125.0, quantity=1)
        total = calc.calculate_total(discount=0.2)
        discounted = 100.0
        shipping = 0.0
        tax = 100.0 * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_discount_wrong_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_quantity_five(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Banana', 2.0, quantity=3)
        calc.add_item('Cherry', 3.0, quantity=1)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_after_merging_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_then_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_then_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.add_item('Cherry', 3.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_duplicate_merged(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, quantity=2)
        calc.add_item('Apple', 1.5, quantity=3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Apple')

    def test_list_items_correct_names(self):
        calc = OrderCalculator()
        calc.add_item('Mango', 5.0)
        calc.add_item('Pineapple', 7.5)
        items = calc.list_items()
        self.assertIn('Mango', items)
        self.assertIn('Pineapple', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 2.0)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_complete_order_flow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, quantity=2)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 100.0)
        discounted = calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 90.0)
        total = calc.calculate_total(discount=0.1)
        expected = 90.0 + 10.0 + 100.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_add_again(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        calc.add_item('Banana', 2.0)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_multiple_discount_calculations(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 100.0, quantity=1)
        total1 = calc.calculate_total(discount=0.1)
        total2 = calc.calculate_total(discount=0.2)
        self.assertNotEqual(total1, total2)

    def test_free_shipping_boundary(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 110.0, quantity=1)
        total = calc.calculate_total(discount=0.1)
        discounted = 99.0
        shipping = 10.0
        tax = (99.0 + 10.0) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_tax_on_shipping_only(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 50.0, quantity=1)
        total = calc.calculate_total(discount=1.0)
        expected = 0.0 + 10.0 + 10.0 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_large_order_stress_test(self):
        calc = OrderCalculator()
        for i in range(50):
            calc.add_item(f'Item{i}', float(i + 1), quantity=i + 1)
        self.assertEqual(len(calc.items), 50)
        subtotal = calc.get_subtotal()
        self.assertGreater(subtotal, 0)

    def test_floating_point_precision(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 9.99, quantity=1)
        calc.add_item('Banana', 12.49, quantity=2)
        total = calc.calculate_total(discount=0.0)
        self.assertIsInstance(total, float)

    def test_items_list_independence(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Apple', 1.5)
        self.assertEqual(len(calc1.items), 1)
        self.assertEqual(len(calc2.items), 0)

    def test_item_quantity_accumulation(self):
        calc = OrderCalculator()
        for _ in range(5):
            calc.add_item('Apple', 1.0, quantity=1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_remove_then_calculate(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, quantity=1)
        calc.add_item('Banana', 20.0, quantity=1)
        calc.add_item('Cherry', 30.0, quantity=1)
        calc.remove_item('Banana')
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 40.0)

    def test_error_message_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError) as context:
            calc.add_item('Apple', 2.0)
        self.assertIn('same name', str(context.exception).lower())

    def test_error_message_non_existent_removal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError) as context:
            calc.remove_item('Banana')
        self.assertIn('Banana', str(context.exception))

    def test_value_error_messages_descriptive(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError) as context:
            calc.add_item('', 1.5)
        self.assertIn('empty', str(context.exception).lower())