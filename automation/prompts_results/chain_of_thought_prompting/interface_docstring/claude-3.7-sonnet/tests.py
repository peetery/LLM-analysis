import unittest
from order_calculator import OrderCalculator, Item


class TestOrderCalculator(unittest.TestCase):
   def test_default_constructor(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.tax_rate, 0.23)
       self.assertEqual(calculator.free_shipping_threshold, 100.0)
       self.assertEqual(calculator.shipping_cost, 10.0)

   def test_custom_constructor(self):
       calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
       self.assertEqual(calculator.tax_rate, 0.1)
       self.assertEqual(calculator.free_shipping_threshold, 50.0)
       self.assertEqual(calculator.shipping_cost, 5.0)

   def test_invalid_tax_rate_negative(self):
       with self.assertRaises(ValueError):
           OrderCalculator(tax_rate=-0.1)

   def test_invalid_tax_rate_above_one(self):
       with self.assertRaises(ValueError):
           OrderCalculator(tax_rate=1.1)

   def test_invalid_free_shipping_threshold(self):
       with self.assertRaises(ValueError):
           OrderCalculator(free_shipping_threshold=-10.0)

   def test_invalid_shipping_cost(self):
       with self.assertRaises(ValueError):
           OrderCalculator(shipping_cost=-5.0)

   def test_invalid_constructor_parameter_types(self):
       with self.assertRaises(TypeError):
           OrderCalculator(tax_rate="0.23")
       with self.assertRaises(TypeError):
           OrderCalculator(free_shipping_threshold="100")
       with self.assertRaises(TypeError):
           OrderCalculator(shipping_cost="10")

   def test_adding_new_item(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 2)
       self.assertFalse(calculator.is_empty())
       self.assertEqual(calculator.total_items(), 2)

   def test_adding_item_with_default_quantity(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       self.assertEqual(calculator.total_items(), 1)

   def test_adding_existing_item(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 2)
       calculator.add_item("Product", 10.0, 3)
       self.assertEqual(calculator.total_items(), 5)

   def test_adding_item_with_same_name_different_price(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       with self.assertRaises(ValueError):
           calculator.add_item("Product", 15.0)

   def test_adding_item_with_empty_name(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.add_item("", 10.0)

   def test_adding_item_with_zero_price(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.add_item("Product", 0.0)

   def test_adding_item_with_negative_price(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.add_item("Product", -10.0)

   def test_adding_item_with_zero_quantity(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.add_item("Product", 10.0, 0)

   def test_adding_item_with_negative_quantity(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.add_item("Product", 10.0, -2)

   def test_adding_item_with_invalid_types(self):
       calculator = OrderCalculator()
       with self.assertRaises(TypeError):
           calculator.add_item(123, 10.0)
       with self.assertRaises(TypeError):
           calculator.add_item("Product", "10.0")
       with self.assertRaises(TypeError):
           calculator.add_item("Product", 10.0, "2")

   def test_removing_existing_item(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       calculator.remove_item("Product")
       self.assertTrue(calculator.is_empty())

   def test_removing_non_existing_item(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.remove_item("Product")

   def test_removing_item_with_invalid_type(self):
       calculator = OrderCalculator()
       with self.assertRaises(TypeError):
           calculator.remove_item(123)

   def test_listing_items_in_empty_order(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.list_items(), [])

   def test_listing_items_in_non_empty_order(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 10.0)
       calculator.add_item("Product2", 20.0)
       self.assertEqual(set(calculator.list_items()), {"Product1", "Product2"})

   def test_listing_items_with_duplicate_names(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 10.0, 2)
       calculator.add_item("Product1", 10.0, 3)
       calculator.add_item("Product2", 20.0)
       self.assertEqual(set(calculator.list_items()), {"Product1", "Product2"})

   def test_empty_order_after_initialization(self):
       calculator = OrderCalculator()
       self.assertTrue(calculator.is_empty())

   def test_non_empty_order(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       self.assertFalse(calculator.is_empty())

   def test_empty_order_after_clearing(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       calculator.clear_order()
       self.assertTrue(calculator.is_empty())

   def test_clearing_empty_order(self):
       calculator = OrderCalculator()
       calculator.clear_order()
       self.assertTrue(calculator.is_empty())

   def test_clearing_non_empty_order(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       calculator.clear_order()
       self.assertTrue(calculator.is_empty())
       self.assertEqual(calculator.total_items(), 0)

   def test_total_items_in_empty_order(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.total_items(), 0)

   def test_total_items_with_single_item(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 3)
       self.assertEqual(calculator.total_items(), 3)

   def test_total_items_with_multiple_items(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 10.0, 3)
       calculator.add_item("Product2", 20.0, 2)
       self.assertEqual(calculator.total_items(), 5)

   def test_subtotal_with_single_item(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 3)
       self.assertEqual(calculator.get_subtotal(), 30.0)

   def test_subtotal_with_multiple_items(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 10.0, 3)
       calculator.add_item("Product2", 20.0, 2)
       self.assertEqual(calculator.get_subtotal(), 70.0)

   def test_subtotal_with_empty_order(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.get_subtotal()

   def test_zero_discount(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.apply_discount(100.0, 0.0), 100.0)

   def test_partial_discount(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.apply_discount(100.0, 0.2), 80.0)

   def test_full_discount(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.apply_discount(100.0, 1.0), 0.0)

   def test_negative_subtotal(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.apply_discount(-100.0, 0.2)

   def test_negative_discount(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.apply_discount(100.0, -0.2)

   def test_discount_above_one(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.apply_discount(100.0, 1.2)

   def test_invalid_types_for_discount_calculation(self):
       calculator = OrderCalculator()
       with self.assertRaises(TypeError):
           calculator.apply_discount("100.0", 0.2)
       with self.assertRaises(TypeError):
           calculator.apply_discount(100.0, "0.2")

   def test_shipping_below_threshold(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_shipping(90.0), 10.0)

   def test_shipping_at_threshold(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_shipping(100.0), 0.0)

   def test_shipping_above_threshold(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_shipping(110.0), 0.0)

   def test_shipping_with_invalid_type(self):
       calculator = OrderCalculator()
       with self.assertRaises(TypeError):
           calculator.calculate_shipping("90.0")

   def test_tax_on_zero_amount(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_tax(0.0), 0.0)

   def test_tax_on_positive_amount(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_tax(100.0), 23.0)

   def test_tax_on_negative_amount(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.calculate_tax(-100.0)

   def test_tax_with_invalid_type(self):
       calculator = OrderCalculator()
       with self.assertRaises(TypeError):
           calculator.calculate_tax("100.0")

   def test_total_with_no_discount(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 3)
       self.assertEqual(calculator.calculate_total(), 36.9)  # 30 + 0 (free shipping) + 23% tax = 36.9

   def test_total_with_discount(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 100.0, 1)
       self.assertEqual(calculator.calculate_total(0.2), 98.4)  # 100 - 20% = 80 + 0 (free shipping) + 23% tax = 98.4

   def test_total_below_free_shipping_threshold(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 40.0, 2)
       self.assertEqual(calculator.calculate_total(), 110.7)  # 80 + 10 (shipping) + 23% tax on 90 = 110.7

   def test_total_above_free_shipping_threshold(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 60.0, 2)
       self.assertEqual(calculator.calculate_total(), 147.6)  # 120 + 0 (free shipping) + 23% tax = 147.6

   def test_total_with_empty_order(self):
       calculator = OrderCalculator()
       with self.assertRaises(ValueError):
           calculator.calculate_total()

   def test_total_with_invalid_discount(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       with self.assertRaises(ValueError):
           calculator.calculate_total(1.2)

   def test_total_with_invalid_type(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0)
       with self.assertRaises(TypeError):
           calculator.calculate_total("0.2")

   def test_exact_boundary_for_free_shipping(self):
       calculator = OrderCalculator()
       self.assertEqual(calculator.calculate_shipping(100.0), 0.0)
       calculator.add_item("Product", 100.0, 1)
       total = calculator.calculate_total()
       expected = 100.0 + 0.0 + calculator.tax_rate * 100.0
       self.assertEqual(total, expected)

   def test_with_very_large_values(self):
       calculator = OrderCalculator()
       large_price = 1000000.0
       calculator.add_item("ExpensiveProduct", large_price)
       self.assertEqual(calculator.get_subtotal(), large_price)

   def test_with_very_small_values(self):
       calculator = OrderCalculator()
       small_price = 0.01
       calculator.add_item("CheapProduct", small_price, 10)
       self.assertEqual(calculator.get_subtotal(), 0.1)

   def test_floating_point_precision(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 0.1, 3)
       self.assertAlmostEqual(calculator.get_subtotal(), 0.3, places=10)

   def test_complete_order_flow(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 60.0, 1)
       calculator.add_item("Product2", 40.0, 1)
       discounted = calculator.apply_discount(calculator.get_subtotal(), 0.1)
       shipping = calculator.calculate_shipping(discounted)
       tax = calculator.calculate_tax(discounted + shipping)
       expected_total = discounted + shipping + tax
       self.assertEqual(calculator.calculate_total(0.1), expected_total)

   def test_add_remove_calculate_flow(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 40.0, 2)
       calculator.add_item("Product2", 30.0, 1)
       calculator.remove_item("Product1")
       self.assertEqual(calculator.get_subtotal(), 30.0)
       self.assertEqual(calculator.calculate_total(), 46.9)  # 30 + 10 (shipping) + 23% tax on 40 = 46.9

   def test_add_clear_verify_flow(self):
       calculator = OrderCalculator()
       calculator.add_item("Product1", 40.0, 2)
       calculator.add_item("Product2", 30.0, 1)
       calculator.clear_order()
       self.assertTrue(calculator.is_empty())
       self.assertEqual(calculator.total_items(), 0)
       self.assertEqual(calculator.list_items(), [])

   def test_multiple_quantity_updates(self):
       calculator = OrderCalculator()
       calculator.add_item("Product", 10.0, 1)
       calculator.add_item("Product", 10.0, 2)
       calculator.add_item("Product", 10.0, 3)
       self.assertEqual(calculator.total_items(), 6)
       self.assertEqual(calculator.get_subtotal(), 60.0)

   def test_order_with_mixed_item_types(self):
       calculator = OrderCalculator()
       calculator.add_item("CheapProduct", 1.0, 10)
       calculator.add_item("ExpensiveProduct", 200.0, 1)
       self.assertEqual(calculator.get_subtotal(), 210.0)
       self.assertEqual(calculator.calculate_total(), 258.3)  # 210 + 0 (free shipping) + 23% tax = 258.3


if __name__ == "__main__":
   unittest.main()