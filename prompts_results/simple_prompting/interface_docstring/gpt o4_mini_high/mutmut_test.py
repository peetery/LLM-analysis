import unittest

from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-5.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_errors(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_item_typical(self):
        calc = OrderCalculator()
        calc.add_item("apple", 1.0, 3)
        self.assertEqual(calc.get_subtotal(), 3.0)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item("banana", 2.0)
        self.assertEqual(calc.get_subtotal(), 2.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_increase_quantity(self):
        calc = OrderCalculator()
        calc.add_item("milk", 1.5, 2)
        calc.add_item("milk", 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.get_subtotal(), 7.5)

    def test_add_item_conflicting_price(self):
        calc = OrderCalculator()
        calc.add_item("bread", 2.0)
        with self.assertRaises(ValueError):
            calc.add_item("bread", 2.5)

    def test_add_item_invalid_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0, 1)
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item", 0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("item", -1.0, 1)
        with self.assertRaises(TypeError):
            calc.add_item("item", "1.0", 1)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("item", 1.0, 0)
        with self.assertRaises(ValueError):
            calc.add_item("item", 1.0, -2)
        with self.assertRaises(TypeError):
            calc.add_item("item", 1.0, "1")

    def test_remove_item_typical(self):
        calc = OrderCalculator()
        calc.add_item("toy", 5.0, 2)
        calc.remove_item("toy")
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("nonexistent")

    def test_remove_item_invalid_name(self):
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
        self.assertEqual(calc.get_subtotal(), 1.0*2 + 2.5*4)

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_edge(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, 1.1)
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_typical(self):
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)

    def test_calculate_shipping_invalid(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_typical(self):
        calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-5.0)
        with self.assertRaises(TypeError):
            calc.calculate_tax("100")

    def test_calculate_total_typical(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item("x", 20.0, 3)
        total = calc.calculate_total()
        subtotal = 20.0*3
        shipping = 10.0
        tax = (subtotal + shipping)*0.1
        self.assertEqual(total, subtotal + shipping + tax)

    # def test_calculate_total_with_discount_free_shipping(self):
    #     calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
    #     calc.add_item("y", 30.0, 2)
    #     total = calc.calculate_total(discount=0.5)
    #     discounted = (30.0*2)*0.5
    #     shipping = 0.0
    #     tax = (discounted + shipping)*0.2
    #     self.assertEqual(total, discounted + shipping + tax)

    def test_calculate_total_errors(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_total(discount="0.1")
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.1)
        calc2 = OrderCalculator()
        with self.assertRaises(ValueError):
            calc2.calculate_total()

    def test_total_items_and_list_and_clear(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])
        calc.add_item("p", 1.0, 2)
        calc.add_item("q", 2.0, 3)
        self.assertEqual(calc.total_items(), 5)
        names = calc.list_items()
        self.assertCountEqual(names, ["p", "q"])
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item("z", 1.0)
        self.assertFalse(calc.is_empty())


if __name__ == "__main__":
    unittest.main()
