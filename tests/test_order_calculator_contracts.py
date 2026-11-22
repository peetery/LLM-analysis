import unittest

from order_calculator import OrderCalculator


class TestOrderCalculatorContracts(unittest.TestCase):
    def assert_error(self, exception, message, operation, *args, **kwargs):
        with self.assertRaises(exception) as caught:
            operation(*args, **kwargs)
        self.assertEqual(str(caught.exception), message)

    def test_constructor_defaults_and_boundaries(self):
        default = OrderCalculator()
        self.assertEqual(
            (default.tax_rate, default.free_shipping_threshold, default.shipping_cost),
            (0.23, 100.0, 10.0)
        )
        self.assertTrue(default.is_empty())
        for values in ((0, 0, 0), (1, 50, 5), (0.15, 20, 2.5)):
            with self.subTest(values=values):
                calc = OrderCalculator(*values)
                self.assertEqual(
                    (calc.tax_rate, calc.free_shipping_threshold, calc.shipping_cost), values
                )

    def test_constructor_rejects_types_and_ranges(self):
        cases = [
            ('tax_rate', 'bad', TypeError, 'Tax rate must be a float or int.'),
            ('free_shipping_threshold', None, TypeError,
             'Free shipping threshold must be a float or int.'),
            ('shipping_cost', 'bad', TypeError, 'Shipping cost must be a float or int.'),
            ('tax_rate', -0.01, ValueError, 'Tax rate must be between 0.0 and 1.0.'),
            ('tax_rate', 1.01, ValueError, 'Tax rate must be between 0.0 and 1.0.'),
            ('free_shipping_threshold', -0.01, ValueError,
             'Free shipping threshold cannot be negative.'),
            ('shipping_cost', -0.01, ValueError, 'Shipping cost cannot be negative.')
        ]
        for parameter, value, exception, message in cases:
            with self.subTest(parameter=parameter, value=value):
                self.assert_error(exception, message, OrderCalculator, **{parameter: value})

    def test_add_item_rejects_invalid_inputs(self):
        cases = [
            ((None, 2, 1), TypeError, 'Item name must be a string.'),
            (('apple', None, 1), TypeError, 'Price must be a number.'),
            (('apple', 2, 1.5), TypeError, 'Quantity must be an integer.'),
            (('', 2, 1), ValueError, 'Item name cannot be empty.'),
            (('apple', 0, 1), ValueError, 'Price must be greater than 0.'),
            (('apple', -1, 1), ValueError, 'Price must be greater than 0.'),
            (('apple', 2, 0), ValueError, 'Quantity must be at least 1.'),
            (('apple', 2, -1), ValueError, 'Quantity must be at least 1.')
        ]
        for args, exception, message in cases:
            with self.subTest(args=args):
                calc = OrderCalculator()
                self.assert_error(exception, message, calc.add_item, *args)
                self.assertTrue(calc.is_empty())

    def test_items_merge_only_for_identical_name_and_price(self):
        calc = OrderCalculator()
        calc.add_item('apple', 2)
        calc.add_item('banana', 3, 2)
        calc.add_item('apple', 2, 3)
        self.assertEqual(calc.total_items(), 6)
        self.assertEqual(calc.get_subtotal(), 14)
        self.assertEqual(set(calc.list_items()), {'apple', 'banana'})
        self.assertEqual(len(calc.list_items()), 2)
        self.assertEqual(len(calc.items), 2)
        self.assert_error(
            ValueError, 'Item with the same name but different price already exists.',
            calc.add_item, 'apple', 4
        )
        self.assertEqual(calc.get_subtotal(), 14)
        self.assertEqual(calc.total_items(), 6)

    def test_removal_preserves_other_items_and_reports_missing_names(self):
        calc = OrderCalculator()
        calc.add_item('apple', 2, 3)
        calc.add_item('banana', 5)
        calc.remove_item('apple')
        self.assertEqual(calc.list_items(), ['banana'])
        self.assertEqual(calc.total_items(), 1)
        self.assertEqual(calc.get_subtotal(), 5)
        self.assert_error(
            ValueError, "Item with name 'apple' does not exist in the order.",
            calc.remove_item, 'apple'
        )
        self.assert_error(TypeError, 'Item name must be a string.', calc.remove_item, None)
        calc.remove_item('banana')
        self.assertTrue(calc.is_empty())

    def test_empty_order_and_clear_reset_state(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])
        for operation in (calc.get_subtotal, calc.calculate_total):
            self.assert_error(
                ValueError, 'Cannot calculate subtotal on empty order.', operation
            )
        calc.add_item('apple', 2, 3)
        self.assertFalse(calc.is_empty())
        calc.clear_order()
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)
        self.assertEqual(calc.list_items(), [])
        calc.add_item('banana', 4)
        self.assertEqual(calc.get_subtotal(), 4)

    def test_discount_endpoints_and_fraction(self):
        for subtotal, discount, expected in (
            (0, 0, 0), (0, 1, 0), (80, 0, 80), (80, 1, 0), (80, 0.25, 60)
        ):
            with self.subTest(subtotal=subtotal, discount=discount):
                self.assertAlmostEqual(
                    OrderCalculator().apply_discount(subtotal, discount), expected
                )

    def test_discount_errors_distinguish_types_and_ranges(self):
        cases = [
            (('bad', 0), TypeError, 'Subtotal must be a number.'),
            ((10, None), TypeError, 'Discount must be a number.'),
            ((10, -0.01), ValueError, 'Discount must be between 0.0 and 1.0.'),
            ((10, 1.01), ValueError, 'Discount must be between 0.0 and 1.0.'),
            ((-0.01, 0), ValueError, 'Cannot apply discount on negative subtotal.')
        ]
        for args, exception, message in cases:
            with self.subTest(args=args):
                self.assert_error(
                    exception, message, OrderCalculator().apply_discount, *args
                )

    def test_shipping_uses_configured_threshold_including_equality(self):
        calc = OrderCalculator(free_shipping_threshold=20, shipping_cost=3)
        for subtotal, expected in ((0, 3), (19.99, 3), (20, 0), (20.01, 0)):
            with self.subTest(subtotal=subtotal):
                self.assertEqual(calc.calculate_shipping(subtotal), expected)
        self.assertEqual(
            OrderCalculator(free_shipping_threshold=0).calculate_shipping(0), 0
        )
        self.assert_error(
            TypeError, 'Discounted subtotal must be a number.',
            calc.calculate_shipping, None
        )

    def test_tax_uses_configured_rate_and_rejects_invalid_amounts(self):
        for rate, amount, expected in ((0, 40, 0), (1, 40, 40), (0.15, 40, 6), (0.23, 0, 0)):
            with self.subTest(rate=rate, amount=amount):
                self.assertAlmostEqual(OrderCalculator(tax_rate=rate).calculate_tax(amount), expected)
        calc = OrderCalculator()
        self.assert_error(TypeError, 'Amount must be a number.', calc.calculate_tax, None)
        self.assert_error(
            ValueError, 'Cannot calculate tax on negative amount.', calc.calculate_tax, -0.01
        )

    def test_total_taxes_shipping_and_uses_post_discount_threshold(self):
        cases = [
            ((0.23, 100, 10), 10, 0, 24.6),
            ((0.23, 100, 10), 10, 0.1, 23.37),
            ((0.23, 100, 10), 100, 0, 123),
            ((0.23, 100, 10), 100, 0.1, 123),
            ((0.23, 100, 10), 10, 1, 12.3),
            ((0, 100, 10), 10, 0.5, 15),
            ((0.15, 20, 3), 25, 0.2, 23),
            ((0.15, 20, 3), 25, 0.4, 20.7)
        ]
        for parameters, subtotal, discount, expected in cases:
            with self.subTest(parameters=parameters, subtotal=subtotal, discount=discount):
                calc = OrderCalculator(*parameters)
                calc.add_item('apple', subtotal)
                self.assertAlmostEqual(calc.calculate_total(discount), expected)
                self.assertEqual(calc.get_subtotal(), subtotal)
                self.assertEqual(calc.total_items(), 1)
        calc = OrderCalculator()
        calc.add_item('apple', 100)
        self.assertAlmostEqual(calc.calculate_total(), 123)

    def test_total_rejects_invalid_discount_without_changing_order(self):
        for discount, exception, message in (
            (None, TypeError, 'Discount must be a number.'),
            (-0.01, ValueError, 'Discount must be between 0.0 and 1.0.'),
            (1.01, ValueError, 'Discount must be between 0.0 and 1.0.')
        ):
            with self.subTest(discount=discount):
                calc = OrderCalculator()
                calc.add_item('apple', 2)
                self.assert_error(exception, message, calc.calculate_total, discount)
                self.assertEqual(calc.get_subtotal(), 2)


if __name__ == '__main__':
    unittest.main()
