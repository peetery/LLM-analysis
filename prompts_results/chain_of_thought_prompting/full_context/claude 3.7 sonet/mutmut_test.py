import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator


# class Item(TypedDict):
#     """
#     Represents a single product entry in the order.
#
#     :key name: The name of the product.
#     :key price: The price per unit of the product.
#     :key quantity: The number of units of the product.
#     """
#     name: str
#     price: float
#     quantity: int
#
#
# class OrderCalculator:
#     def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
#         """
#         Initializes a new OrderCalculator instance.
#         Initializes an empty list of items (each represented as a TypedDict 'Item')
#         and stores the configured tax and shipping parameters.
#
#         :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
#         :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
#         :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).
#
#         :raises ValueError:
#             - If tax_rate is not in the range [0.0, 1.0].
#             - If free_shipping_threshold is negative.
#             - If shipping_cost is negative.
#         :raises TypeError: If any parameter is of incorrect type.
#         """
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
#         """
#         Add an item to the order.
#
#         If an item with the same name and price already exists, its quantity is increased.
#
#         :param name: the name of the item
#         :param price: the price of the item
#         :param quantity: the quantity of the item (default is 1)
#         :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
#         :raises TypeError: If inputs are of incorrect types.
#         """
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
#         """
#         Removes an item from the order.
#
#         :param name: The name of the item to remove.
#         :raises ValueError: If no item with the given name exists in the order.
#         :raises TypeError: If name is not a string.
#         """
#         if not isinstance(name, str):
#             raise TypeError("Item name must be a string.")
#         if not any(item["name"] == name for item in self.items):
#             raise ValueError(f"Item with name '{name}' does not exist in the order.")
#
#         self.items = [item for item in self.items if item["name"] != name]
#
#     def get_subtotal(self) -> float:
#         """
#         Calculates the subtotal (sum of item prices times their quantities) for all items in the order.
#
#         :return: The subtotal as a float.
#         :raises ValueError: If the order is empty.
#         """
#         if not self.items:
#             raise ValueError("Cannot calculate subtotal on empty order.")
#         return sum(item["price"] * item["quantity"] for item in self.items)
#
#     def apply_discount(self, subtotal: float, discount: float) -> float:
#         """
#         Applies a percentage discount to the given subtotal.
#
#         :param subtotal: the subtotal amount (must be >= 0)
#         :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
#         :return: The discounted subtotal.
#         :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
#         :raises TypeError: If inputs are of incorrect types.
#         """
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
#         """
#         Calculates the shipping cost based on the discounted subtotal.
#
#         If the discounted subtotal >= free shipping threshold shipping is free (0.0).
#         Otherwise, the standard shipping cost is applied.
#
#         :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
#         :return: The shipping cost as a float (0.0 or self.shipping_cost).
#         :raises TypeError: If input is not a number.
#         """
#         if not isinstance(discounted_subtotal, (float, int)):
#             raise TypeError("Discounted subtotal must be a number.")
#         if discounted_subtotal >= self.free_shipping_threshold:
#             return 0.0
#         return self.shipping_cost
#
#     def calculate_tax(self, amount: float) -> float:
#         """
#         Calculates the tax based on the provided amount using the configured tax rate.
#
#         :param amount: The amount on which to calculate the tax (must be >= 0.0).
#         :return: The tax as a float.
#         :raises ValueError: If the amount is negative.
#         :raises TypeError: If input is not a number.
#         """
#         if not isinstance(amount, (float, int)):
#             raise TypeError("Amount must be a number.")
#         if amount < 0.0:
#             raise ValueError("Cannot calculate tax on negative amount.")
#         return amount * self.tax_rate
#
#     def calculate_total(self, discount: float = 0.0) -> float:
#         """
#         Calculates the total cost of the order after applying discount, shipping, and tax.
#
#         This method performs the following steps:
#         1. Calculates the subtotal from all items.
#         2. Applies the given discount.
#         3. Adds shipping cost if necessary.
#         4. Calculates tax on the discounted subtotal + shipping.
#
#         :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
#         :return: The final total as a float.
#         :raises ValueError:
#             - If the subtotal is negative.
#             - If the discount is invalid.
#             - If the order is empty.
#         :raises TypeError: If input is not a number.
#         """
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
#         """
#         Returns the total quantity of all items in the order.
#
#         :return: The sum of the quantities of all items.
#         :return:
#         """
#         return sum(item["quantity"] for item in self.items)
#
#     def clear_order(self):
#         """
#         Removes all items from the order, resetting it to an empty state.
#         """
#         self.items = []
#
#     def list_items(self) -> List[str]:
#         """
#         Returns a list of all unique item names currently in the order.
#
#         :return: A list of unique item names (no duplicates).
#         """
#         return list(set(item["name"] for item in self.items))
#
#     def is_empty(self) -> bool:
#         """
#         Checks whether the order is currently empty.
#
#         :return: True if no items are in the order, False otherwise.
#         """
#         return len(self.items) == 0


