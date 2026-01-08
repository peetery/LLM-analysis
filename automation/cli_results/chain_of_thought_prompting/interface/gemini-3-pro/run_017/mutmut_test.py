import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_init_custom(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(60.0), 0.0)

    def test_init_zero_values(self):
        zero_calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(zero_calc.calculate_tax(100.0), 0.0)
        self.assertEqual(zero_calc.calculate_shipping(100.0), 0.0)

    def test_init_negative_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_multiple_distinct(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Banana', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_accumulation(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        items = self.calc.list_items()
        self.assertEqual(len(items), 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadItem', -1.0, 1)

    def test_add_item_invalid_quantity_zero(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, 0)

    def test_add_item_invalid_quantity_negative(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 1.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_state_transitions(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_total_items_sum(self):
        self.calc.add_item('A', 10.0, 5)
        self.calc.add_item('B', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_get_subtotal_mixed(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 40.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_exact_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(101.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax_standard(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_total_standard_flow(self):
        self.calc.add_item('Item', 50.0, 2)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', '10.0', 1)

    def test_add_item_type_error_quantity(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Item', 10.0, 1.5)