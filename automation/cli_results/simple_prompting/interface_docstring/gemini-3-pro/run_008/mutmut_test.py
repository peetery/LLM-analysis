import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_success(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_accumulate_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 7.5)

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_conflict(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_success(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.2)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_custom_config(self):
        custom_calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(custom_calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_custom_rate(self):
        custom_calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_invalid_value(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_simple(self):
        self.calc.add_item('Item1', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Item1', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item1', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.5), 123.0)

    def test_calculate_total_with_discount_triggering_shipping(self):
        self.calc.add_item('Item1', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.1)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 20.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())