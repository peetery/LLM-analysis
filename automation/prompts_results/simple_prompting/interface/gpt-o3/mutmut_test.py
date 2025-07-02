import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = OrderCalculator()

    # __init__, is_empty
    def test_is_empty_initially(self):
        self.assertTrue(self.calc.is_empty())

    def test_custom_init_parameters(self):
        custom = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        custom.add_item("item", 20.0, 2)
        self.assertAlmostEqual(custom.calculate_tax(100.0), 10.0)

    # add_item
    def test_add_item_updates_subtotal(self):
        self.calc.add_item("Book", 15.0, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 30.0)

    def test_add_item_updates_total_items(self):
        self.calc.add_item("Pen", 1.5, 3)
        self.assertEqual(self.calc.total_items(), 3)

    def test_add_multiple_items_list_items(self):
        self.calc.add_item("A", 5.0)
        self.calc.add_item("B", 3.0)
        self.assertCountEqual(self.calc.list_items(), ["A", "B"])

    def test_add_item_invalid_price_raises(self):
        with self.assertRaises(Exception):
            self.calc.add_item("Bad", -1.0, 1)

    def test_add_item_invalid_quantity_raises(self):
        with self.assertRaises(Exception):
            self.calc.add_item("BadQty", 1.0, 0)

    def test_add_item_invalid_name_type_raises(self):
        with self.assertRaises(Exception):
            self.calc.add_item(123, 1.0, 1)  # type: ignore

    # remove_item
    def test_remove_item_success(self):
        self.calc.add_item("Del", 10.0)
        self.calc.remove_item("Del")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent_raises(self):
        with self.assertRaises(Exception):
            self.calc.remove_item("None")

    # get_subtotal
    def test_get_subtotal_no_items_zero(self):
        self.assertAlmostEqual(self.calc.get_subtotal(), 0.0)

    # apply_discount
    def test_apply_discount_typical(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 15.0), 85.0)

    def test_apply_discount_zero_discount(self):
        self.assertAlmostEqual(self.calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_negative_discount_raises(self):
        with self.assertRaises(Exception):
            self.calc.apply_discount(50.0, -5.0)

    # calculate_shipping
    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(80.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calc.calculate_shipping(120.0), 0.0)

    def test_calculate_shipping_negative_subtotal_raises(self):
        with self.assertRaises(Exception):
            self.calc.calculate_shipping(-1.0)

    # calculate_tax
    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises(self):
        with self.assertRaises(Exception):
            self.calc.calculate_tax(-10.0)

    # calculate_total
    def test_calculate_total_no_discount(self):
        self.calc.add_item("Item", 40.0, 3)  # subtotal 120
        expected_total = 120.0  # discounted subtotal
        expected_total += 0.0   # shipping (free)
        expected_total += 120.0 * 0.23  # tax
        self.assertAlmostEqual(self.calc.calculate_total(), expected_total)

    def test_calculate_total_with_discount(self):
        self.calc.add_item("Item", 20.0, 2)  # subtotal 40
        discount = 5.0
        discounted = 35.0
        shipping = 10.0
        tax = (discounted + shipping) * 0.23
        expected_total = discounted + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(discount), expected_total)

    # clear_order, total_items
    def test_clear_order_resets_state(self):
        self.calc.add_item("X", 1.0, 2)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.list_items(), [])


if __name__ == "__main__":
    unittest.main()