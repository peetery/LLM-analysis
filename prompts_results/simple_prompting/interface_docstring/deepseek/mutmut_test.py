import unittest
from typing import List
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_params(self):
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)

    def test_init_custom_params(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.1")

    def test_init_invalid_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100.0")

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10.0")

    def test_add_item(self):
        self.calculator.add_item("Apple", 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 2)

    def test_add_item_duplicate(self):
        self.calculator.add_item("Apple", 1.0, 2)
        self.calculator.add_item("Apple", 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_duplicate_different_price(self):
        self.calculator.add_item("Apple", 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 2.0)

    def test_add_item_invalid_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", -1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", "1.0")

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Apple", 1.0, 0)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Apple", 1.0, "2")

    def test_remove_item(self):
        self.calculator.add_item("Apple", 1.0)
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Apple")

    def test_remove_item_invalid_name(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal(self):
        self.calculator.add_item("Apple", 1.0, 2)
        self.calculator.add_item("Banana", 0.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 3.5)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.1), 90.0)

    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-1.0, 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100.0", 0.1)

    def test_apply_discount_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "0.1")

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_not_free(self):
        self.assertEqual(self.calculator.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_invalid_input(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("100.0")

    def test_calculate_tax(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("100.0")

    def test_calculate_total(self):
        self.calculator.add_item("Apple", 1.0, 100)
        total = 100.0 * (1 - 0.0) + 0.0  # subtotal - discount + shipping
        total_with_tax = total + total * 0.23
        self.assertEqual(self.calculator.calculate_total(), total_with_tax)

    # def test_calculate_total_with_discount(self):
    #     self.calculator.add_item("Apple", 1.0, 100)
    #     total = 100.0 * (1 - 0.1) + 0.0  # subtotal - discount + shipping
    #     total_with_tax = total + total * 0.23
    #     self.assertEqual(self.calculator.calculate_total(0.1), total_with_tax)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item("Apple", 1.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("0.1")

    def test_total_items(self):
        self.calculator.add_item("Apple", 1.0, 2)
        self.calculator.add_item("Banana", 0.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item("Apple", 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_list_items(self):
        self.calculator.add_item("Apple", 1.0)
        self.calculator.add_item("Banana", 0.5)
        self.assertEqual(set(self.calculator.list_items()), {"Apple", "Banana"})

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item("Apple", 1.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.remove_item("Apple")
        self.assertTrue(self.calculator.is_empty())