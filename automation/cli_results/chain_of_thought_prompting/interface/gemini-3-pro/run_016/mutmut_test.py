import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_init_custom_parameters(self):
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_shipping(60.0), 0.0)

    def test_add_item_single_valid(self):
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_custom_quantity(self):
        self.calc.add_item('Banana', 2.0, quantity=5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_multiple_distinct(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_duplicate_name_aggregates(self):
        self.calc.add_item('Apple', 1.0, quantity=1)
        self.calc.add_item('Apple', 1.0, quantity=2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Item', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Item', 10.0, quantity=0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Item', 10.0, quantity=-1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_get_subtotal_mixed_items(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.5)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        cost = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        cost = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        cost = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax_standard(self):
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        tax = self.calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_calculate_total_negative_discount(self):
        self.calc.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-5.0)

    def test_total_items_sum(self):
        self.calc.add_item('A', 10.0, 3)
        self.calc.add_item('B', 10.0, 2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_initial(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_after_add(self):
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())