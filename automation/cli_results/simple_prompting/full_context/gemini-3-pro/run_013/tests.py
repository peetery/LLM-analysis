import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_different_price_conflict(self):
        self.calculator.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, '5')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)

    def test_remove_item_success(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 2.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_success(self):
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 15.0
        self.assertEqual(self.calculator.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_above_threshold(self):
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 15.0
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('100')

    def test_calculate_tax_success(self):
        self.calculator.tax_rate = 0.2
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 20.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_total_success(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.1), 120.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(), 240.0)

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items(self):
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 5)
        self.calculator.add_item('A', 10)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())