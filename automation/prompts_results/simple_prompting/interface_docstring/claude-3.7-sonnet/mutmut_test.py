import unittest
from typing import TypedDict, List


class Item(TypedDict):
    """
    Represents a single product entry in the order.
    
    :key name: The name of the product.
    :key price: The price per unit of the product.
    :key quantity: The number of units of the product.
    """


class OrderCalculator:
    def __init__(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.
        
        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).
        
        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        pass
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.
        
        If an item with the same name and price already exists, its quantity is increased.
        
        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        pass
    
    def remove_item(self, name: str):
        """
        Removes an item from the order.
        
        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        pass
    
    def get_subtotal(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.
        
        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        pass
    
    def apply_discount(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.
        
        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        pass
    
    def calculate_shipping(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.
        
        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.
        
        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        pass
    
    def calculate_tax(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.
        
        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        pass
    
    def calculate_total(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.
        
        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.
        
        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        pass
    
    def total_items(self) -> int:
        """
        Returns the total quantity of all items in the order.
        
        :return: The sum of the quantities of all items.
        :return:
        """
        pass
    
    def clear_order(self):
        """
        Removes all items from the order, resetting it to an empty state.
        """
        pass
    
    def list_items(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.
        
        :return: A list of unique item names (no duplicates).
        """
        pass
    
    def is_empty(self) -> bool:
        """
        Checks whether the order is currently empty.
        
        :return: True if no items are in the order, False otherwise.
        """
        pass


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = OrderCalculator()
        self.calculator_custom = OrderCalculator(tax_rate=0.10, free_shipping_threshold=50.0, shipping_cost=5.0)
    
    def test_init_default_values(self):
        self.assertEqual(0.23, self.calculator._tax_rate)
        self.assertEqual(100.0, self.calculator._free_shipping_threshold)
        self.assertEqual(10.0, self.calculator._shipping_cost)
        self.assertEqual([], self.calculator._items)
    
    def test_init_custom_values(self):
        self.assertEqual(0.10, self.calculator_custom._tax_rate)
        self.assertEqual(50.0, self.calculator_custom._free_shipping_threshold)
        self.assertEqual(5.0, self.calculator_custom._shipping_cost)
    
    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
    
    def test_init_invalid_free_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-0.1)
    
    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-0.1)
    
    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100.0")
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10.0")
    
    def test_add_item_valid(self):
        self.calculator.add_item("Test Item", 10.0, 2)
        self.assertEqual(1, len(self.calculator._items))
        self.assertEqual("Test Item", self.calculator._items[0]["name"])
        self.assertEqual(10.0, self.calculator._items[0]["price"])
        self.assertEqual(2, self.calculator._items[0]["quantity"])
    
    def test_add_item_default_quantity(self):
        self.calculator.add_item("Test Item", 10.0)
        self.assertEqual(1, self.calculator._items[0]["quantity"])
    
    def test_add_item_same_name_same_price(self):
        self.calculator.add_item("Test Item", 10.0, 2)
        self.calculator.add_item("Test Item", 10.0, 3)
        self.assertEqual(1, len(self.calculator._items))
        self.assertEqual(5, self.calculator._items[0]["quantity"])
    
    def test_add_item_same_name_different_price(self):
        self.calculator.add_item("Test Item", 10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 20.0)
    
    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 10.0)
    
    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", -10.0)
    
    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Test Item", 10.0, -1)
    
    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Test Item", "10.0")
        with self.assertRaises(TypeError):
            self.calculator.add_item("Test Item", 10.0, 1.5)
    
    def test_remove_item_existing(self):
        self.calculator.add_item("Test Item", 10.0)
        self.calculator.remove_item("Test Item")
        self.assertEqual(0, len(self.calculator._items))
    
    def test_remove_item_nonexistent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Nonexistent Item")
    
    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)
    
    def test_get_subtotal_valid(self):
        self.calculator.add_item("Item 1", 10.0, 2)
        self.calculator.add_item("Item 2", 20.0, 1)
        self.assertEqual(40.0, self.calculator.get_subtotal())
    
    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()
    
    def test_apply_discount_valid(self):
        self.assertEqual(80.0, self.calculator.apply_discount(100.0, 0.2))
        self.assertEqual(100.0, self.calculator.apply_discount(100.0, 0.0))
        self.assertEqual(0.0, self.calculator.apply_discount(100.0, 1.0))
    
    def test_apply_discount_invalid_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-1.0, 0.2)
    
    def test_apply_discount_invalid_discount(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)
    
    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100.0", 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "0.2")
    
    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(10.0, self.calculator.calculate_shipping(99.9))
        self.assertEqual(5.0, self.calculator_custom.calculate_shipping(49.9))
    
    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(0.0, self.calculator.calculate_shipping(100.0))
        self.assertEqual(0.0, self.calculator.calculate_shipping(200.0))
        self.assertEqual(0.0, self.calculator_custom.calculate_shipping(50.0))
    
    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("100.0")
    
    def test_calculate_tax_valid(self):
        self.assertEqual(23.0, self.calculator.calculate_tax(100.0))
        self.assertEqual(10.0, self.calculator_custom.calculate_tax(100.0))
        self.assertEqual(0.0, self.calculator.calculate_tax(0.0))
    
    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)
    
    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("100.0")
    
    def test_calculate_total_no_discount(self):
        self.calculator.add_item("Item", 50.0, 1)
        # Subtotal: 50.0
        # Discounted: 50.0
        # Shipping: 10.0
        # Tax: (50.0 + 10.0) * 0.23 = 13.8
        # Total: 50.0 + 10.0 + 13.8 = 73.8
        self.assertEqual(73.8, self.calculator.calculate_total())
    
    def test_calculate_total_with_discount(self):
        self.calculator.add_item("Item", 50.0, 1)
        # Subtotal: 50.0
        # Discounted: 50.0 * (1 - 0.1) = 45.0
        # Shipping: 10.0
        # Tax: (45.0 + 10.0) * 0.23 = 12.65
        # Total: 45.0 + 10.0 + 12.65 = 67.65
        self.assertEqual(67.65, self.calculator.calculate_total(0.1))
    
    def test_calculate_total_free_shipping(self):
        self.calculator.add_item("Item", 150.0, 1)
        # Subtotal: 150.0
        # Discounted: 150.0
        # Shipping: 0.0 (free)
        # Tax: 150.0 * 0.23 = 34.5
        # Total: 150.0 + 0.0 + 34.5 = 184.5
        self.assertEqual(184.5, self.calculator.calculate_total())
    
    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()
    
    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item("Item", 50.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)
    
    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item("Item", 50.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("0.1")
    
    def test_total_items_single_item(self):
        self.calculator.add_item("Item", 10.0, 5)
        self.assertEqual(5, self.calculator.total_items())
    
    def test_total_items_multiple_items(self):
        self.calculator.add_item("Item 1", 10.0, 2)
        self.calculator.add_item("Item 2", 20.0, 3)
        self.assertEqual(5, self.calculator.total_items())
    
    def test_total_items_empty(self):
        self.assertEqual(0, self.calculator.total_items())
    
    def test_clear_order(self):
        self.calculator.add_item("Item", 10.0)
        self.calculator.clear_order()
        self.assertEqual(0, len(self.calculator._items))
    
    def test_list_items_empty(self):
        self.assertEqual([], self.calculator.list_items())
    
    def test_list_items_single(self):
        self.calculator.add_item("Item", 10.0)
        self.assertEqual(["Item"], self.calculator.list_items())
    
    def test_list_items_multiple(self):
        self.calculator.add_item("Item 1", 10.0)
        self.calculator.add_item("Item 2", 20.0)
        self.assertIn("Item 1", self.calculator.list_items())
        self.assertIn("Item 2", self.calculator.list_items())
        self.assertEqual(2, len(self.calculator.list_items()))
    
    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())
    
    def test_is_empty_false(self):
        self.calculator.add_item("Item", 10.0)
        self.assertFalse(self.calculator.is_empty())
    
    def test_is_empty_after_clear(self):
        self.calculator.add_item("Item", 10.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == "__main__":
    unittest.main()