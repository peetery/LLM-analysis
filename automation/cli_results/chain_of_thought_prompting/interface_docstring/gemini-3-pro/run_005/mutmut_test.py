import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertIsInstance(calc, OrderCalculator)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_boundary_tax_rate(self):
        calc_0 = OrderCalculator(tax_rate=0.0)
        calc_1 = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_0.calculate_tax(100.0), 0.0)
        self.assertEqual(calc_1.calculate_tax(100.0), 100.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        self.assertEqual(calc.total_items(), 2)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_existing_update_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_explicit_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadPrice', 0.0)
        with self.assertRaises(ValueError):
            calc.add_item('BadPrice', -5.0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('BadQty', 1.0, 0)
        with self.assertRaises(ValueError):
            calc.add_item('BadQty', 1.0, -1)

    def test_add_item_price_conflict(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            calc.add_item('ItemA', 12.0)

    def test_add_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            calc.add_item('Item', '10.0')

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Ghost')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_normal(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_normal(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

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

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50.0')

    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_normal(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertEqual(calc.calculate_total(discount=0.0), 72.0)

    def test_calculate_total_default_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertEqual(calc.calculate_total(), 72.0)

    def test_calculate_total_with_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=50.0)
        calc.add_item('ExpensiveItem', 150.0, 1)
        self.assertEqual(calc.calculate_total(), 165.0)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.5)

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 20.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10.0)
        calc.add_item('B', 20.0)
        calc.add_item('A', 10.0)
        items = calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_state_changes(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('A', 1.0)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.clear_order()
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])
        with self.assertRaises(ValueError):
            calc.get_subtotal()