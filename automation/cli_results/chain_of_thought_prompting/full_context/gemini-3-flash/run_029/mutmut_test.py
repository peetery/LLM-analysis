import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertEqual(oc.items, [])

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_tax_rate_boundary_low(self):
        oc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(oc.tax_rate, 0.0)

    def test_init_tax_rate_boundary_high(self):
        oc = OrderCalculator(tax_rate=1.0)
        self.assertEqual(oc.tax_rate, 1.0)

    def test_init_threshold_boundary(self):
        oc = OrderCalculator(free_shipping_threshold=0.0)
        self.assertEqual(oc.free_shipping_threshold, 0.0)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error_tax(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_type_error_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_type_error_shipping(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_success(self):
        oc = OrderCalculator()
        oc.add_item("Laptop", 1000.0, 1)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]["name"], "Laptop")

    def test_add_item_multiple(self):
        oc = OrderCalculator()
        oc.add_item("Mouse", 25.0, 2)
        oc.add_item("Keyboard", 50.0, 1)
        self.assertEqual(len(oc.items), 2)

    def test_add_item_update_quantity(self):
        oc = OrderCalculator()
        oc.add_item("Mouse", 25.0, 1)
        oc.add_item("Mouse", 25.0, 2)
        self.assertEqual(len(oc.items), 1)
        self.assertEqual(oc.items[0]["quantity"], 3)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 10.0, 1)

    def test_add_item_zero_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("Freebie", 0.0, 1)

    def test_add_item_negative_price(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("Bad", -5.0, 1)

    def test_add_item_invalid_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("Item", 10.0, 0)

    def test_add_item_price_conflict(self):
        oc = OrderCalculator()
        oc.add_item("Mouse", 25.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item("Mouse", 30.0, 1)

    def test_add_item_type_error_name(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 10.0, 1)

    def test_add_item_type_error_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("Item", "10.0", 1)

    def test_add_item_type_error_quantity(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item("Item", 10.0, 1.5)

    def test_remove_item_success(self):
        oc = OrderCalculator()
        oc.add_item("Mouse", 25.0, 1)
        oc.remove_item("Mouse")
        self.assertEqual(len(oc.items), 0)

    def test_remove_item_non_existent(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item("Ghost")

    def test_remove_item_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(None)

    def test_get_subtotal_success(self):
        oc = OrderCalculator()
        oc.add_item("Mouse", 25.0, 2)
        oc.add_item("Keyboard", 50.0, 1