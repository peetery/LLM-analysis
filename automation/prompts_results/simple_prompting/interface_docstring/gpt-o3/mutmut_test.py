import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    # __init__
    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)

    def test_init_invalid_tax_rate_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_shipping_cost_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1)

    def test_init_invalid_type_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    # add_item
    def test_add_item_new(self):
        self.calc.add_item("apple", 2.0, 3)
        self.assertIn("apple", self.calc.list_items())

    def test_add_item_existing_increments_quantity(self):
        self.calc.add_item("apple", 2.0, 1)
        self.calc.add_item("apple", 2.0, 2)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_item_same_name_different_price_value_error(self):
        self.calc.add_item("apple", 2.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("apple", 3.0, 1)

    def test_add_item_invalid_price_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("apple", 0, 1)

    def test_add_item_invalid_types_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.0, 1)

    # remove_item
    def test_remove_item_success(self):
        self.calc.add_item("apple", 2.0, 1)
        self.calc.remove_item("apple")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_not_found_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("missing")

    def test_remove_item_invalid_type_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    # get_subtotal
    def test_get_subtotal_correct(self):
        self.calc.add_item("apple", 2.0, 3)
        self.calc.add_item("banana", 1.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 2.0 * 3 + 1.5 * 2)

    def test_get_subtotal_empty_order_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    # apply_discount
    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100, 0.2), 80)

    def test_apply_discount_zero(self):
        self.assertEqual(self.calc.apply_discount(50, 0), 50)

    def test_apply_discount_full_discount(self):
        self.assertEqual(self.calc.apply_discount(50, 1), 0)

    def test_apply_discount_invalid_discount_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50, -0.1)

    def test_apply_discount_negative_subtotal_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-1, 0.1)

    def test_apply_discount_invalid_types_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    # calculate_shipping
    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(150), 0)

    def test_calculate_shipping_cost(self):
        self.assertEqual(self.calc.calculate_shipping(50), 10)

    def test_calculate_shipping_invalid_type_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("50")

    # calculate_tax
    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100), 23)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0), 0)

    def test_calculate_tax_negative_amount_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1)

    def test_calculate_tax_invalid_type_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("100")

    # calculate_total
    def test_calculate_total_no_discount(self):
        self.calc.add_item("book", 20, 3)
        expected_subtotal = 60
        expected_shipping = 10
        expected_tax = (expected_subtotal + expected_shipping) * 0.23
        expected_total = expected_subtotal + expected_shipping + expected_tax
        self.assertAlmostEqual(self.calc.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calc.add_item("book", 20, 3)
        discounted_subtotal = 60 * 0.8
        shipping = 10
        tax = (discounted_subtotal + shipping) * 0.23
        expected_total = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected_total)

    def test_calculate_total_invalid_discount_value_error(self):
        self.calc.add_item("book", 10, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_empty_order_value_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_type_type_error(self):
        self.calc.add_item("book", 10, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.1")

    # total_items
    def test_total_items(self):
        self.calc.add_item("apple", 2.0, 2)
        self.calc.add_item("banana", 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    # clear_order
    def test_clear_order(self):
        self.calc.add_item("apple", 2.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    # list_items
    def test_list_items_unique(self):
        self.calc.add_item("apple", 2.0, 1)
        self.calc.add_item("banana", 1.0, 2)
        self.assertCountEqual(self.calc.list_items(), ["apple", "banana"])

    # is_empty
    def test_is_empty_true_false(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item("apple", 2.0, 1)
        self.assertFalse(self.calc.is_empty())


if __name__ == "__main__":
    unittest.main()