import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_typical(self):
        self.calculator.add_item('Test Item', 25.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 50.0)
        self.assertIn('Test Item', self.calculator.list_items())

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Single Item', 10.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 10.0)

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', -1.0, 1)

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid', 10.0, -5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Name', '10.0', 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Name', 10.0, 1.5)

    def test_remove_item_success(self):
        self.calculator.add_item('To Remove', 10.0, 1)
        self.calculator.remove_item('To Remove')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_get_subtotal_multiple(self):
        self.calculator.add_item('A', 10.0, 1)
        self.calculator.add_item('B', 20.0, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 50.0)

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -5.0)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 105.0)

    def test_calculate_shipping_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(50.0), 10.0)
        self.assertAlmostEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_total_items_calculation(self):
        self.calculator.add_item('A', 10.0, 3)
        self.calculator.add_item('B', 10.0, 7)
        self.assertEqual(self.calculator.total_items(), 10)

    def test_clear_order_functionality(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(len(self.calculator.list_items()), 0)

    def test_list_items_content(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 2.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Item', 1.0, 1)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())