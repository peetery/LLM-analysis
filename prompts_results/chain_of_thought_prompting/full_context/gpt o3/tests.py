import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def _create_example_order(self):
        oc = OrderCalculator()
        oc.add_item("A", 2.0, 3)  # 6.0
        oc.add_item("B", 5.0, 1)  # 5.0
        return oc

    # __init__
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.items, [])
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=1.0, free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(oc.tax_rate, 1.0)
        self.assertEqual(oc.free_shipping_threshold, 0.0)
        self.assertEqual(oc.shipping_cost, 0.0)

    def test_init_invalid_tax_rate(self):
        for rate in (-0.1, 1.1):
            with self.assertRaises(ValueError):
                OrderCalculator(tax_rate=rate)

    def test_init_negative_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[])
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost={})

    # add_item
    def test_add_item_first(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.5, 2)
        self.assertEqual(oc.total_items(), 2)

    def test_add_item_second_distinct(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.5, 1)
        oc.add_item("Notebook", 3.0, 1)
        self.assertEqual(len(oc.items), 2)

    def test_add_item_merge_duplicate(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.5, 2)
        oc.add_item("Pen", 1.5, 3)
        self.assertEqual(oc.total_items(), 5)
        self.assertEqual(len(oc.items), 1)

    def test_add_item_duplicate_different_price(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.5, 1)
        with self.assertRaises(ValueError):
            oc.add_item("Pen", 2.0, 1)

    def test_add_item_quantity_one(self):
        oc = OrderCalculator()
        oc.add_item("Single", 2.5)
        self.assertEqual(oc.total_items(), 1)

    def test_add_item_value_errors(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("", 1.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item("BadPrice", 0, 1)
        with self.assertRaises(ValueError):
            oc.add_item("BadQty", 1.0, 0)

    def test_add_item_type_errors(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0, 1)
        with self.assertRaises(TypeError):
            oc.add_item("Bad", "1.0", 1)
        with self.assertRaises(TypeError):
            oc.add_item("Bad", 1.0, 1.5)

    # remove_item
    def test_remove_item_existing(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.0, 1)
        oc.remove_item("Pen")
        self.assertNotIn("Pen", oc.list_items())

    def test_remove_item_last(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1.0, 1)
        oc.remove_item("Pen")
        self.assertTrue(oc.is_empty())

    def test_remove_item_not_present(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item("Ghost")

    def test_remove_item_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    # get_subtotal
    def test_get_subtotal_multiple_items(self):
        oc = self._create_example_order()
        self.assertAlmostEqual(oc.get_subtotal(), 11.0, places=2)

    def test_get_subtotal_single_item(self):
        oc = OrderCalculator()
        oc.add_item("Solo", 4.0, 2)
        self.assertAlmostEqual(oc.get_subtotal(), 8.0, places=2)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    # apply_discount
    def test_apply_discount_normal(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100, 0.2), 80.0, places=2)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100, 0), 100.0, places=2)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100, 1), 0.0, places=2)

    def test_apply_discount_invalid_rate(self):
        oc = OrderCalculator()
        for rate in (-0.1, 1.1):
            with self.assertRaises(ValueError):
                oc.apply_discount(100, rate)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10, 0.1)

    def test_apply_discount_type_errors(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount("100", 0.1)
        with self.assertRaises(TypeError):
            oc.apply_discount(100, "0.1")

    # calculate_shipping
    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=50, shipping_cost=8)
        self.assertEqual(oc.calculate_shipping(30), 8)

    def test_calculate_shipping_equal_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=50, shipping_cost=8)
        self.assertEqual(oc.calculate_shipping(50), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=50, shipping_cost=8)
        self.assertEqual(oc.calculate_shipping(60), 0.0)

    def test_calculate_shipping_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping("30")

    # calculate_tax
    def test_calculate_tax_positive(self):
        oc = OrderCalculator(tax_rate=0.23)
        self.assertAlmostEqual(oc.calculate_tax(100), 23.0, places=2)

    def test_calculate_tax_zero(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(0), 0)

    def test_calculate_tax_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-1)

    def test_calculate_tax_type_error(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax("100")

    # calculate_total
    def test_calculate_total_happy_path(self):
        oc = OrderCalculator()
        oc.add_item("A", 30, 1)
        oc.add_item("B", 40, 1)
        total = oc.calculate_total(0.1)
        self.assertAlmostEqual(total, 89.79, places=2)

    def test_calculate_total_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 60, 2)  # subtotal 120
        total = oc.calculate_total(0.1)  # discounted 108 >= 100 so free shipping
        expected = 108 + 108 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item("A", 50, 2)  # subtotal 100, free shipping
        total = oc.calculate_total(0)
        expected = 100 + 100 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_full_discount_but_shipping(self):
        oc = OrderCalculator()
        oc.add_item("A", 30, 1)
        total = oc.calculate_total(1)
        expected = 10 + 10 * 0.23
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_type_error_discount(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_total("0.1")

    def test_calculate_total_invalid_discount_value(self):
        oc = OrderCalculator()
        oc.add_item("A", 10, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(1.5)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total(0.1)

    # total_items
    def test_total_items_sum(self):
        oc = OrderCalculator()
        oc.add_item("A", 1, 2)
        oc.add_item("A", 1, 3)
        oc.add_item("B", 1, 1)
        self.assertEqual(oc.total_items(), 6)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    # clear_order
    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item("A", 1, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.total_items(), 0)

    # list_items
    def test_list_items_unique(self):
        oc = OrderCalculator()
        oc.add_item("Pen", 1, 1)
        oc.add_item("Pen", 1, 2)
        oc.add_item("Book", 2, 1)
        self.assertCountEqual(oc.list_items(), ["Pen", "Book"])

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    # is_empty
    def test_is_empty_new(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_add(self):
        oc = OrderCalculator()
        oc.add_item("A", 1, 1)
        self.assertFalse(oc.is_empty())

    def test_is_empty_after_clear(self):
        oc = OrderCalculator()
        oc.add_item("A", 1, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())


if __name__ == "__main__":
    unittest.main()
