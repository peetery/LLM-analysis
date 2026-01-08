import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_boundary_low(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_boundary_high(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc.tax_rate, 1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_init_tax_rate_out_of_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calc.add_item("Apple", 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Apple")
        self.assertEqual(self.calc.items[0]["price"], 1.5)
        self.assertEqual(self.calc.items[0]["quantity"], 10)

    def test_add_item_quantity_increase(self):
        self.calc.add_item("Apple", 1.5, 10)
        self.calc.add_item("Apple", 1.5, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 15)

    def test_add_item_price_conflict(self):
        self.calc.add_item("Apple", 1.5, 10)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0, 5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "1.5")
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 1.5, "10")

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 1.5)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 1.5, 0)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 1.5)
        self.calc.remove_item("Apple")