import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_with_defaults(self):
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

    def test_init_tax_rate_at_lower_boundary(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_at_upper_boundary(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_zero_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(calc.free_shipping_threshold, 0.0)

    def test_init_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        self.assertEqual(calc.shipping_cost, 0.0)

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_tax_rate_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_free_shipping_threshold_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_init_shipping_cost_as_string(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_tax_rate_as_integer(self):
        calc = OrderCalculator(tax_rate=0)
        self.assertEqual(calc.tax_rate, 0)

    def test_init_free_shipping_threshold_as_integer(self):
        calc = OrderCalculator(free_shipping_threshold=100)
        self.assertEqual(calc.free_shipping_threshold, 100)

    def test_init_shipping_cost_as_integer(self):
        calc = OrderCalculator(shipping_cost=10)
        self.assertEqual(calc.shipping_cost, 10)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_with_specified_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Apple')
        self.assertEqual(calc.items[0]['price'], 1.5)
        self.assertEqual(calc.items[0]['quantity'], 3)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 5)
        self.assertEqual(len(calc.items), 2)

    def test_add_item_with_same_name_and_price_merge(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 5)

    def test_add_item_with_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(calc.items[0]['quantity'], 10)

    def test_add_item_with_same_name_but_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_with_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_with_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0, 1)

    def test_add_item_with_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.5, 1)

    def test_add_item_with_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_with_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, -1)

    def test_add_item_name_as_non_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)

    def test_add_item_price_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)

    def test_add_item_quantity_as_float(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, 1.5)

    def test_add_item_quantity_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '1')

    def test_add_item_with_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1000000)
        self.assertEqual(calc.items[0]['quantity'], 1000000)

    def test_add_item_with_very_small_positive_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 0.01, 1)
        self.assertEqual(calc.items[0]['price'], 0.01)

    def test_remove_existing_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_from_order_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['name'], 'Banana')

    def test_remove_non_existent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_from_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_item_name_as_non_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_remove_merged_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_get_subtotal_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 4)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_get_subtotal_with_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_with_very_large_values(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1000.0, 1000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_no_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full_discount(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_to_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.apply_discount(0.0, 0.5)
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
            calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_discount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    def test_apply_discount_as_integer(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100, 0)
        self.assertEqual(result, 100)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_equal_to_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_on_zero_subtotal(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_discounted_subtotal_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_shipping_just_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_just_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax_on_positive_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 20.0)

    def test_calculate_tax_on_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_amount_as_string(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_tax_with_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_with_one_tax_rate(self):
        calc = OrderCalculator(tax_rate=1.0)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 100.0)

    def test_calculate_total_no_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        self.assertEqual(total, 72.0)

    def test_calculate_total_no_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 15)
        total = calc.calculate_total()
        self.assertEqual(total, 180.0)

    def test_calculate_total_with_discount_with_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=0.1)
        self.assertEqual(total, 66.0)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 60.0)

    def test_calculate_total_with_full_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=1.0)
        self.assertEqual(total, 12.0)

    def test_calculate_total_on_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_discount_as_string(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 5)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.2')

    def test_calculate_total_at_exact_free_shipping_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 10)
        total = calc.calculate_total()
        self.assertEqual(total, 120.0)

    def test_calculate_total_discount_brings_subtotal_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 11)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 130.8, places=2)

    def test_calculate_total_tax_applied_to_discounted_subtotal_plus_shipping(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total(discount=0.2)
        self.assertEqual(total, 62.5)

    def test_total_items_on_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_with_single_item_quantity_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)

    def test_total_items_with_single_item_quantity_greater_than_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_with_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_merging_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_non_empty_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_clear_already_empty_order(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertEqual(len(calc.items), 0)

    def test_is_empty_returns_true_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_on_empty_order(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_with_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_with_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Banana', 0.5, 3)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_with_duplicate_names_merged(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_uniqueness(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        items = calc.list_items()
        self.assertEqual(len(items), 1)

    def test_is_empty_on_new_order(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing_order(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_removing_all_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_workflow_complete_order_lifecycle(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        total = calc.calculate_total()
        self.assertEqual(total, 72.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_workflow_add_remove_add_same_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_workflow_edge_case_at_free_shipping_boundary(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 5)
        shipping = calc.calculate_shipping(calc.get_subtotal())
        self.assertEqual(shipping, 0.0)

    def test_calculation_chain_verification(self):
        calc = OrderCalculator(tax_rate=0.25, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 20.0, 4)
        total = calc.calculate_total(discount=0.25)
        expected_subtotal = 80.0
        expected_discounted = 60.0
        expected_shipping = 10.0
        expected_tax = (60.0 + 10.0) * 0.25
        expected_total = 60.0 + 10.0 + expected_tax
        self.assertEqual(total, expected_total)

    def test_multiple_discounts_scenario(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Apple', 10.0, 10)
        total1 = calc.calculate_total(discount=0.1)
        total2 = calc.calculate_total(discount=0.2)
        self.assertNotEqual(total1, total2)

    def test_state_isolation(self):
        calc1 = OrderCalculator()
        calc2 = OrderCalculator()
        calc1.add_item('Apple', 1.5, 2)
        self.assertEqual(len(calc2.items), 0)

    def test_edge_add_remove_check_total_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 0)

    def test_edge_very_large_order(self):
        calc = OrderCalculator()
        for i in range(100):
            calc.add_item(f'Item{i}', 1.0, 1)
        self.assertEqual(len(calc.items), 100)

    def test_edge_price_with_many_decimal_places(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.123456789, 1)
        self.assertEqual(calc.items[0]['price'], 1.123456789)

    def test_edge_mixed_integer_and_float_prices(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1, 1)
        calc.add_item('Banana', 1.5, 1)
        subtotal = calc.get_subtotal()
        self.assertEqual(subtotal, 2.5)