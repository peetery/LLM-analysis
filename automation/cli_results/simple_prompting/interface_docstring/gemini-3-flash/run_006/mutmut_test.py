import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_success(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(self.calc.total_items(), 15)

    def test_add_item_different_price_raises_value_error(self):
        self.calc.add_item('Apple', 1.5, 10)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 5)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.5, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, -5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, '1')

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
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
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_success(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Widget', 80.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.5), 60.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Widget', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_type(self):
        self.calc.add_item('Widget', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='high')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items_unique(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Banana', 2.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.0, 1)
        self.assertFalse(self.calc.is_empty())