import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_valid_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 20.0)
        self.assertEqual(calc.calculate_shipping(20.0), 5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_tax_rate_boundary_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_init_tax_rate_boundary_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.calculate_tax(100.0), 100.0)

    def test_init_tax_rate_out_of_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_out_of_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertIn('Apple', calc.list_items())
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_with_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5, 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_duplicate_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 1)

    def test_add_item_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.5, 1)
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.5', 1)
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.5, '1')

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0, 2)
        calc.add_item('Banana', 2.0, 3)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_success(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_boundaries(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_range(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_integration(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 66.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.5), 110.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items_count(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.add_item('B', 1.0, 5)
        self.assertEqual(calc.total_items(), 6)

    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 2.0, 1)
        names = calc.list_items()
        self.assertEqual(len(names), 2)
        self.assertIn('A', names)
        self.assertIn('B', names)

    def test_is_empty_state_transitions(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('A', 1.0, 1)
        self.assertFalse(calc.is_empty())
        calc.remove_item('A')
        self.assertTrue(calc.is_empty())

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.add_item('B', 2.0, 2)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
if __name__ == '__main__':
    unittest.main()