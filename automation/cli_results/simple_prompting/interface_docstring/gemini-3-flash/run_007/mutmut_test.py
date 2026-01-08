import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-0.01)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_standard(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Widget', self.calc.list_items())

    def test_add_item_increase_quantity_existing(self):
        self.calc.add_item('Widget', 10.0, 2)
        self.calc.add_item('Widget', 10.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', -5.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 10.0, -2)

    def test_add_item_different_price_error(self):
        self.calc.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Widget', 12.0, 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', '10', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Widget', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Widget', 10.0, 1)
        self.calc.remove_item('Widget')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_in_order(self):
        self.calc.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Gadget')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 42.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.25), 75.0)

    def test_apply_discount_zero_and_full(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-1.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.01)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.01)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, None)

    def test_calculate_shipping_logic(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('high')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax({'amount': 10})

    def test_calculate_total_no_discount(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 123.0)

    def test_calculate_total_with_discount_and_shipping(self):
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.2), 110.7)

    def test_calculate_total_empty_order_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total(0.1)

    def test_calculate_total_invalid_discount_value(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('0.2')

    def test_total_items_count(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 10, 1)
        self.assertEqual(self.calc.total_items(), 3)

    def test_clear_order_removes_all(self):
        self.calc.add_item('A', 10, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique_names(self):
        self.calc.add_item('Apple', 1.0, 1)
        self.calc.add_item('Orange', 2.0, 1)
        self.calc.add_item('Apple', 1.0, 5)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertSetEqual(set(items), {'Apple', 'Orange'})

    def test_is_empty_functionality(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0, 1)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Item')
        self.assertTrue(self.calc.is_empty())