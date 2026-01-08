import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_init_tax_rate_value_error_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_value_error_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_shipping_cost_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_normal(self):
        calc = OrderCalculator()
        calc.add_item("Laptop", 1000.0, 2)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "Laptop")
        self.assertEqual(calc.items[0]["price"], 1000.0)
        self.assertEqual(calc.items[0]["quantity"], 2)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Mouse", 25.0)
        self.assertEqual(calc.items[0]["quantity"], 1)

    def test_add_item_update_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 1.0, 5)
        calc.add_item("Pen", 1.0, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["quantity"], 8)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Item", "10.0")

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Item", 10.0, 1.5)

    def test_add_item_empty_name_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0)

    def test_add_item_invalid_price_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 0)

    def test_add_item_invalid_quantity_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 10.0, 0)

    def test_add_item_price_conflict_error(self):
        calc = OrderCalculator()
        calc.add_item("Item", 10.0)
        with self.assertRaises(ValueError):
            calc.add_item("Item", 15.0)

    def test_remove_item_normal(self):
        calc = OrderCalculator()
        calc.add_item("Item1", 10.0)
        calc.add_item("Item2", 20.0)
        calc.remove_item("Item1")
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "Item2")

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_remove_item_not_found_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("NonExistent")

    def test_get_subtotal_normal(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 2)
        calc.add_item("B", 5.0, 1)
        self.assertEqual(calc.get_subtotal(), 25.0)