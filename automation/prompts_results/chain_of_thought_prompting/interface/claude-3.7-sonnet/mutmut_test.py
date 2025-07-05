import unittest
from typing import TypedDict, List

class Item(TypedDict):
   pass

class OrderCalculator:
   def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
       pass

   def add_item(self, name: str, price: float, quantity: int = 1):
       pass

   def remove_item(self, name: str):
       pass

   def get_subtotal(self) -> float:
       pass

   def apply_discount(self, subtotal: float, discount: float) -> float:
       pass

   def calculate_shipping(self, discounted_subtotal: float) -> float:
       pass

   def calculate_tax(self, amount: float) -> float:
       pass

   def calculate_total(self, discount: float = 0.0) -> float:
       pass

   def total_items(self) -> int:
       pass

   def clear_order(self):
       pass

   def list_items(self) -> List[str]:
       pass

   def is_empty(self) -> bool:
       pass


class TestOrderCalculator(unittest.TestCase):
   def setUp(self):
       self.calculator = OrderCalculator()
       self.custom_calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=5.0)

   def test_default_constructor(self):
       self.assertEqual(0.23, self.calculator._tax_rate)
       self.assertEqual(100.0, self.calculator._free_shipping_threshold)
       self.assertEqual(10.0, self.calculator._shipping_cost)

   def test_custom_constructor(self):
       self.assertEqual(0.1, self.custom_calculator._tax_rate)
       self.assertEqual(200.0, self.custom_calculator._free_shipping_threshold)
       self.assertEqual(5.0, self.custom_calculator._shipping_cost)

   def test_add_single_item(self):
       self.calculator.add_item("product", 10.0)
       self.assertEqual(1, self.calculator.total_items())
       self.assertEqual(10.0, self.calculator.get_subtotal())

   def test_add_item_with_custom_quantity(self):
       self.calculator.add_item("product", 10.0, 3)
       self.assertEqual(3, self.calculator.total_items())
       self.assertEqual(30.0, self.calculator.get_subtotal())

   def test_add_multiple_different_items(self):
       self.calculator.add_item("product1", 10.0)
       self.calculator.add_item("product2", 20.0)
       self.assertEqual(2, len(self.calculator.list_items()))
       self.assertEqual(30.0, self.calculator.get_subtotal())

   def test_add_duplicate_item(self):
       self.calculator.add_item("product", 10.0)
       self.calculator.add_item("product", 20.0)
       self.assertEqual(1, len(self.calculator.list_items()))

   def test_add_item_with_zero_price(self):
       self.calculator.add_item("free_product", 0.0)
       self.assertEqual(1, self.calculator.total_items())
       self.assertEqual(0.0, self.calculator.get_subtotal())

   def test_add_item_with_negative_price(self):
       with self.assertRaises(ValueError):
           self.calculator.add_item("product", -10.0)

   def test_add_item_with_zero_quantity(self):
       with self.assertRaises(ValueError):
           self.calculator.add_item("product", 10.0, 0)

   def test_add_item_with_negative_quantity(self):
       with self.assertRaises(ValueError):
           self.calculator.add_item("product", 10.0, -1)

   def test_add_item_with_empty_name(self):
       with self.assertRaises(ValueError):
           self.calculator.add_item("", 10.0)

   def test_add_item_with_invalid_name_type(self):
       with self.assertRaises(TypeError):
           self.calculator.add_item(123, 10.0)

   def test_add_item_with_invalid_price_type(self):
       with self.assertRaises(TypeError):
           self.calculator.add_item("product", "10.0")

   def test_add_item_with_invalid_quantity_type(self):
       with self.assertRaises(TypeError):
           self.calculator.add_item("product", 10.0, "3")

   def test_remove_existing_item(self):
       self.calculator.add_item("product", 10.0)
       self.calculator.remove_item("product")
       self.assertTrue(self.calculator.is_empty())

   def test_remove_non_existent_item(self):
       with self.assertRaises(KeyError):
           self.calculator.remove_item("non_existent")

   def test_remove_item_with_empty_name(self):
       with self.assertRaises(ValueError):
           self.calculator.remove_item("")

   def test_remove_item_with_invalid_name_type(self):
       with self.assertRaises(TypeError):
           self.calculator.remove_item(123)

   def test_remove_item_from_empty_order(self):
       with self.assertRaises(KeyError):
           self.calculator.remove_item("product")

   def test_get_subtotal_with_multiple_items(self):
       self.calculator.add_item("product1", 10.0, 2)
       self.calculator.add_item("product2", 20.0, 3)
       self.assertEqual(80.0, self.calculator.get_subtotal())

   def test_get_subtotal_with_single_item(self):
       self.calculator.add_item("product", 10.0, 2)
       self.assertEqual(20.0, self.calculator.get_subtotal())

   def test_get_subtotal_from_empty_order(self):
       self.assertEqual(0.0, self.calculator.get_subtotal())

   def test_apply_percentage_discount(self):
       self.assertEqual(80.0, self.calculator.apply_discount(100.0, 20.0))

   def test_apply_fixed_amount_discount(self):
       self.assertEqual(80.0, self.calculator.apply_discount(100.0, 20.0))

   def test_apply_zero_discount(self):
       self.assertEqual(100.0, self.calculator.apply_discount(100.0, 0.0))

   def test_apply_discount_greater_than_subtotal(self):
       self.assertEqual(0.0, self.calculator.apply_discount(100.0, 150.0))

   def test_apply_negative_discount(self):
       with self.assertRaises(ValueError):
           self.calculator.apply_discount(100.0, -20.0)

   def test_apply_discount_to_zero_subtotal(self):
       self.assertEqual(0.0, self.calculator.apply_discount(0.0, 20.0))

   def test_apply_discount_with_invalid_subtotal_type(self):
       with self.assertRaises(TypeError):
           self.calculator.apply_discount("100.0", 20.0)

   def test_apply_discount_with_invalid_discount_type(self):
       with self.assertRaises(TypeError):
           self.calculator.apply_discount(100.0, "20.0")

   def test_calculate_shipping_below_threshold(self):
       self.assertEqual(10.0, self.calculator.calculate_shipping(90.0))

   def test_calculate_shipping_above_threshold(self):
       self.assertEqual(0.0, self.calculator.calculate_shipping(110.0))

   def test_calculate_shipping_exactly_at_threshold(self):
       self.assertEqual(0.0, self.calculator.calculate_shipping(100.0))

   def test_calculate_shipping_with_zero_subtotal(self):
       self.assertEqual(10.0, self.calculator.calculate_shipping(0.0))

   def test_calculate_shipping_with_negative_subtotal(self):
       with self.assertRaises(ValueError):
           self.calculator.calculate_shipping(-10.0)

   def test_calculate_shipping_with_invalid_subtotal_type(self):
       with self.assertRaises(TypeError):
           self.calculator.calculate_shipping("90.0")

   def test_calculate_tax_for_normal_amount(self):
       self.assertEqual(23.0, self.calculator.calculate_tax(100.0))

   def test_calculate_tax_for_zero_amount(self):
       self.assertEqual(0.0, self.calculator.calculate_tax(0.0))

   def test_calculate_tax_for_negative_amount(self):
       with self.assertRaises(ValueError):
           self.calculator.calculate_tax(-100.0)

   def test_calculate_tax_with_invalid_amount_type(self):
       with self.assertRaises(TypeError):
           self.calculator.calculate_tax("100.0")

   def test_calculate_total_without_discount(self):
       self.calculator.add_item("product", 50.0, 2)
       total = self.calculator.calculate_total()
       self.assertEqual(133.0, total)  # 100 + 10 shipping + 23 tax

   def test_calculate_total_with_discount(self):
       self.calculator.add_item("product", 50.0, 2)
       total = self.calculator.calculate_total(20.0)
       self.assertEqual(108.8, total)  # 100 - 20 = 80 + 10 shipping + 18.4 tax

   def test_calculate_total_for_empty_order(self):
       total = self.calculator.calculate_total()
       self.assertEqual(0.0, total)

   def test_calculate_total_with_free_shipping(self):
       self.calculator.add_item("product", 101.0)
       total = self.calculator.calculate_total()
       self.assertEqual(124.23, total)  # 101 + 0 shipping + 23.23 tax

   def test_calculate_total_with_invalid_discount_type(self):
       with self.assertRaises(TypeError):
           self.calculator.calculate_total("20.0")

   def test_calculate_total_with_negative_discount(self):
       with self.assertRaises(ValueError):
           self.calculator.calculate_total(-20.0)

   def test_calculate_total_with_discount_exceeding_subtotal(self):
       self.calculator.add_item("product", 50.0)
       total = self.calculator.calculate_total(60.0)
       self.assertEqual(0.0, total)  # Subtotal becomes 0, no shipping or tax

   def test_count_total_items_with_multiple_products(self):
       self.calculator.add_item("product1", 10.0, 2)
       self.calculator.add_item("product2", 20.0, 3)
       self.assertEqual(5, self.calculator.total_items())

   def test_count_total_items_with_single_product(self):
       self.calculator.add_item("product", 10.0, 3)
       self.assertEqual(3, self.calculator.total_items())

   def test_count_total_items_in_empty_order(self):
       self.assertEqual(0, self.calculator.total_items())

   def test_clear_non_empty_order(self):
       self.calculator.add_item("product1", 10.0)
       self.calculator.add_item("product2", 20.0)
       self.calculator.clear_order()
       self.assertTrue(self.calculator.is_empty())

   def test_clear_already_empty_order(self):
       self.calculator.clear_order()
       self.assertTrue(self.calculator.is_empty())

   def test_clear_order_and_verify_state_reset(self):
       self.calculator.add_item("product", 10.0, 2)
       self.calculator.clear_order()
       self.assertEqual(0, self.calculator.total_items())
       self.assertEqual(0.0, self.calculator.get_subtotal())
       self.assertEqual(0, len(self.calculator.list_items()))
       self.assertTrue(self.calculator.is_empty())

   def test_list_items_with_multiple_products(self):
       self.calculator.add_item("product1", 10.0)
       self.calculator.add_item("product2", 20.0)
       items = self.calculator.list_items()
       self.assertEqual(2, len(items))
       self.assertIn("product1", items)
       self.assertIn("product2", items)

   def test_list_items_with_single_product(self):
       self.calculator.add_item("product", 10.0)
       items = self.calculator.list_items()
       self.assertEqual(1, len(items))
       self.assertIn("product", items)

   def test_list_items_in_empty_order(self):
       items = self.calculator.list_items()
       self.assertEqual(0, len(items))

   def test_check_empty_status_on_new_order(self):
       self.assertTrue(self.calculator.is_empty())

   def test_check_empty_status_after_adding_items(self):
       self.calculator.add_item("product", 10.0)
       self.assertFalse(self.calculator.is_empty())

   def test_check_empty_status_after_removing_all_items(self):
       self.calculator.add_item("product", 10.0)
       self.calculator.remove_item("product")
       self.assertTrue(self.calculator.is_empty())

   def test_check_empty_status_after_clearing(self):
       self.calculator.add_item("product", 10.0)
       self.calculator.clear_order()
       self.assertTrue(self.calculator.is_empty())

   def test_add_and_remove_items(self):
       self.calculator.add_item("product1", 10.0)
       self.calculator.add_item("product2", 20.0)
       self.calculator.remove_item("product1")
       self.assertEqual(1, len(self.calculator.list_items()))
       self.assertEqual(20.0, self.calculator.get_subtotal())

   def test_full_order_processing_workflow(self):
       self.calculator.add_item("product1", 30.0, 2)
       self.calculator.add_item("product2", 40.0, 1)
       subtotal = self.calculator.get_subtotal()
       self.assertEqual(100.0, subtotal)
       discounted = self.calculator.apply_discount(subtotal, 20.0)
       self.assertEqual(80.0, discounted)
       shipping = self.calculator.calculate_shipping(discounted)
       self.assertEqual(10.0, shipping)
       tax = self.calculator.calculate_tax(discounted + shipping)
       self.assertEqual(20.7, tax)
       total = self.calculator.calculate_total(20.0)
       self.assertEqual(110.7, total)

   def test_order_modification_after_calculation(self):
       self.calculator.add_item("product", 50.0)
       total1 = self.calculator.calculate_total()
       self.calculator.add_item("product2", 50.0)
       total2 = self.calculator.calculate_total()
       self.assertNotEqual(total1, total2)

   def test_discount_impact_on_shipping(self):
       self.calculator.add_item("product", 110.0)
       total_no_discount = self.calculator.calculate_total()
       total_with_discount = self.calculator.calculate_total(20.0)
       self.assertGreater(total_no_discount, total_with_discount)

   def test_order_state_after_operations(self):
       self.calculator.add_item("product1", 10.0)
       self.calculator.add_item("product2", 20.0)
       self.calculator.remove_item("product1")
       self.calculator.add_item("product3", 30.0)
       items = self.calculator.list_items()
       self.assertEqual(2, len(items))
       self.assertIn("product2", items)
       self.assertIn("product3", items)
       self.assertEqual(50.0, self.calculator.get_subtotal())


if __name__ == '__main__':
   unittest.main()