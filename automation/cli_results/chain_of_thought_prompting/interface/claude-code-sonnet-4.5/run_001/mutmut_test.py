import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(100), 23.0)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(30), 5.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_zero_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100), 0.0)

    def test_init_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_add_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.get_subtotal(), 1.0)

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_multiple_different_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 0.5, 3)
        self.assertEqual(calc.get_subtotal(), 3.5)

    def test_add_duplicate_item_same_name(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Apple', 1.0, 3)
        self.assertEqual(calc.get_subtotal(), 5.0)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, -1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_float_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 1.5)

    def test_add_item_very_large_price(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 10000000000.0, 1)
        self.assertEqual(calc.get_subtotal(), 10000000000.0)

    def test_add_item_very_large_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1000000)
        self.assertEqual(calc.get_subtotal(), 1000000.0)

    def test_remove_item_from_empty_cart(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Apple')

    def test_remove_nonexistent_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('')

    def test_remove_all_items_one_by_one(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 0.5, 1)
        calc.remove_item('Apple')
        calc.remove_item('Banana')
        self.assertTrue(calc.is_empty())

    def test_get_subtotal_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 6.0)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 9.0)

    def test_get_subtotal_after_adding_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.get_subtotal(), 1.0)
        calc.add_item('Banana', 2.0, 1)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_get_subtotal_after_removing_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 2.0, 1)
        calc.remove_item('Apple')
        self.assertEqual(calc.get_subtotal(), 2.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -10.0)

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

    def test_calculate_shipping_zero_subtotal(self):
        calc = OrderCalculator()
        result = calc.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_with_zero_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_with_zero_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=0.0)
        result = calc.calculate_shipping(50.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_normal(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-100.0)

    def test_calculate_tax_custom_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        result = calc.calculate_tax(100.0)
        self.assertEqual(result, 15.0)

    def test_calculate_tax_very_large_amount(self):
        calc = OrderCalculator()
        result = calc.calculate_tax(10000000000.0)
        self.assertEqual(result, 10000000000.0 * 0.23)

    def test_calculate_total_single_item_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        total = calc.calculate_total()
        expected = (10.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_eligible(self):
        calc = OrderCalculator()
        calc.add_item('Expensive', 150.0, 1)
        total = calc.calculate_total()
        expected = 150.0 * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_free_shipping_not_eligible(self):
        calc = OrderCalculator()
        calc.add_item('Cheap', 50.0, 1)
        total = calc.calculate_total()
        expected = (50.0 + 10.0) * 1.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_negative_discount(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-10.0)

    def test_calculate_total_zero_discount_default(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 50.0, 1)
        total1 = calc.calculate_total()
        total2 = calc.calculate_total(discount=0.0)
        self.assertEqual(total1, total2)

    def test_calculate_total_all_zero_rates(self):
        calc = OrderCalculator(tax_rate=0.0, shipping_cost=0.0)
        calc.add_item('Apple', 100.0, 1)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 100.0)

    def test_total_items_empty_cart(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 3)
        calc.add_item('Banana', 1.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        self.assertEqual(calc.total_items(), 2)
        calc.add_item('Banana', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 1.0, 3)
        calc.remove_item('Apple')
        self.assertEqual(calc.total_items(), 3)

    def test_total_items_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order_empty_cart(self):
        calc = OrderCalculator()
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_with_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.add_item('Banana', 2.0, 3)
        calc.clear_order()
        self.assertEqual(len(calc.list_items()), 0)

    def test_clear_order_is_empty_becomes_true(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order_total_items_becomes_zero(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 10)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty_cart(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_single_item(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertEqual(calc.list_items(), ['Apple'])

    def test_list_items_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 1.0, 1)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_order_preserved(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 1.0, 1)
        calc.add_item('Cherry', 1.0, 1)
        items = calc.list_items()
        self.assertEqual(len(items), 3)

    def test_list_items_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertIn('Apple', calc.list_items())
        calc.add_item('Banana', 1.0, 1)
        self.assertIn('Banana', calc.list_items())

    def test_list_items_after_remove(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.add_item('Banana', 1.0, 1)
        calc.remove_item('Apple')
        items = calc.list_items()
        self.assertNotIn('Apple', items)
        self.assertIn('Banana', items)

    def test_list_items_returns_copy(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        items = calc.list_items()
        items.append('Banana')
        self.assertEqual(len(calc.list_items()), 1)

    def test_is_empty_new_cart(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_remove_all(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 5)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_workflow_add_remove_add(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 1)
        calc.add_item('Banana', 20.0, 1)
        calc.remove_item('Apple')
        calc.add_item('Cherry', 30.0, 1)
        self.assertEqual(calc.get_subtotal(), 50.0)

    def test_workflow_edge_case_chain(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('Apple', 1.0, 1)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_state_consistency(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 10.0, 2)
        calc.add_item('Banana', 5.0, 3)
        self.assertEqual(calc.get_subtotal(), 35.0)
        self.assertEqual(calc.total_items(), 5)
        self.assertFalse(calc.is_empty())
        self.assertEqual(len(calc.list_items()), 2)

    def test_rounding_precision(self):
        calc = OrderCalculator()
        calc.add_item('Item', 0.99, 1)
        total = calc.calculate_total()
        self.assertIsInstance(total, float)

    def test_immutability_of_parameters(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        calc.calculate_total()
        self.assertEqual(calc.calculate_tax(100.0), 23.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_add_item_wrong_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'ten', 1)

    def test_apply_discount_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, 'ten')

    def test_calculate_shipping_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('fifty')

    def test_calculate_tax_wrong_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('hundred')

    def test_calculate_total_wrong_type(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 100.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='ten')