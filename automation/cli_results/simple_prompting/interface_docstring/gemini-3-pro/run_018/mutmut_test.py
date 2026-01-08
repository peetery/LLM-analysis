import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_valid_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_valid_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')

    def test_add_item_valid(self):
        self.calc.add_item('Widget', 10.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Widget', 10.0, 1)
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, -1)

    def test_add_item_price_mismatch(self):
        self.calc.add_item('Widget', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 15.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10.0')

    def test_remove_item_valid(self):
        self.calc.add_item('Widget', 10.0)
        self.calc.remove_item('Widget')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_boundaries(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_custom_config(self):
        custom_calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(custom_calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_standard(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 123.0)

    def test_calculate_total_with_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.5)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.1')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_sum(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 20.0)
        self.calc.add_item('A', 10.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty_true(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        self.calc.add_item('A', 10.0)
        self.assertFalse(self.calc.is_empty())