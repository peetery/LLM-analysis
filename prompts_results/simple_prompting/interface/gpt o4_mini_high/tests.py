import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.oc = OrderCalculator()

    def test_is_empty_initial(self):
        self.assertTrue(self.oc.is_empty())

    def test_total_items_empty(self):
        self.assertEqual(self.oc.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.oc.list_items(), [])

    def test_get_subtotal_empty(self):
        self.assertAlmostEqual(self.oc.get_subtotal(), 0.0)

    def test_add_item_typical(self):
        self.oc.add_item("apple", 1.0, 3)
        self.assertFalse(self.oc.is_empty())
        self.assertEqual(self.oc.total_items(), 3)
        self.assertCountEqual(self.oc.list_items(), ["apple"])
        self.assertAlmostEqual(self.oc.get_subtotal(), 3.0)

    def test_add_item_default_quantity(self):
        self.oc.add_item("banana", 2.5)
        self.assertEqual(self.oc.total_items(), 1)
        self.assertAlmostEqual(self.oc.get_subtotal(), 2.5)

    def test_add_item_multiple_calls(self):
        self.oc.add_item("orange", 1.0, 2)
        self.oc.add_item("orange", 1.0, 1)
        self.assertEqual(self.oc.total_items(), 3)
        self.assertAlmostEqual(self.oc.get_subtotal(), 3.0)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item(123, 1.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item("pear", "free", 1)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.oc.add_item("pear", -1.0, 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.oc.add_item("pear", 1.0, "two")

    def test_add_item_nonpositive_quantity(self):
        with self.assertRaises(ValueError):
            self.oc.add_item("pear", 1.0, 0)

    def test_remove_item_typical(self):
        self.oc.add_item("apple", 1.0, 2)
        self.oc.add_item("banana", 2.0, 1)
        self.oc.remove_item("apple")
        self.assertEqual(self.oc.total_items(), 1)
        self.assertCountEqual(self.oc.list_items(), ["banana"])
        self.assertAlmostEqual(self.oc.get_subtotal(), 2.0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.oc.remove_item("nonexistent")

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.remove_item(123)

    def test_apply_discount_typical(self):
        result = self.oc.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_no_discount(self):
        self.assertAlmostEqual(self.oc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        self.assertAlmostEqual(self.oc.apply_discount(80.0, 1.0), 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.oc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.oc.apply_discount("100", 0.1)
        with self.assertRaises(TypeError):
            self.oc.apply_discount(100.0, "0.1")

    def test_calculate_shipping_free(self):
        self.assertAlmostEqual(self.oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_cost(self):
        self.assertAlmostEqual(self.oc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_shipping("50")

    def test_calculate_tax_typical(self):
        self.assertAlmostEqual(self.oc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        self.assertAlmostEqual(self.oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.oc.calculate_tax("100")

    def test_calculate_total_no_discount_free_shipping(self):
        self.oc.add_item("item", 50.0, 3)
        total = self.oc.calculate_total()
        subtotal = 150.0
        expected = subtotal + subtotal * 0.23
        self.assertAlmostEqual(total, expected)

    def test_calculate_total_with_discount_and_shipping(self):
        self.oc.add_item("item", 20.0, 2)
        total = self.oc.calculate_total(0.1)
        discounted = 40.0 * 0.9
        shipping = 10.0
        tax = discounted * 0.23
        expected = discounted + shipping + tax
        self.assertAlmostEqual(total, expected)

    def test_total_items_multiple(self):
        self.oc.add_item("a", 1.0, 2)
        self.oc.add_item("b", 2.0, 3)
        self.assertEqual(self.oc.total_items(), 5)

    def test_clear_order(self):
        self.oc.add_item("x", 5.0, 1)
        self.oc.clear_order()
        self.assertTrue(self.oc.is_empty())
        self.assertEqual(self.oc.list_items(), [])
        self.assertAlmostEqual(self.oc.get_subtotal(), 0.0)

    def test_custom_init_parameters(self):
        oc2 = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(oc2.calculate_tax(200.0), 20.0)
        self.assertAlmostEqual(oc2.calculate_shipping(49.99), 5.0)
        self.assertAlmostEqual(oc2.calculate_shipping(50.0), 0.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="high")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="low")
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="cheap")

if __name__ == '__main__':
    unittest.main()
