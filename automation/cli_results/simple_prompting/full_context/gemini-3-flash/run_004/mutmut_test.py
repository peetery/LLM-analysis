import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_type_errors(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_value_errors(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        self.calc.add_item("Apple", 2.5, 4)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {"name": "Apple", "price": 2.5, "quantity": 4})

    def test_add_item_existing_same_price(self):
        self.calc.add_item("Apple", 2.5, 4)
        self.calc.add_item("Apple", 2.5, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["quantity"], 6)

    def test_add_item_existing_different_price(self):
        self.calc.add_item("Apple", 2.5, 4)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 3.0, 1)

    def test_add_item_type_errors(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.5)
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "2.5")
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 2.5, 2.5)

    def test_add_item_value_errors(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 2.5)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.5, 0)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 2.5)
        self.calc.add_item("Banana", 1.5)
        self.calc.remove_item("Apple")
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]["name"], "Banana")

    def test_