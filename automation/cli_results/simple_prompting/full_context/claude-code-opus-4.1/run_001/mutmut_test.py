import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_boundary_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_boundary_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

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

    def test_init_integer_parameters(self):
        calc = OrderCalculator(tax_rate=0, free_shipping_threshold=100, shipping_cost=10)
        self.assertEqual(calc.tax_rate, 0)
        self.assertEqual(calc.free_shipping_threshold, 100)
        self.assertEqual(calc.shipping_cost, 10)

    def test_add_item_basic(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Book')
        self.assertEqual(calc.items[0]['price'], 25.99)
        self.assertEqual(calc.items[0]['quantity'], 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Pen', 1.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_same_name_same_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Book', 25.99, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        calc.add_item('Pen', 1.5, 2)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_same_name_different_price_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Book', 30.0, 1)

    def test_add_item_name_not_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_price_not_number(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Book', '25.99', 1)

    def test_add_item_quantity_not_integer(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Book', 25.99, 2.5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 25.99, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 25.99, -1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', 0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Book', -10.0, 1)

    def test_add_item_integer_price(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25, 1)
        self.assertEqual(calc.items[0]['price'], 25)

    def test_remove_item_basic(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Pen', 1.5, 3)
        calc.remove_item('Book')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Pen')

    def test_remove_item_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        calc.remove_item('Book')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Pen')

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Book')

    def test_remove_item_name_not_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        self.assertAlmostEqual(calc.get_subtotal(), 51.98, places=2)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Pen', 1.5, 3)
        self.assertAlmostEqual(calc.get_subtotal(), 56.48, places=2)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_single_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        self.assertEqual(calc.get_subtotal(), 100.0)

    def test_apply_discount_basic(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0, places=2)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_subtotal_not_number(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_not_number(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_negative_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_integer_inputs(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_calculate_shipping_free_shipping(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(99.99)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_exactly_threshold(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_custom_threshold_and_cost(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        result = calc.calculate_shipping(49.99)
        self.assertEqual(result, 5.0)

    def test_calculate_shipping_input_not_number(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_shipping_integer_input(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(50)
        self.assertEqual(result, 10.0)

    def test_calculate_tax_basic(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0, places=2)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertAlmostEqual(result, 15.0, places=2)

    def test_calculate_tax_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_full_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 100.0)

    def test_calculate_tax_input_not_number(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_integer_input(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100)
        self.assertEqual(result, 23.0)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Book', 125.0, 1)
        total = calc.calculate_total(discount=0.2)
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_not_number(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        total = calc.calculate_total(discount=1.0)
        self.assertAlmostEqual(total, 12.3, places=2)

    def test_calculate_total_integer_discount(self):
        calc = OrderCalculator()
        calc.add_item('Book', 100.0, 1)
        total = calc.calculate_total(discount=0)
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Pen', 1.5, 5)
        self.assertEqual(calc.total_items(), 7)

    def test_total_items_after_adding_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Book', 25.99, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Pen', 1.5, 3)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_order_preserves_settings(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50.0)
        calc.add_item('Book', 25.99, 1)
        calc.clear_order()
        self.assertEqual(calc.tax_rate, 0.15)
        self.assertEqual(calc.free_shipping_threshold, 50.0)

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Book', items)

    def test_list_items_multiple_unique_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        calc.add_item('Pen', 1.5, 2)
        calc.add_item('Notebook', 5.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)
        self.assertIn('Book', items)
        self.assertIn('Pen', items)
        self.assertIn('Notebook', items)

    def test_list_items_no_duplicates_when_quantity_increased(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 2)
        calc.add_item('Book', 25.99, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Book', items)

    def test_is_empty_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Book', 25.99, 1)
        calc.remove_item('Book')
        self.assertTrue(calc.is_empty())