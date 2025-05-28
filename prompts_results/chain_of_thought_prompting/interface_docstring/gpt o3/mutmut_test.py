import unittest
from order_calculator import OrderCalculator


class TestOrderCalculator(unittest.TestCase):
    def test_init_default(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertAlmostEqual(calc.calculate_tax(100), 23.0, places=2)
        self.assertEqual(calc.calculate_shipping(50), 10.0)
        self.assertEqual(calc.calculate_shipping(100), 0.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50, shipping_cost=5)
        self.assertAlmostEqual(calc.calculate_tax(100), 10.0, places=2)
        self.assertEqual(calc.calculate_shipping(49.99), 5.0)
        self.assertEqual(calc.calculate_shipping(50), 0.0)

    def test_init_tax_rate_above_one_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)

    def test_init_negative_tax_rate_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_negative_free_shipping_threshold_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10)

    def test_init_negative_shipping_cost_raises_value_error(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_init_wrong_type_tax_rate_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.2")

    def test_init_wrong_type_free_shipping_threshold_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100")

    def test_init_wrong_type_shipping_cost_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_add_item_first_entry(self):
        calc = OrderCalculator()
        calc.add_item("Book", 20.0, 2)
        self.assertEqual(calc.total_items(), 2)

    def test_add_item_same_name_price_aggregates_quantity(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.add_item("Book", 10.0, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(calc.list_items(), ["Book"])

    def test_add_item_same_name_different_price_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0)
        with self.assertRaises(ValueError):
            calc.add_item("Book", 12.0)

    def test_add_item_empty_name_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("", 10.0)

    def test_add_item_non_positive_price_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 0)

    def test_add_item_quantity_less_than_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item("Book", 10.0, 0)

    def test_add_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 10.0, 1)

    def test_add_item_price_not_number_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Book", "9.99", 1)

    def test_add_item_quantity_not_int_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item("Book", 9.99, "3")

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.remove_item("Book")
        self.assertTrue(calc.is_empty())

    def test_remove_item_one_of_many(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0)
        calc.add_item("Pen", 1.0)
        calc.remove_item("Pen")
        self.assertEqual(calc.list_items(), ["Book"])
        self.assertEqual(calc.total_items(), 1)

    def test_remove_item_nonexistent_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item("Ghost")

    def test_remove_item_name_not_string_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        calc = OrderCalculator()
        calc.add_item("Book", 10.0, 2)
        calc.add_item("Pen", 1.0, 3)
        self.assertEqual(calc.get_subtotal(), 23.0)

    def test_get_subtotal_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_typical(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(100, 0.2), 80.0, places=2)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(50, 0.0), 50.0, places=2)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.apply_discount(50, 1.0), 0.0, places=2)

    def test_apply_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50, -0.1)

    def test_apply_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(50, 1.1)

    def test_apply_discount_negative_subtotal_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10, 0.1)

    def test_apply_discount_subtotal_wrong_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount("100", 0.1)

    def test_apply_discount_discount_wrong_type_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100, "0.1")

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_equal_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)
    #
    # def test_calculate_shipping_negative_subtotal_raises_value_error(self):
    #     calc = OrderCalculator()
    #     with self.assertRaises(ValueError):
    #         calc.calculate_shipping(-1.0)

    def test_calculate_shipping_non_numeric_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping("50")

    def test_calculate_tax_typical(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100), 20.0, places=2)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.calculate_tax(0), 0.0, places=2)

    def test_calculate_tax_negative_amount_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-1)

    def test_calculate_tax_non_numeric_amount_raises_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("100")

    def test_calculate_total_small_order_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("Item", 20.0)
        self.assertAlmostEqual(calc.calculate_total(), 36.9, places=2)

    def test_calculate_total_large_order_no_discount(self):
        calc = OrderCalculator()
        calc.add_item("A", 60.0)
        calc.add_item("B", 50.0)
        self.assertAlmostEqual(calc.calculate_total(), 135.3, places=2)

    def test_calculate_total_discount_triggers_shipping(self):
        calc = OrderCalculator()
        calc.add_item("Item", 100.0)
        self.assertAlmostEqual(calc.calculate_total(0.2), 110.7, places=2)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator()
        calc.add_item("Item", 40.0)
        self.assertAlmostEqual(calc.calculate_total(1.0), 12.3, places=2)

    def test_calculate_total_discount_zero(self):
        calc = OrderCalculator()
        calc.add_item("A", 30.0)
        calc.add_item("B", 30.0)
        self.assertAlmostEqual(calc.calculate_total(0.0), 86.1, places=2)

    def test_calculate_total_discount_above_one_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item("Item", 20.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.1)

    def test_calculate_total_discount_below_zero_raises_value_error(self):
        calc = OrderCalculator()
        calc.add_item("Item", 20.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(-0.1)

    def test_calculate_total_discount_wrong_type_raises_type_error(self):
        calc = OrderCalculator()
        calc.add_item("Item", 20.0)
        with self.assertRaises(TypeError):
            calc.calculate_total("0.2")

    def test_calculate_total_empty_order_raises_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0, 2)
        calc.add_item("B", 5.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_list_items_unique(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.add_item("B", 5.0)
        calc.add_item("A", 10.0)
        self.assertCountEqual(calc.list_items(), ["A", "B"])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_new_calculator(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_after_adding_item(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        self.assertFalse(calc.is_empty())

    def test_is_empty_after_clearing(self):
        calc = OrderCalculator()
        calc.add_item("A", 10.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
