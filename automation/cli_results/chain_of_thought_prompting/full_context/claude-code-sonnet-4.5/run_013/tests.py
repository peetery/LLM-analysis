import unittest
from order_calculator import OrderCalculator, Item

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
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

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_init_items_list_empty(self):
        calc = OrderCalculator()
        self.assertIsInstance(calc.items, list)
        self.assertEqual(len(calc.items), 0)

    def test_init_tax_rate_not_numeric(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_not_numeric(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_not_numeric(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_free_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_single_custom_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5, 5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.5)
        calc.add_item('Cherry', 2.0)
        self.assertEqual(len(calc.items), 3)

    def test_add_item_duplicate_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2, 1)
        self.assertEqual(calc.items[0]['price'], 2)

    def test_add_item_very_small_price(self):
        calc = OrderCalculator()
        calc.add_item('Gum', 0.01)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Rice', 10.0, 1000)
        self.assertEqual(calc.items[0]['quantity'], 1000)

    def test_add_item_whitespace_name(self):
        calc = OrderCalculator()
        calc.add_item('  Bread  ', 2.5)
        self.assertEqual(calc.items[0]['name'], '  Bread  ')

    def test_add_item_name_not_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5)

    def test_add_item_price_not_numeric(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5')

    def test_add_item_quantity_not_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_remove_item_exists(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_one_of_many(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.add_item('Banana', 0.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_item_all_quantities_removed(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_name_not_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_not_exists(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_get_subtotal_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.get_subtotal(), 1.5)

    def test_get_subtotal_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 4)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_correct_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 10.0, 2)
        calc.add_item('Item2', 5.0, 3)
        expected = 10.0 * 2 + 5.0 * 3
        self.assertEqual(calc.get_subtotal(), expected)

    def test_get_subtotal_floating_point(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.33, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 0.99, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_integer_inputs(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_apply_discount_calculation_accuracy(self):
        calc = OrderCalculator()
        subtotal = 123.45
        discount = 0.15
        expected = subtotal * (1 - discount)
        self.assertAlmostEqual(calc.apply_discount(subtotal, discount), expected, places=2)

    def test_apply_discount_subtotal_not_numeric(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_not_numeric(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_integer_input(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        result = calc.calculate_shipping(50)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_not_numeric(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_integer_input(self):
        calc = OrderCalculator(tax_rate=0.2)
        result = calc.calculate_tax(100)
        self.assertEqual(result, 20.0)

    def test_calculate_tax_calculation_accuracy(self):
        calc = OrderCalculator(tax_rate=0.23)
        amount = 87.65
        expected = amount * 0.23
        self.assertAlmostEqual(calc.calculate_tax(amount), expected, places=2)

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_not_numeric(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(0.1)
        discounted = 100.0 * 0.9
        expected = discounted + 10.0 + (discounted + 10.0) * 0.2
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_triggered(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 150.0)
        total = calc.calculate_total()
        expected = 150.0 + 0.0 + 150.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_shipping_charged(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 60.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_multiple_items(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item('Item1', 30.0, 2)
        calc.add_item('Item2', 20.0, 1)
        total = calc.calculate_total(0.0)
        subtotal = 80.0
        shipping = 5.0
        tax = (subtotal + shipping) * 0.1
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_calculation_flow(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Product', 50.0, 2)
        total = calc.calculate_total(0.2)
        subtotal = 100.0
        discounted = subtotal * 0.8
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_integer_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=200.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total(0)
        expected = 100.0 + 10.0 + 110.0 * 0.2
        self.assertEqual(total, expected)

    def test_calculate_total_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0)
        total = calc.calculate_total()
        expected = 50.0 + 10.0 + 0.0
        self.assertEqual(total, expected)

    def test_calculate_total_discount_not_numeric(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_single_item_multiple_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items_various_quantities(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.5, 2)
        calc.add_item('Cherry', 2.0, 5)
        self.assertEqual(calc.total_items(), 10)

    def test_total_items_after_add_and_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        calc.add_item('Banana', 0.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 2)

    def test_clear_order_non_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_items_list_empty(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertEqual(calc.items, [])

    def test_clear_order_then_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        calc.add_item('Banana', 0.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

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
        calc.add_item('Banana', 0.5)
        calc.add_item('Cherry', 2.0)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertIn('Cherry', items)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], 'Apple')

    def test_list_items_returns_list_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        items = calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], str)

    def test_is_empty_initial_state(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complete_order_flow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 40.0, 2)
        calc.add_item('Item2', 30.0, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 110.0)
        total = calc.calculate_total(0.1)
        discounted = 110.0 * 0.9
        shipping = 0.0
        tax = discounted * 0.1
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_multiple_discounts_not_cumulative(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total1 = calc.calculate_total(0.1)
        total2 = calc.calculate_total(0.2)
        self.assertNotEqual(total1, total2)

    def test_order_with_only_free_shipping_items(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_order_just_below_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 99.99)
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_large_order_calculation(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=1000.0, shipping_cost=50.0)
        calc.add_item('Item1', 100.0, 10)
        calc.add_item('Item2', 50.0, 20)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 2000.0)
        total = calc.calculate_total(0.0)
        expected = 2000.0 + 0.0 + 2000.0 * 0.2
        self.assertEqual(total, expected)

    def test_floating_point_precision_in_total(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 33.33, 3)
        total = calc.calculate_total(0.15)
        subtotal = 99.99
        discounted = subtotal * 0.85
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected, places=2)

    def test_state_consistency_after_exceptions(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        try:
            calc.add_item('Apple', 2.0)
        except ValueError:
            pass
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['price'], 1.5)

    def test_items_structure_correct(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        item = calc.items[0]
        self.assertIn('name', item)
        self.assertIn('price', item)
        self.assertIn('quantity', item)
        self.assertEqual(item['name'], 'Apple')
        self.assertEqual(item['price'], 1.5)
        self.assertEqual(item['quantity'], 2)

    def test_items_list_type(self):
        calc = OrderCalculator()
        self.assertIsInstance(calc.items, list)