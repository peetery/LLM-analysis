import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    # __init__
    def test_init_valid_defaults(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)
        self.assertTrue(oc.is_empty())

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50, shipping_cost=5)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50)
        self.assertEqual(oc.shipping_cost, 5)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-2)

    # add_item
    def test_add_item_new(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Book", 10.0, 2)
        self.assertEqual(self.calc.items[0], {"name": "Book", "price": 10.0, "quantity": 2})

    def test_add_item_existing_increases_quantity(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Pen", 1.5, 1)
        self.calc.add_item("Pen", 1.5, 3)
        self.assertEqual(self.calc.items[0]["quantity"], 4)

    def test_add_item_same_name_different_price(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Notebook", 5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item("Notebook", 6.0, 1)

    def test_add_item_invalid_name_type(self):
        self.calc = OrderCalculator()
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 5.0, 1)

    def test_add_item_empty_name(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.add_item("", 5.0, 1)

    def test_add_item_invalid_price_value(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.add_item("Box", 0, 1)

    def test_add_item_invalid_quantity_value(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.add_item("Box", 1.0, 0)

    # remove_item
    def test_remove_item_success(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Cup", 2.0, 1)
        self.calc.remove_item("Cup")
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_nonexistent(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.remove_item("Ghost")

    def test_remove_item_invalid_type(self):
        self.calc = OrderCalculator()
        with self.assertRaises(TypeError):
            self.calc.remove_item(10)

    # get_subtotal
    def test_get_subtotal(self):
        self.calc = OrderCalculator()
        self.calc.add_item("ItemA", 3.0, 2)
        self.calc.add_item("ItemB", 4.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_order(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    # apply_discount
    def test_apply_discount_valid(self):
        self.calc = OrderCalculator()
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_invalid_rate(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        self.calc = OrderCalculator()
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100", 0.1)

    # calculate_shipping
    def test_calculate_shipping_free(self):
        self.calc = OrderCalculator(free_shipping_threshold=50)
        self.assertEqual(self.calc.calculate_shipping(60), 0.0)

    def test_calculate_shipping_cost(self):
        self.calc = OrderCalculator(shipping_cost=7)
        self.assertEqual(self.calc.calculate_shipping(20), 7)

    def test_calculate_shipping_invalid_type(self):
        self.calc = OrderCalculator()
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("20")

    # calculate_tax
    def test_calculate_tax_valid(self):
        self.calc = OrderCalculator(tax_rate=0.1)
        self.assertAlmostEqual(self.calc.calculate_tax(50), 5)

    def test_calculate_tax_negative_amount(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-1)

    def test_calculate_tax_invalid_type(self):
        self.calc = OrderCalculator()
        with self.assertRaises(TypeError):
            self.calc.calculate_tax([1])

    # calculate_total
    def test_calculate_total_no_discount(self):
        self.calc = OrderCalculator(tax_rate=0.1, shipping_cost=5, free_shipping_threshold=100)
        self.calc.add_item("Item", 20, 2)
        expected = 40 + 5 + (45 * 0.1)  # discounted_subtotal=40, shipping=5, tax on 45
        self.assertAlmostEqual(self.calc.calculate_total(), expected)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=30, shipping_cost=5)
        self.calc.add_item("Item", 20, 2)
        total = self.calc.calculate_total(discount=0.25)  # subtotal=40, discounted=30, free shipping, tax=6
        self.assertAlmostEqual(total, 36)

    def test_calculate_total_invalid_discount_type(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Item", 10, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount="0.1")

    def test_calculate_total_empty_order(self):
        self.calc = OrderCalculator()
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    # total_items
    def test_total_items(self):
        self.calc = OrderCalculator()
        self.calc.add_item("A", 1, 3)
        self.calc.add_item("B", 2, 2)
        self.assertEqual(self.calc.total_items(), 5)

    # clear_order
    def test_clear_order(self):
        self.calc = OrderCalculator()
        self.calc.add_item("X", 1, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())

    # list_items
    def test_list_items_unique(self):
        self.calc = OrderCalculator()
        self.calc.add_item("Pen", 1, 1)
        self.calc.add_item("Pen", 1, 2)
        self.calc.add_item("Pencil", 2, 1)
        self.assertEqual(set(self.calc.list_items()), {"Pen", "Pencil"})

    # is_empty
    def test_is_empty(self):
        self.calc = OrderCalculator()
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item("Thing", 1, 1)
        self.assertFalse(self.calc.is_empty())


if __name__ == "__main__":
    unittest.main()
