import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_below_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_type_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_basic(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_same_name_and_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 3.0, 2)
        calc.add_item('Orange', 3.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_same_name_different_price_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Grape', 4.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Grape', 5.0, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Pear', -1.0, 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Plum', 0.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Mango', 5.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Kiwi', 2.0, -1)

    def test_add_item_invalid_type_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0, 1)

    def test_add_item_invalid_type_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Peach', '2.0', 1)

    def test_add_item_invalid_type_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Cherry', 3.0, '1')

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Lemon', 1.0, 2)
        calc.remove_item('Lemon')
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        calc.add_item('Lime', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Orange')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        calc.add_item('Coconut', 4.0, 1)
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Watermelon', 10.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Strawberry', 2.0, 5)
        calc.add_item('Blueberry', 3.0, 2)
        self.assertEqual(calc.get_subtotal(), 16.0)

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

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_discount_below_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_invalid_type_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_apply_discount_invalid_type_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_invalid_type(self):
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

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 50.0, 2)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, (100.0 + 10.0) * 1.23)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item2', 100.0, 1)
        total = calc.calculate_total(0.2)
        self.assertEqual(total, 80.0 * 1.23)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item3', 150.0, 1)
        total = calc.calculate_total(0.0)
        self.assertEqual(total, 150.0 * 1.23)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item4', 50.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_invalid_type(self):
        calc = OrderCalculator()
        calc.add_item('Item5', 50.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Tomato', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Potato', 2.0, 3)
        calc.add_item('Carrot', 1.5, 4)
        self.assertEqual(calc.total_items(), 7)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Onion', 1.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Garlic', 0.5, 1)
        self.assertEqual(calc.list_items(), ['Garlic'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Pepper', 2.0, 1)
        calc.add_item('Salt', 1.0, 1)
        items = calc.list_items()
        self.assertIn('Pepper', items)
        self.assertIn('Salt', items)
        self.assertEqual(len(items), 2)

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('Cucumber', 1.5, 2)
        calc.add_item('Cucumber', 1.5, 3)
        items = calc.list_items()
        self.assertEqual(items.count('Cucumber'), 1)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('Lettuce', 2.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Spinach', 3.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Broccoli', 2.5, 1)
        calc.remove_item('Broccoli')
        self.assertTrue(calc.is_empty())