class TestOrderCalculator(unittest.TestCase):
    """Test cases for the OrderCalculator class."""

    def setUp(self):
        """Set up a new OrderCalculator instance for each test."""
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        """Test that the constructor initializes with correct default values."""
        self.assertEqual(0.23, self.calc.tax_rate)
        self.assertEqual(100.0, self.calc.free_shipping_threshold)
        self.assertEqual(10.0, self.calc.shipping_cost)
        self.assertEqual([], self.calc.items)

    def test_init_custom_values(self):
        """Test that the constructor accepts and sets custom values."""
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(0.1, custom_calc.tax_rate)
        self.assertEqual(50.0, custom_calc.free_shipping_threshold)
        self.assertEqual(5.0, custom_calc.shipping_cost)

    def test_init_invalid_tax_rate_type(self):
        """Test that constructor raises TypeError for invalid tax_rate type."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")

    def test_init_invalid_free_shipping_threshold_type(self):
        """Test that constructor raises TypeError for invalid free_shipping_threshold type."""
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100.0")

    def test_init_invalid_shipping_cost_type(self):
        """Test that constructor raises TypeError for invalid shipping_cost type."""
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10.0")

    def test_init_tax_rate_out_of_range(self):
        """Test that constructor raises ValueError for tax_rate out of valid range."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_free_shipping_threshold(self):
        """Test that constructor raises ValueError for negative free_shipping_threshold."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping_cost(self):
        """Test that constructor raises ValueError for negative shipping_cost."""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_basic(self):
        """Test adding a single item to an empty order."""
        self.calc.add_item("Product", 10.0, 2)
        self.assertEqual(1, len(self.calc.items))
        self.assertEqual("Product", self.calc.items[0]["name"])
        self.assertEqual(10.0, self.calc.items[0]["price"])
        self.assertEqual(2, self.calc.items[0]["quantity"])

    def test_add_item_default_quantity(self):
        """Test that add_item uses default quantity of 1 if not specified."""
        self.calc.add_item("Product", 10.0)
        self.assertEqual(1, self.calc.items[0]["quantity"])

    def test_add_item_existing_item_same_price(self):
        """Test that adding an existing item with same price increases its quantity."""
        self.calc.add_item("Product", 10.0, 2)
        self.calc.add_item("Product", 10.0, 3)
        self.assertEqual(1, len(self.calc.items))
        self.assertEqual(5, self.calc.items[0]["quantity"])

    def test_add_item_same_name_different_price(self):
        """Test that adding an item with same name but different price raises ValueError."""
        self.calc.add_item("Product", 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item("Product", 15.0)

    def test_add_item_empty_name(self):
        """Test that adding an item with empty name raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item("", 10.0)

    def test_add_item_zero_price(self):
        """Test that adding an item with zero price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item("Product", 0.0)

    def test_add_item_negative_price(self):
        """Test that adding an item with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item("Product", -10.0)

    def test_add_item_zero_quantity(self):
        """Test that adding an item with zero quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item("Product", 10.0, 0)

    def test_add_item_negative_quantity(self):
        """Test that adding an item with negative quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item("Product", 10.0, -1)

    def test_add_item_invalid_name_type(self):
        """Test that add_item raises TypeError for invalid name type."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_invalid_price_type(self):
        """Test that add_item raises TypeError for invalid price type."""
        with self.assertRaises(TypeError):
            self.calc.add_item("Product", "10.0")

    def test_add_item_invalid_quantity_type(self):
        """Test that add_item raises TypeError for invalid quantity type."""
        with self.assertRaises(TypeError):
            self.calc.add_item("Product", 10.0, 1.5)

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calc.add_item("Product1", 10.0)
        self.calc.add_item("Product2", 20.0)
        self.calc.remove_item("Product1")
        self.assertEqual(1, len(self.calc.items))
        self.assertEqual("Product2", self.calc.items[0]["name"])

    def test_remove_item_nonexistent(self):
        """Test that removing a nonexistent item raises ValueError."""
        self.calc.add_item("Product", 10.0)
        with self.assertRaises(ValueError):
            self.calc.remove_item("NonexistentProduct")

    def test_remove_item_invalid_name_type(self):
        """Test that remove_item raises TypeError for invalid name type."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_basic(self):
        """Test basic subtotal calculation with multiple items."""
        self.calc.add_item("Product1", 10.0, 2)  # 10.0 * 2 = 20.0
        self.calc.add_item("Product2", 15.0, 3)  # 15.0 * 3 = 45.0
        self.assertEqual(65.0, self.calc.get_subtotal())  # 20.0 + 45.0 = 65.0

    def test_get_subtotal_empty_order(self):
        """Test that getting subtotal on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_zero(self):
        """Test applying zero discount."""
        self.assertEqual(100.0, self.calc.apply_discount(100.0, 0.0))

    def test_apply_discount_partial(self):
        """Test applying partial discount."""
        self.assertEqual(80.0, self.calc.apply_discount(100.0, 0.2))

    def test_apply_discount_full(self):
        """Test applying full discount."""
        self.assertEqual(0.0, self.calc.apply_discount(100.0, 1.0))

    def test_apply_discount_invalid_subtotal_type(self):
        """Test that apply_discount raises TypeError for invalid subtotal type."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount("100.0", 0.2)

    def test_apply_discount_invalid_discount_type(self):
        """Test that apply_discount raises TypeError for invalid discount type."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, "0.2")

    def test_apply_discount_negative_subtotal(self):
        """Test that apply_discount raises ValueError for negative subtotal."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_apply_discount_negative_discount(self):
        """Test that apply_discount raises ValueError for negative discount."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.2)

    def test_apply_discount_excessive_discount(self):
        """Test that apply_discount raises ValueError for discount > 1.0."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping calculation when subtotal is below free shipping threshold."""
        self.assertEqual(10.0, self.calc.calculate_shipping(99.0))

    def test_calculate_shipping_at_threshold(self):
        """Test shipping calculation when subtotal is exactly at free shipping threshold."""
        self.assertEqual(0.0, self.calc.calculate_shipping(100.0))

    def test_calculate_shipping_above_threshold(self):
        """Test shipping calculation when subtotal is above free shipping threshold."""
        self.assertEqual(0.0, self.calc.calculate_shipping(101.0))

    def test_calculate_shipping_invalid_type(self):
        """Test that calculate_shipping raises TypeError for invalid discounted_subtotal type."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping("100.0")

    def test_calculate_tax_zero_amount(self):
        """Test tax calculation with zero amount."""
        self.assertEqual(0.0, self.calc.calculate_tax(0.0))

    def test_calculate_tax_positive_amount(self):
        """Test tax calculation with positive amount."""
        self.assertEqual(23.0, self.calc.calculate_tax(100.0))  # 100.0 * 0.23 = 23.0

    def test_calculate_tax_custom_rate(self):
        """Test tax calculation with custom tax rate."""
        custom_calc = OrderCalculator(tax_rate=0.1)
        self.assertEqual(10.0, custom_calc.calculate_tax(100.0))  # 100.0 * 0.1 = 10.0

    def test_calculate_tax_invalid_type(self):
        """Test that calculate_tax raises TypeError for invalid amount type."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax("100.0")

    def test_calculate_tax_negative_amount(self):
        """Test that calculate_tax raises ValueError for negative amount."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-100.0)

    def test_calculate_total_no_discount_below_threshold(self):
        """Test total calculation with no discount and subtotal below free shipping threshold."""
        self.calc.add_item("Product", 50.0, 1)  # Subtotal: 50.0
        # Discounted: 50.0, Shipping: 10.0, Tax: (50.0 + 10.0) * 0.23 = 13.8, Total: 50.0 + 10.0 + 13.8 = 73.8
        self.assertAlmostEqual(73.8, self.calc.calculate_total(), places=9)

    def test_calculate_total_with_discount_below_threshold(self):
        """Test total calculation with discount and subtotal below free shipping threshold."""
        self.calc.add_item("Product", 50.0, 1)  # Subtotal: 50.0
        # Discounted: 50.0 * 0.8 = 40.0, Shipping: 10.0, Tax: (40.0 + 10.0) * 0.23 = 11.5, Total: 40.0 + 10.0 + 11.5 = 61.5
        self.assertAlmostEqual(61.5, self.calc.calculate_total(0.2), places=9)

    def test_calculate_total_no_discount_above_threshold(self):
        """Test total calculation with no discount and subtotal above free shipping threshold."""
        self.calc.add_item("Product", 150.0, 1)  # Subtotal: 150.0
        # Discounted: 150.0, Shipping: 0.0, Tax: 150.0 * 0.23 = 34.5, Total: 150.0 + 0.0 + 34.5 = 184.5
        self.assertAlmostEqual(184.5, self.calc.calculate_total(), places=9)

    def test_calculate_total_with_discount_above_to_below_threshold(self):
        """Test total calculation with discount that brings subtotal from above to below threshold."""
        self.calc.add_item("Product", 150.0, 1)  # Subtotal: 150.0
        # Discounted: 150.0 * 0.5 = 75.0, Shipping: 10.0, Tax: (75.0 + 10.0) * 0.23 = 19.55, Total: 75.0 + 10.0 + 19.55 = 104.55
        self.assertAlmostEqual(104.55, self.calc.calculate_total(0.5), places=9)

    def test_calculate_total_empty_order(self):
        """Test that calculate_total raises ValueError for empty order."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test that calculate_total raises TypeError for invalid discount type."""
        self.calc.add_item("Product", 50.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total("0.2")

    def test_total_items_empty_order(self):
        """Test that total_items returns 0 for empty order."""
        self.assertEqual(0, self.calc.total_items())

    def test_total_items_single_item(self):
        """Test total_items with a single item."""
        self.calc.add_item("Product", 10.0, 5)
        self.assertEqual(5, self.calc.total_items())

    def test_total_items_multiple_items(self):
        """Test total_items with multiple items."""
        self.calc.add_item("Product1", 10.0, 2)
        self.calc.add_item("Product2", 20.0, 3)
        self.assertEqual(5, self.calc.total_items())  # 2 + 3 = 5

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item("Product", 10.0)
        self.calc.clear_order()
        self.assertEqual([], self.calc.items)

    def test_list_items_empty_order(self):
        """Test listing items in empty order."""
        self.assertEqual([], self.calc.list_items())

    def test_list_items_multiple_items(self):
        """Test listing multiple items."""
        self.calc.add_item("Product1", 10.0)
        self.calc.add_item("Product2", 20.0)
        items = self.calc.list_items()
        self.assertEqual(2, len(items))
        self.assertIn("Product1", items)
        self.assertIn("Product2", items)

    def test_is_empty_true(self):
        """Test that is_empty returns True for empty order."""
        self.assertTrue(self.calc.is_empty())

    def test_is_empty_false(self):
        """Test that is_empty returns False for non-empty order."""
        self.calc.add_item("Product", 10.0)
        self.assertFalse(self.calc.is_empty())


if __name__ == "__main__":
    unittest.main()