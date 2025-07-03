import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    # __init__ tests
    def test_init_default(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_tax_rate_value_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_value_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    # add_item tests
    def test_add_item_typical(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 3.0)

    def test_add_item_increment_quantity(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.0, 1)
        calc.add_item('apple', 1.0, 2)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0, 1)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0, 1)

    def test_add_item_invalid_price_value(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('apple', 0.0, 1)

    def test_add_item_invalid_quantity_value(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('apple', 1.0, 0)

    def test_add_item_invalid_quantity_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('apple', 1.0, '2')

    def test_add_item_same_name_different_price(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('apple', 2.0, 1)

    # remove_item tests
    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('banana', 2.0, 1)
        calc.remove_item('banana')
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('orange')

    def test_remove_item_invalid_name_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    # get_subtotal tests
    def test_get_subtotal_multiple(self):
        calc = OrderCalculator()
        calc.add_item('a', 2.0, 2)
        calc.add_item('b', 3.0, 1)
        self.assertEqual(calc.get_subtotal(), 7.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    # apply_discount tests
    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertEqual(calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.5)

    def test_apply_discount_invalid_discount_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, -0.1)

    def test_apply_discount_invalid_discount_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(10.0, 1.1)

    def test_apply_discount_invalid_subtotal_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_discount_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.2')

    # calculate_shipping tests
    def test_calculate_shipping_free(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_cost(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    # calculate_tax tests
    def test_calculate_tax_typical(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(100.0), 23.0, places=7)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-5.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    # calculate_total tests
    def test_calculate_total_no_discount(self):
        calc = OrderCalculator()
        calc.add_item('x', 10.0, 1)
        total = calc.calculate_total()
        expected = 10.0 + 10.0 + (20.0 * 0.23)  # subtotal + shipping + tax
        self.assertAlmostEqual(total, expected, places=7)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator()
        calc.add_item('y', 50.0, 1)
        total = calc.calculate_total(0.5)
        discounted = 25.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax, places=7)

    def test_calculate_total_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item('z', 5.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_calculate_total_invalid_discount_value(self):
        calc = OrderCalculator()
        calc.add_item('z', 5.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    # total_items tests
    def test_total_items_nonempty(self):
        calc = OrderCalculator()
        calc.add_item('a', 1.0, 2)
        calc.add_item('b', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    # clear_order tests
    def test_clear_order_clears(self):
        calc = OrderCalculator()
        calc.add_item('a', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    # list_items tests
    def test_list_items_nonempty(self):
        calc = OrderCalculator()
        calc.add_item('apple', 1.0, 1)
        calc.add_item('banana', 2.0, 1)
        self.assertCountEqual(calc.list_items(), ['apple', 'banana'])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    # is_empty tests
    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('item', 1.0, 1)
        self.assertFalse(calc.is_empty())


if __name__ == '__main__':
    unittest.main()