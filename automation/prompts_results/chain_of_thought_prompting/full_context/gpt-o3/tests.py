import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    # __init__
    def test_init_defaults_valid(self):
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.15, free_shipping_threshold=50, shipping_cost=5)
        self.assertEqual((calc.tax_rate, calc.free_shipping_threshold, calc.shipping_cost), (0.15, 50, 5))

    def test_init_invalid_tax_rate_below_zero(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_tax_rate_above_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_invalid_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-0.01)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_invalid_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_invalid_shipping_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    # add_item
    def test_add_item_fresh(self):
        self.calc.add_item("Book", 10.0, 2)
        self.assertEqual(self.calc.total_items(), 2)

    def test_add_item_duplicate_same_price_increments(self):
        self.calc.add_item("Pen", 2.0, 1)
        self.calc.add_item("Pen", 2.0, 3)
        self.assertEqual(self.calc.total_items(), 4)

    def test_add_item_duplicate_different_price_error(self):
        self.calc.add_item("Notebook", 5.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Notebook", 6.0)

    def test_add_item_empty_name_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("", 1.0)

    def test_add_item_price_zero_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Eraser", 0.0)

    def test_add_item_price_negative_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Eraser", -1.0)

    def test_add_item_quantity_zero_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Stapler", 3.0, 0)

    def test_add_item_quantity_negative_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item("Stapler", 3.0, -1)

    def test_add_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)

    def test_add_item_price_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Glue", "1.0")

    def test_add_item_quantity_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item("Glue", 1.0, 1.5)

    # remove_item
    def test_remove_item_existing(self):
        self.calc.add_item("Clip", 1.0)
        self.calc.remove_item("Clip")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent_error(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item("Ghost")

    def test_remove_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    # get_subtotal
    def test_get_subtotal_multiple_items(self):
        self.calc.add_item("A", 2.0, 2)
        self.calc.add_item("B", 3.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 7.0, places=2)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    # apply_discount
    def test_apply_discount_standard(self):
        self.assertAlmostEqual(self.calc.apply_discount(100, 0.2), 80.0, places=2)

    def test_apply_discount_zero(self):
        self.assertAlmostEqual(self.calc.apply_discount(50, 0.0), 50.0, places=2)

    def test_apply_discount_full(self):
        self.assertAlmostEqual(self.calc.apply_discount(50, 1.0), 0.0, places=2)

    def test_apply_discount_discount_negative_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50, -0.1)

    def test_apply_discount_discount_above_one_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(50, 1.1)

    def test_apply_discount_subtotal_negative_error(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10, 0.2)

    def test_apply_discount_subtotal_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount("50", 0.2)

    def test_apply_discount_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(50, "0.2")

    # calculate_shipping
    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150), 0.0)

    def test_calculate_shipping_equal_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100), 0.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_zero(self):
        self.assertEqual(self.calc.calculate_shipping(0), 10.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("50")

    # calculate_tax
    def test_calculate_tax_standard(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100), 23.0, places=2)

    def test_calculate_tax_zero(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0), 0.0, places=2)

    def test_calculate_tax_negative_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("10")

    # calculate_total
    def test_calculate_total_no_discount_with_shipping(self):
        self.calc.add_item("X", 40, 2)
        total = self.calc.calculate_total()
        expected = 90 + 20.7
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_free_shipping(self):
        self.calc.add_item("Y", 60, 2)
        total = self.calc.calculate_total(0.1)
        discounted = 120 * 0.9
        expected = discounted + discounted * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_discount_triggers_shipping(self):
        self.calc.add_item("Z", 60, 2)
        total = self.calc.calculate_total(0.3)
        discounted = 120 * 0.7
        expected = discounted + 10 + (discounted + 10) * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_full_discount(self):
        self.calc.add_item("W", 50, 1)
        total = self.calc.calculate_total(1)
        expected = 10 + 10 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_discount_negative_error(self):
        self.calc.add_item("A", 10)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(-0.1)

    def test_calculate_total_discount_above_one_error(self):
        self.calc.add_item("A", 10)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(1.1)

    def test_calculate_total_discount_type_error(self):
        self.calc.add_item("A", 10)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.2")

    # total_items
    def test_total_items_counts(self):
        self.calc.add_item("A", 1, 3)
        self.calc.add_item("B", 2, 2)
        self.assertEqual(self.calc.total_items(), 5)

    def test_total_items_zero_when_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    # clear_order
    def test_clear_order(self):
        self.calc.add_item("A", 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    # list_items
    def test_list_items_unique(self):
        self.calc.add_item("A", 1)
        self.calc.add_item("A", 1)
        self.calc.add_item("B", 1)
        self.assertSetEqual(set(self.calc.list_items()), {"A", "B"})

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    # is_empty
    def test_is_empty_true_on_new(self):
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false_after_add(self):
        self.calc.add_item("A", 1)
        self.assertFalse(self.calc.is_empty())

    def test_is_empty_true_after_clear(self):
        self.calc.add_item("A", 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    # integration
    def test_add_remove_total_flow(self):
        self.calc.add_item("A", 10)
        self.calc.remove_item("A")
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_complex_order_total(self):
        self.calc.add_item("A", 30, 2)
        self.calc.add_item("B", 20, 1)
        subtotal = 80
        discounted = subtotal * 0.85
        shipping = 0
        tax = discounted * 0.23
        expected = discounted + tax
        total = self.calc.calculate_total(0.15)
        self.assertAlmostEqual(total, expected, places=2)


if __name__ == "__main__":
    unittest.main()