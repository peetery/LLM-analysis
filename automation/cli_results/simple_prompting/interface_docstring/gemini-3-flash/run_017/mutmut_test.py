import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_init_defaults(self):
        default_calc = OrderCalculator()
        self.assertTrue(default_calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(0.1, 50.0, 5.0)
        self.assertTrue(calc.is_empty())

    def test_init_raises_value_error_for_tax_rate_out_of_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_raises_value_error_for_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_raises_value_error_for_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_raises_type_error_for_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_add_item_success(self):
        self.calc.add_item("Laptop", 1000.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertIn("Laptop", self.calc.list_items())

    def test_add_item_increases_quantity_for_same_name_and_price(self):
        self.calc.add_item("Mouse", 20.0, 1)
        self.calc.add_item("Mouse", 20.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_raises_value_error_for_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 10.0, 1)

    def test_add_item_raises_value_error_for_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Item", 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Item", -1.0, 1)

    def test_add_item_raises_value_error_for_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Item", 10.0, 0)

    def test_add_item_raises_value_error_for_conflicting_price(self):
        self.calc.add_item("Item", 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Item", 15.0, 1)

    def test_add_item_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_remove_item_success(self):
        self.calc.add_item("Item", 10.0, 1)
        self.calc.remove_item("Item")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_raises_value_error_if_not_exists(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("NonExistent")

    def test_remove_item_raises_type_error_if_not_string(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item("A", 10.0, 2)
        self.calc.add_item("B", 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_raises_value_error_when_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_raises_value_error_for_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_raises_value_