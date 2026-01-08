import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_valid_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_add_item_valid(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertIn("Apple", self.calc.list_items())

    def test_add_item_increase_quantity(self):
        self.calc.add_item("Apple", 2.0, 5)
        self.calc.add_item("Apple", 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 2.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", -1.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", "2.0", 1)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 2.0, 0)
        with self.assertRaises(TypeError):
            self.calc.add_item("Apple", 2.0, 1.5)

    def test_add_item_different_price_conflict(self):
        self.calc.add_item("Apple", 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Apple", 3.0, 1)

    def test_remove_item_success(self):
        self.calc.add_item("Apple", 2.0, 1)
        self.calc.remove_item("Apple")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("Orange")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item("Apple", 2.0, 2)
        self.calc.add_item("Banana", 3.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 7.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_