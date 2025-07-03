import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_basic(self):
        calc = OrderCalculator()
        calc.add_item("Widget", 10.0, 2)
        self.assertEqual(calc.total_items(), 2)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.items, [{"name": "Widget", "price": 10.0, "quantity": 2}])

    def test_add_item_increment(self):
        calc = OrderCalculator()
        calc.add_item("Widget", 10.0, 1)
        calc.add_item("Widget", 10.0, 3)
        self.assertEqual(calc.items[0]["quantity"], 4)

    def test_add_item_same_name_diff_price(self):
        calc = OrderCalculator()
        calc.add_item("Widget", 10.0)
        with self.assertRaises(ValueError):
            calc.add_item("Widget", 12.0)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Widget", "10.0", 1)

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Widget", 10.0, 1.5)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0, 1)

    def test_add_item_negative_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Widget", 10.0, 0)

    def test_add_item_nonpositive_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Widget", 0.0, 1)

    def test_remove_item_basic(self):
        calc = OrderCalculator()
        calc.add_item("Widget", 10.0, 1)
        calc.remove_item("Widget")
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Nonexistent")

    def test_remove_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_basic(self):
        calc = OrderCalculator()
        calc.add_item("A", 5.0, 2)
        calc.add_item("B", 3.0, 3)
        self.assertEqual(calc.get_subtotal(), 5*2 + 3*3)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_basic(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.1")

    def test_apply_discount_invalid_discount_value(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.5)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("100")

    def test_calculate_tax_basic(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("100")

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-50.0)

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item("A", 50.0, 1)
        calc.add_item("B", 25.0, 1)
        total = calc.calculate_total()
        subtotal = 75.0
        shipping = 5.0
        tax = (subtotal + shipping) * 0.1
        self.assertAlmostEqual(total, subtotal + shipping + tax)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=5.0)
        calc.add_item("A", 30.0, 2)
        total = calc.calculate_total(0.1)
        subtotal = 60.0
        discounted = 54.0
        shipping = 5.0
        tax = (discounted + shipping) * 0.2
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item("A", 60.0, 1)
        total = calc.calculate_total()
        discounted = 60.0
        shipping = 0.0
        tax = discounted * 0.1
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_total("0.1")

    def test_calculate_total_invalid_discount_range(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 2)
        calc.add_item("B", 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 1.0, 1)
        calc.add_item("B", 2.0, 1)
        calc.add_item("A", 1.0, 2)
        self.assertCountEqual(calc.list_items(), ["A", "B"])

    def test_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item("A", 1.0, 1)
        self.assertFalse(calc.is_empty())

if __name__ == '__main__':
    unittest.main()