import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
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

    def test_init_invalid_tax_rate_range_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_range_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_item_success(self):
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

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 1.5, 2)
        calc.add_item("Pen", 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["quantity"], 5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0)

    def test_add_item_invalid_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 0.0)

    def test_add_item_invalid_price_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", -10.0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Item", 10.0, 0)

    def test_add_item_price_conflict(self):
        calc = OrderCalculator()
        calc.add_item("Bread", 2.0)
        with self.assertRaises(ValueError):
            calc.add_item("Bread", 2.5)

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

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.add_item("B", 20.0)
        calc.remove_item("A")
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]["name"], "B")

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Nonexistent")

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_success(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 2