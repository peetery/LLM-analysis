import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_default(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.1")

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_free_shipping_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100.0")

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10.0")

    def test_add_item_valid(self):
        calc = OrderCalculator()
        calc.add_item("apple", 2.5, 3)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 7.5)
        self.assertListEqual(calc.list_items(), ["apple"])

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item("apple", 2.0, 1)
        calc.add_item("apple", 2.0, 2)
        self.assertEqual(calc.total_items(), 3)
        self.assertAlmostEqual(calc.get_subtotal(), 6.0, places=2)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0, 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("banana", 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("banana", -1.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("banana", 1.0, 0)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("banana", 1.0, -1)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("banana", "1.0", 1)

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("banana", 1.0, 1.5)

    def test_add_item_conflicting_price(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("apple", 2.0, 1)

    def test_remove_item_valid(self):
        calc = OrderCalculator()
        calc.add_item("pear", 3.0, 2)
        calc.remove_item("pear")
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("pear")

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, 2)
        calc.add_item("b", 2.5, 4)
        self.assertAlmostEqual(calc.get_subtotal(), 1.0*2 + 2.5*4, places=2)

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        result = calc.apply_discount(200.0, 0.25)
        self.assertAlmostEqual(result, 150.0, places=2)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0, places=2)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_discount_below_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50.0, -0.1)

    def test_apply_discount_discount_above_one(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50.0, 1.1)

    def test_apply_discount_subtotal_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_apply_discount_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_free(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_cost(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50.0")

    def test_calculate_tax_typical(self):
        calc = OrderCalculator(tax_rate=0.23)
        result = calc.calculate_tax(100.0)