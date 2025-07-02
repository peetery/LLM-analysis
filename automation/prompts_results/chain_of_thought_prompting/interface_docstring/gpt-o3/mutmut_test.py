import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    # __init__ scenarios
    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertAlmostEqual(calc.tax_rate, 0.23)
        self.assertAlmostEqual(calc.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50, shipping_cost=5)
        self.assertAlmostEqual(calc.tax_rate, 0.05)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50)
        self.assertAlmostEqual(calc.shipping_cost, 5)

    def test_init_tax_rate_zero(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertAlmostEqual(calc.tax_rate, 0.0)

    def test_init_tax_rate_one(self):
        calc = OrderCalculator(tax_rate=1.0)
        self.assertAlmostEqual(calc.tax_rate, 1.0)

    def test_init_tax_rate_negative_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_one_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.2)

    def test_init_negative_free_shipping_threshold_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1)

    def test_init_negative_shipping_cost_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_free_shipping_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="50")

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    # add_item scenarios
    def test_add_item_first(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 3)
        self.assertEqual(calc.total_items(), 3)

    def test_add_item_accumulates_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 3)
        calc.add_item("Pen", 2.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_add_item_same_name_diff_price_error(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item("Pen", 2.5, 1)

    def test_add_item_quantity_default(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0)
        self.assertEqual(calc.total_items(), 1)

    def test_add_item_empty_name_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 1.0, 1)

    def test_add_item_non_positive_price_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 0, 1)

    def test_add_item_quantity_less_than_one_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 5.0, 0)

    def test_add_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0, 1)

    def test_add_item_price_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Pen", "2.0", 1)

    def test_add_item_quantity_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Pen", 2.0, "3")

    # remove_item scenarios
    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 1)
        calc.remove_item("Pen")
        self.assertTrue(calc.is_empty())

    def test_remove_item_nonexistent_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Ghost")

    def test_remove_item_name_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    # get_subtotal scenarios
    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 3)
        calc.add_item("Book", 10.0, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    # apply_discount scenarios
    def test_apply_discount_normal(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(50.0, 0.0), 50.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(50.0, 1.0), 0.0)

    def test_apply_discount_negative_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50.0, -0.1)

    def test_apply_discount_above_one_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50.0, 1.5)

    def test_apply_discount_negative_subtotal_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-5.0, 0.1)

    def test_apply_discount_subtotal_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_apply_discount_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, "0.2")

    # calculate_shipping scenarios
    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_shipping(80.0), calc.shipping_cost)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_shipping(calc.free_shipping_threshold), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("80")

    # calculate_tax scenarios
    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("50")

    # calculate_total scenarios
    def test_calculate_total_no_discount_shipping_added(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 20.0, 2)
        expected = 40.0 + calc.shipping_cost + 0.23 * (40.0 + calc.shipping_cost)
        self.assertAlmostEqual(calc.calculate_total(0.0), expected)

    def test_calculate_total_discount_causes_shipping(self):
        calc = OrderCalculator()
        calc.add_item("Item", 120.0, 1)
        discounted = 120.0 * 0.8
        shipping = calc.shipping_cost
        expected = discounted + shipping + 0.23 * (discounted + shipping)
        self.assertAlmostEqual(calc.calculate_total(0.2), expected)

    def test_calculate_total_discount_keeps_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("Item", 130.0, 1)
        discounted = 130.0 * 0.9
        shipping = 0.0
        expected = discounted + shipping + 0.23 * (discounted + shipping)
        self.assertAlmostEqual(calc.calculate_total(0.1), expected)

    def test_calculate_total_discount_zero(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 20.0, 5)
        subtotal = 100.0
        shipping = 0.0
        expected = subtotal + shipping + 0.23 * subtotal
        self.assertAlmostEqual(calc.calculate_total(0.0), expected)

    def test_calculate_total_discount_full(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 25.0, 2)
        discounted = 0.0
        shipping = calc.shipping_cost
        expected = shipping + 0.23 * shipping
        self.assertAlmostEqual(calc.calculate_total(1.0), expected)

    def test_calculate_total_discount_negative_error(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_discount_above_one_error(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_calculate_total_empty_order_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total(0.0)

    def test_calculate_total_discount_type_error(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total("0.1")

    # total_items scenarios
    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 3)
        calc.add_item("Book", 5.0, 2)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    # clear_order scenario
    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    # list_items scenarios
    def test_list_items_unique_names(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 2)
        calc.add_item("Pen", 2.0, 1)
        calc.add_item("Book", 5.0, 1)
        self.assertEqual(set(calc.list_items()), {"Pen", "Book"})

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    # is_empty scenarios
    def test_is_empty_initial(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_add(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 1)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clear(self):
        calc = OrderCalculator()
        calc.add_item("Pen", 2.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())