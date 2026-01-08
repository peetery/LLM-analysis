import unittest
from order_calculator import OrderCalculator

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

    def test_init_tax_rate_as_int(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

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

    def test_init_tax_rate_boundary_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_boundary_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_add_item_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_same_name_and_price_increases_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Orange', 2.0, 2)
        calc.add_item('Orange', 2.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_same_name_different_price_raises_error(self):
        calc = OrderCalculator()
        calc.add_item('Grape', 3.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Grape', 4.0, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Mango', '1.5', 1)

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Peach', 1.5, 1.5)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Pear', 1.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Plum', 1.0, -1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Cherry', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Kiwi', -1.0, 1)

    def test_add_item_price_as_int(self):
        calc = OrderCalculator()
        calc.add_item('Watermelon', 5, 1)
        self.assertEqual(calc.items[0]['price'], 5)

    def test_remove_item_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Lemon', 0.8, 2)
        calc.remove_item('Lemon')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_nonexistent_item(self):
        calc = OrderCalculator()
        calc.add_item('Lime', 0.7, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Orange')

    def test_remove_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_item_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Strawberry', 2.0, 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Blueberry', 3.0, 2)
        calc.add_item('Raspberry', 4.0, 1)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_discount_below_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_discount_above_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_subtotal_as_int(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0.1)
        self.assertEqual(result, 90.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('150')

    def test_calculate_shipping_discounted_subtotal_as_int(self):
        calc = OrderCalculator()
        shipping = calc.calculate_shipping(50)
        self.assertEqual(shipping, 10.0)

    def test_calculate_tax_valid_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_amount_as_int(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(100)
        self.assertEqual(tax, 23.0)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item1', 20.0, 2)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 61.5, places=2)

    def test_calculate_total_with_discount_with_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item2', 30.0, 2)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 75.9, places=2)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item3', 50.0, 3)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 184.5, places=2)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item('Item4', 60.0, 2)
        total = calc.calculate_total(discount=0.2)
        self.assertAlmostEqual(total, 118.08, places=2)

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item('Item5', 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_discount_as_int(self):
        calc = OrderCalculator()
        calc.add_item('Item6', 200.0, 1)
        total = calc.calculate_total(discount=0)
        self.assertAlmostEqual(total, 246.0, places=2)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item7', 5.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item8', 5.0, 2)
        calc.add_item('Item9', 10.0, 4)
        self.assertEqual(calc.total_items(), 6)

    def test_total_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('Item10', 5.0, 1)
        calc.add_item('Item11', 10.0, 2)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_already_empty(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Item12', 5.0, 1)
        self.assertEqual(calc.list_items(), ['Item12'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Item13', 5.0, 1)
        calc.add_item('Item14', 10.0, 1)
        items = calc.list_items()
        self.assertEqual(set(items), {'Item13', 'Item14'})

    def test_list_items_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('Item15', 5.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Item16', 5.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_complex_scenario_multiple_operations(self):
        calc = OrderCalculator()
        calc.add_item('Product1', 25.0, 2)
        calc.add_item('Product2', 15.0, 3)
        calc.add_item('Product1', 25.0, 1)
        self.assertEqual(calc.total_items(), 6)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 120.0)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 145.98, places=2)
        calc.remove_item('Product2')
        self.assertEqual(calc.total_items(), 3)

    def test_free_shipping_threshold_edge_case(self):
        calc = OrderCalculator(free_shipping_threshold=100.0)
        calc.add_item('Product3', 50.0, 2)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 123.0, places=2)

    def test_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        calc.add_item('Product4', 50.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 60.0)

    def test_max_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        calc.add_item('Product5', 50.0, 1)
        total = calc.calculate_total()
        self.assertEqual(total, 120.0)

    def test_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        calc.add_item('Product6', 50.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 61.5, places=2)