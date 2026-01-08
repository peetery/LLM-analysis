import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.get_subtotal_base_tax_rate(), 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.08, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item("Item", 10.0)
        self.assertEqual(calc.calculate_tax(100.0), 8.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_tax_rate_out_of_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_costs(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-10.0)

    def test_add_item_new(self):
        self.calculator.add_item("Apple", 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertIn("Apple", self.calculator.list_items())

    def test_add_item_increment_quantity(self):
        self.calculator.add_item("Apple", 2.0, 5)
        self.calculator.add_item("Apple", 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)
        self.assertEqual(len(self.calculator.list_items()), 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 2.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", "2.0")
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", 2.0, "1")

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 2.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0, -1)

    def test_add_item_price_mismatch(self):
        self.calculator.add_item("