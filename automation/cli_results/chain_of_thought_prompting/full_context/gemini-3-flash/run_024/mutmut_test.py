import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_default_params(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_params(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item("Laptop", 1000.0, 1)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "Laptop")
        self.assertEqual(calc.items[0]["price"], 1000.0)
        self.assertEqual(calc.items[0]["quantity"], 1)

    def test_add_item_merge_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Mouse", 25.0, 1)
        calc.add_item("Mouse", 25.0, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["quantity"], 3)

    def test_add_item_price_conflict(self):
        calc = OrderCalculator()
        calc.add_item("Mouse", 25.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Mouse", 30.0, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0, 1)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Item", -1.0, 1)

    def test_add_item_invalid