import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test', 40.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_tax(100.0), 5.0)

    def test_add_item_normal(self):
        self.calc.add_item('Apple', 1.5, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_quantity(self):
        self.calc.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_accumulation(self):
        self.calc.add_item('Orange', 1.0, 2)
        self.calc.add_item('Orange', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 5.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Gold', -100.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Silver', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Silver', 10.0, -1)

    def test_remove_item(self):
        self.calc.add_item('Apple', 1.0, 3)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost Item')

    def test_is_empty_new(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_modification(self):
        self.calc.add_item('Pen', 2.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    def test_total_items_mixed(self):
        self.calc.add_item('Pencil', 1.0, 2)
        self.calc.add_item('Eraser', 0.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        self.calc.add_item('Book', 15.0)
        self.calc.add_item('Pen', 2.0)
        items = self.calc.list_items()
        self.assertIn('Book', items)
        self.assertIn('Pen', items)
        self.assertEqual(len(items), 2)

    def test_get_subtotal_normal(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calc.calculate_shipping(99.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calc.calculate_shipping(101.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_boundary(self):
        shipping = self.calc.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Expensive Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)