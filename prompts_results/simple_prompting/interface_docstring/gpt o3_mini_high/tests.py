import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def test_init_default_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_default_total_items_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_init_default_shipping_free_at_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_init_default_shipping_charges_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(0.0), 10.0)

    def test_init_default_calculate_tax(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(10.0), 10.0 * 0.23)

    def test_init_invalid_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_invalid_type_free_shipping_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_item_typical(self):
        calc = OrderCalculator()
        calc.add_item("apple", 2.0)
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 2.0)
        self.assertEqual(calc.list_items(), ["apple"])

    def test_add_item_with_quantity(self):
        calc = OrderCalculator()
        calc.add_item("banana", 1.5, quantity=3)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 4.5)

    def test_add_same_item_increments_quantity(self):
        calc = OrderCalculator()
        calc.add_item("orange", 1.0)
        calc.add_item("orange", 1.0, quantity=2)
        self.assertEqual(calc.total_items(), 3)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item("pear", 2.0)
        with self.assertRaises(ValueError):
            calc.add_item("pear", 2.5)

    def test_add_item_invalid_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0)

    def test_add_item_invalid_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("melon", 0.0)

    def test_add_item_invalid_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("melon", -1.0)

    def test_add_item_invalid_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("grape", 1.0, quantity=0)

    def test_add_item_invalid_type_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_invalid_type_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("kiwi", "1.0", 1)

    def test_add_item_invalid_type_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("kiwi", 1.0, quantity=1.5)

    def test_remove_item_typical(self):
        calc = OrderCalculator()
        calc.add_item("apple", 2.0)
        calc.remove_item("apple")
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])

    def test_remove_item_not_exist(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("nonexistent")

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_typical(self):
        calc = OrderCalculator()
        calc.add_item("a", 2.0, quantity=2)
        calc.add_item("b", 3.0, quantity=1)
        self.assertEqual(calc.get_subtotal(), 7.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(30.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_discount_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, -0.1)

    def test_apply_discount_invalid_discount_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, 1.1)

    def test_apply_discount_invalid_type_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_apply_discount_invalid_type_discount(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_free(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_typical(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(200.0), 200.0 * 0.23)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-5.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0, quantity=2)
        calc.add_item("b", 2.0, quantity=3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("a", 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_list_items_nonempty(self):
        calc = OrderCalculator()
        calc.add_item("x", 1.0)
        calc.add_item("y", 2.0)
        self.assertCountEqual(calc.list_items(), ["x", "y"])

    def test_is_empty_initial(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding(self):
        calc = OrderCalculator()
        calc.add_item("item", 1.0)
        self.assertFalse(calc.is_empty())

    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("a", 10.0, quantity=2)
        total = calc.calculate_total()
        subtotal = 20.0
        shipping = 0.0
        tax = (subtotal + shipping) * 0.23
        self.assertAlmostEqual(total, subtotal + shipping + tax)

    def test_calculate_total_with_discount_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("a", 60.0, quantity=2)
        total = calc.calculate_total(discount=0.1)
        discounted = 120.0 * 0.9
        shipping = 0.0
        tax = (discounted + shipping) * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_with_discount_requires_shipping(self):
        calc = OrderCalculator()
        calc.add_item("a", 40.0, quantity=2)
        total = calc.calculate_total(discount=0.5)
        discounted = 80.0 * 0.5
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_invalid_discount_negative(self):
        calc = OrderCalculator()
        calc.add_item("a", 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_calculate_total_invalid_discount_high(self):
        calc = OrderCalculator()
        calc.add_item("a", 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=1.1)

    def test_calculate_total_invalid_type_discount(self):
        calc = OrderCalculator()
        calc.add_item("a", 10.0)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount="0.1")

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()


if __name__ == '__main__':
    unittest.main()
