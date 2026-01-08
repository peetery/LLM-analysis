import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_typical(self):
        self.calculator.add_item("Apple", 2.5, 4)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Apple")
        self.assertEqual(self.calculator.items[0]["quantity"], 4)

    def test_add_item_increase_quantity(self):
        self.calculator.add_item("Apple", 2.5, 4)
        self.calculator.add_item("Apple", 2.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 6)

    def test_add_item_different_price_same_name_raises_error(self):
        self.calculator.add_item("Apple", 2.5, 4)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 3.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 2.5, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 0, 1)
        with self```python
import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    # --- __init__ tests ---
    def test_init_default_values(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    # --- add_item tests ---
    def test_add_item_success(self):
        self.calc.add_item("Apple", 2.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Apple")
        self.assertEqual(self.calc.items[0]["price"], 2.5)
        self.assertEqual(self.calc.items[0]["quantity"], 3)

    def test_add_item_increase_quantity(self):
        self.calc.add_item("Apple", 2.5, 3)
        self.calc.add_item("Apple", 2.5, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 5)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.5)
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "2.5")
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 2.5, 1.5)

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 2.5)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.5, 0)

    def test_add_item_different_price_error(self):
        self.calc.add_item("Apple", 2.5, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 3.0, 1)

    # --- remove_item tests ---
    def test_remove_item_success(self):
        self.calc.add_item("Apple", 2.5)
        self.calc.remove_item("Apple")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non