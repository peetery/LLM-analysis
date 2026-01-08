import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_add_item_valid(self):
        self.calc.add_item('Widget', 25.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 50.0)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_default_quantity(self):
        self.calc.add_item('Gadget', 15.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 15.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -1.0, 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('ZeroQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('NegQty', 10.0, -5)

    def test_add_item_wrong_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(None, 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('StringPrice', '10.0', 1)

    def test_remove_item_existing(self):
        self.calc.add_item('Target', 10.0, 1)
        self.calc.remove_item('Target')
        self.assertTrue(self.calc.is_empty())

    def test_get_subtotal_calculation(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 4)
        self.assertEqual(self.calc.get_subtotal(), 40.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_apply_discount_exceeds_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 110.0)

    def test_calculate_shipping_below_limit(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_limit(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_limit(self):
        self.assertEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calc.calculate_tax(50.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_total_items_multiple_entries(self):
        self.calc.add_item('X', 1.0, 5)
        self.calc.add_item('Y', 2.0, 10)
        self.assertEqual(self.calc.total_items(), 15)

    def test_list_items_content(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Orange', 1.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Orange', items)

    def test_is_empty_states(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('NonEmpty', 1.0)
        self.assertFalse(self.calc.is_empty())