import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_add_item_typical(self):
        self.calc.add_item("Apple", 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertIn("Apple", self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item("Apple", 1.5, 5)
        self.calc.add_item("Apple", 1.5, 5)
        self.assertEqual(self.calc.total_items(), 10)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 1.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 1.0, 0)

    def test_add_item_conflicting_price(self):
        self.calc.add_item("Apple", 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0)

    def test_add_item_type_error_name(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_add_item_type_error_price(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "1.0")

    def test_remove_item_typical(self):
        self.calc.add_item("Apple", 1.0)
        self.calc.remove_item("Apple")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):