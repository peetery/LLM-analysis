import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator


# class Item(TypedDict):
#     name: str
#     price: float
#     quantity: int
#
#
# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         if not isinstance(tax_rate, (float, int)):
#             raise TypeError("Tax rate must be a float or int.")
#         if not isinstance(free_shipping_threshold, (float, int)):
#             raise TypeError("Free shipping threshold must be a float or int.")
#         if not isinstance(shipping_cost, (float, int)):
#             raise TypeError("Shipping cost must be a float or int.")
#         if not 0.0 <= tax_rate <= 1.0:
#             raise ValueError("Tax rate must be between 0.0 and 1.0.")
#         if free_shipping_threshold < 0.0:
#             raise ValueError("Free shipping threshold cannot be negative.")
#         if shipping_cost < 0.0:
#             raise ValueError("Shipping cost cannot be negative.")
#
#         self.items: List[Item] = []
#         self.tax_rate = tax_rate
#         self.free_shipping_threshold = free_shipping_threshold
#         self.shipping_cost = shipping_cost
#
#     def add_item(self, name: str, price: float, quantity: int = 1):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not isinstance(price, (float, int)):
#             raise TypeError("Price must be a number.")
#         if not isinstance(quantity, int):
#             raise TypeError("Quantity must be an integer.")
#         if not name:
#             raise ValueError("Item name cannot be empty.")
#         if quantity < 1:
#             raise ValueError("Quantity must be at least 1.")
#         if price <= 0:
#             raise ValueError("Price must be greater than 0.")
#
#         for item in self.items:
#             if item["name"] == name:
#                 if item["price"] != price:
#                     raise ValueError("Item with the same name but different price already exists.")
#                 item["quantity"] += quantity
#                 return
#
#         self.items.append({
#             "name": name,
#             "price": price,
#             "quantity": quantity
#         })
#
#     def remove_item(self, name: str):
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not any(item["name"] == name for item in self.items):
#             raise ValueError(f"Item with name '{name}' does not exist in the order.")
#
#         self.items = [item for item in self.items if item["name"] != name]
#
#     def get_subtotal(self) -> float:
#         if not self.items:
#             raise ValueError("Cannot calculate subtotal on empty order.")
#         return sum(item["price"] * item["quantity"] for item in self.items)
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         if not isinstance(subtotal, (float, int)):
#             raise TypeError("Subtotal must be a number.")
#         if not isinstance(discount, (float, int)):
#             raise TypeError("Discount must be a number.")
#         if not 0.0 <= discount <= 1.0:
#             raise ValueError("Discount must be between 0.0 and 1.0.")
#         if subtotal < 0.0:
#             raise ValueError("Cannot apply discount on negative subtotal.")
#         return subtotal * (1 - discount)
#
#     def calculate_shipping(self, discounted_subtotal: float) -> float:
#         if not isinstance(discounted_subtotal, (float, int)):
#             raise TypeError("Discounted subtotal must be a number.")
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         if not isinstance(amount, (float, int)):
#             raise TypeError("Amount must be a number.")
#         if amount < 0.0:
#             raise ValueError("Cannot calculate tax on negative amount.")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         if not isinstance(discount, (float, int)):
#             raise TypeError("Discount must be a number.")
#
#         subtotal = self.get_subtotal()
#         if subtotal < 0.0:
#             raise ValueError("Cannot calculate total on negative subtotal.")
#         discounted_subtotal = self.apply_discount(subtotal, discount)
#         shipping_cost = self.calculate_shipping(discounted_subtotal)
#         tax = self.calculate_tax(discounted_subtotal + shipping_cost)
#         return discounted_subtotal + shipping_cost + tax
#
#     def total_items(self) -> int:
#         return sum(item["quantity"] for item in self.items)
#
#     def clear_order(self):
#         self.items = []
#
#     def list_items(self) -> List[str]:
#         return list(set(item["name"] for item in self.items))
#
#     def is_empty(self) -> bool:
#         return len(self.items) == 0


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertEqual(self.calculator.items, [])

    def test_init_custom_values(self):
        calculator = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.1)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.1")

    def test_init_invalid_free_shipping_threshold_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="50")

    def test_init_invalid_shipping_cost_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10")

    def test_init_invalid_tax_rate_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_free_shipping_threshold_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_value(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        self.calculator.add_item("Product", 10.0, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Product")
        self.assertEqual(self.calculator.items[0]["price"], 10.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 2)

    def test_add_item_default_quantity(self):
        self.calculator.add_item("Product", 10.0)
        self.assertEqual(self.calculator.items[0]["quantity"], 1)

    def test_add_existing_item_same_price(self):
        self.calculator.add_item("Product", 10.0, 2)
        self.calculator.add_item("Product", 10.0, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["quantity"], 5)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Product", "10.0")

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item("Product", 10.0, "2")

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 10.0)

    def test_add_item_invalid_quantity_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Product", 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Product", 10.0, -1)

    def test_add_item_invalid_price_value(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Product", 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Product", -10.0)

    def test_add_item_same_name_different_price(self):
        self.calculator.add_item("Product", 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Product", 15.0)

    def test_remove_item_valid(self):
        self.calculator.add_item("Product1", 10.0)
        self.calculator.add_item("Product2", 20.0)
        self.calculator.remove_item("Product1")
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Product2")

    def test_remove_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_remove_nonexistent_item(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("NonexistentProduct")

    def test_get_subtotal_valid(self):
        self.calculator.add_item("Product1", 10.0, 2)
        self.calculator.add_item("Product2", 15.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 65.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100", 0.2)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "0.2")

    def test_apply_discount_invalid_discount_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_subtotal_value(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(200.0), 0.0)

    def test_calculate_shipping_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("100")

    def test_calculate_tax_valid(self):
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("100")

    def test_calculate_tax_invalid_amount_value(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item("Product", 50.0)
        # Subtotal: 50.0
        # Discount: 0.0 (default)
        # Discounted subtotal: 50.0
        # Shipping: 10.0 (below threshold)
        # Tax: (50.0 + 10.0) * 0.23 = 13.8
        # Total: 50.0 + 10.0 + 13.8 = 73.8
        self.assertEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Product", 200.0)
        # Subtotal: 200.0
        # Discount: 0.2 (20%)
        # Discounted subtotal: 160.0
        # Shipping: 0.0 (above threshold)
        # Tax: 160.0 * 0.23 = 36.8
        # Total: a60.0 + 0.0 + 36.8 = 196.8
        self.assertEqual(self.calculator.calculate_total(0.2), 196.8)

    def test_calculate_total_free_shipping_edge(self):
        self.calculator.add_item("Product", 100.0)
        # Subtotal: 100.0
        # Discounted subtotal: 100.0
        # Shipping: 0.0 (equal to threshold)
        # Tax: 100.0 * 0.23 = 23.0
        # Total: 100.0 + 0.0 + 23.0 = 123.0
        self.assertEqual(self.calculator.calculate_total(), 123.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item("Product", 50.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("0.2")

    def test_total_items_multiple_products(self):
        self.calculator.add_item("Product1", 10.0, 2)
        self.calculator.add_item("Product2", 15.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty_order(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        self.calculator.add_item("Product1", 10.0)
        self.calculator.add_item("Product2", 15.0)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items(self):
        self.calculator.add_item("Product1", 10.0)
        self.calculator.add_item("Product2", 15.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn("Product1", items)
        self.assertIn("Product2", items)

    def test_list_items_empty_order(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_duplicates(self):
        self.calculator.add_item("Product1", 10.0, 2)
        self.calculator.add_item("Product1", 10.0, 3)  # Updates quantity, not a duplicate
        self.calculator.add_item("Product2", 15.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item("Product", 10.0)
        self.assertFalse(self.calculator.is_empty())


if __name__ == "__main__":
    unittest.main()