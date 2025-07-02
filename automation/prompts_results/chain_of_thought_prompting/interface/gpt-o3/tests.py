import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):

    # Constructor
    def test_init_defaults(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(100), 23)

    def test_init_custom_parameters(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50, shipping_cost=5)
        self.assertAlmostEqual(oc.calculate_tax(100), 10)
        oc.add_item("item", 40)
        self.assertEqual(oc.calculate_shipping(40), 5)

    def test_init_negative_tax_rate_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_negative_shipping_cost_raises(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    # add_item / remove_item
    def test_add_item_single(self):
        oc = OrderCalculator()
        oc.add_item("apple", 2.0)
        self.assertAlmostEqual(oc.get_subtotal(), 2.0)

    def test_add_item_quantity(self):
        oc = OrderCalculator()
        oc.add_item("banana", 1.5, 3)
        self.assertAlmostEqual(oc.get_subtotal(), 4.5)

    def test_add_item_accumulates_quantity(self):
        oc = OrderCalculator()
        oc.add_item("cookie", 1.0)
        oc.add_item("cookie", 1.0, 2)
        self.assertEqual(oc.total_items(), 3)

    def test_add_item_large_quantity(self):
        oc = OrderCalculator()
        oc.add_item("bulk", 0.1, 10000)
        self.assertAlmostEqual(oc.get_subtotal(), 1000)

    def test_add_item_negative_price_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("bad", -1.0)

    def test_add_item_negative_quantity_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item("bad", 1.0, -2)

    def test_add_item_non_string_name_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0)

    def test_remove_item(self):
        oc = OrderCalculator()
        oc.add_item("milk", 3.0)
        oc.remove_item("milk")
        self.assertTrue(oc.is_empty())

    def test_remove_nonexistent_item_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(KeyError):
            oc.remove_item("ghost")

    # Order state helpers
    def test_is_empty_fresh(self):
        self.assertTrue(OrderCalculator().is_empty())

    def test_is_empty_after_add(self):
        oc = OrderCalculator()
        oc.add_item("egg", 0.2)
        self.assertFalse(oc.is_empty())

    def test_total_items_empty(self):
        self.assertEqual(OrderCalculator().total_items(), 0)

    def test_total_items_multiple_lines(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 2)
        oc.add_item("b", 1.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_list_items_order(self):
        oc = OrderCalculator()
        oc.add_item("x", 1.0)
        oc.add_item("y", 1.0)
        self.assertEqual(oc.list_items(), ["x", "y"])

    def test_list_items_empty_after_clear(self):
        oc = OrderCalculator()
        oc.add_item("z", 1.0)
        oc.clear_order()
        self.assertEqual(oc.list_items(), [])

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item("w", 1.0)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertAlmostEqual(oc.get_subtotal(), 0.0)

    # Monetary helpers
    def test_get_subtotal_multiple_items(self):
        oc = OrderCalculator()
        oc.add_item("a", 1.0, 2)
        oc.add_item("b", 1.5)
        self.assertAlmostEqual(oc.get_subtotal(), 3.5)

    def test_get_subtotal_empty(self):
        self.assertAlmostEqual(OrderCalculator().get_subtotal(), 0.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100, 0), 100)

    def test_apply_discount_positive(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100, 20), 80)

    def test_apply_discount_equal_subtotal(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(50, 50), 0.0)

    def test_apply_discount_greater_than_subtotal_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(50, 60)

    def test_apply_discount_negative_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(50, -5)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_exact_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator()
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_negative_subtotal_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_shipping(-1)

    def test_calculate_tax_positive_amount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(50), 11.5)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.calculate_tax(0), 0)

    def test_calculate_tax_negative_amount_raises(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10)

    # calculate_total
    def test_calculate_total_no_discount(self):
        oc = OrderCalculator()
        oc.add_item("a", 40)
        self.assertAlmostEqual(oc.calculate_total(), 40 + 10 + (40 * 0.23))

    def test_calculate_total_with_discount_below_threshold(self):
        oc = OrderCalculator()
        oc.add_item("a", 40)
        total = oc.calculate_total(discount=10)
        self.assertAlmostEqual(total, 30 + 10 + (30 * 0.23))

    def test_calculate_total_discount_triggers_free_shipping(self):
        oc = OrderCalculator()
        oc.add_item("a", 110)
        total = oc.calculate_total(discount=15)
        discounted = 95
        expected = discounted + 0 + (discounted * 0.23)
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_discount_equal_subtotal(self):
        oc = OrderCalculator()
        oc.add_item("a", 50)
        self.assertAlmostEqual(oc.calculate_total(discount=50), 0)

    def test_calculate_total_empty_cart(self):
        self.assertAlmostEqual(OrderCalculator().calculate_total(), 0)

    def test_calculate_total_negative_discount_raises(self):
        oc = OrderCalculator()
        oc.add_item("a", 10)
        with self.assertRaises(ValueError):
            oc.calculate_total(discount=-1)

    def test_calculate_total_custom_parameters(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=30, shipping_cost=5)
        oc.add_item("a", 20)
        self.assertAlmostEqual(oc.calculate_total(), 20 + 5 + 2)

    def test_calculate_total_precision(self):
        oc = OrderCalculator()
        oc.add_item("small", 0.1, 3)
        expected = 0.3 + 10 + (0.3 * 0.23)
        self.assertAlmostEqual(oc.calculate_total(), expected)

    # State-transition interactions
    def test_chain_add_remove_clear(self):
        oc = OrderCalculator()
        oc.add_item("a", 10)
        oc.add_item("b", 20)
        oc.remove_item("a")
        oc.add_item("c", 5)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertAlmostEqual(oc.calculate_total(), 0)

    def test_two_instances_independent(self):
        oc1 = OrderCalculator()
        oc2 = OrderCalculator()
        oc1.add_item("a", 10)
        self.assertAlmostEqual(oc1.get_subtotal(), 10)
        self.assertAlmostEqual(oc2.get_subtotal(), 0)


if __name__ == "__main__":
    unittest.main()