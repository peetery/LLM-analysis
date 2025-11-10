from order_calculator import OrderCalculator, Item

import unittest
from typing import TypedDict, List

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a new OrderCalculator instance before each test."""
        self.calculator = OrderCalculator()

    def test_initialization_defaults(self):
        """Test constructor with default values."""
        self.assertEqual(self.calculator.tax_rate, 0.23)
        self.assertEqual(self.calculator.free_shipping_threshold, 100.0)
        self.assertEqual(self.calculator.shipping_cost, 10.0)
        self.assertTrue(self.calculator.is_empty())

    def test_initialization_custom_values(self):
        """Test constructor with custom values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 200.0)
        self.assertEqual(calc.shipping_cost, 15.0)

    def test_initialization_invalid_tax_rate(self):
        """Test constructor with an invalid tax rate."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_initialization_invalid_shipping_values(self):
        """Test constructor with invalid shipping values."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-50)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5)

    def test_add_item_single(self):
        """Test adding a single item."""
        self.calculator.add_item('Laptop', 1200.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_multiple_quantity(self):
        """Test adding an item with a quantity greater than one."""
        self.calculator.add_item('Mouse', 25.0, quantity=3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_updates_quantity(self):
        """Test that adding an existing item updates its quantity."""
        self.calculator.add_item('Book', 15.0, quantity=1)
        self.calculator.add_item('Book', 15.0, quantity=2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(len(self.calculator.items), 1)

    def test_add_item_invalid_price(self):
        """Test adding an item with a negative price."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid Item', -10.0)

    def test_add_item_invalid_quantity(self):
        """Test adding an item with zero or negative quantity."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid Item', 10.0, quantity=0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Invalid Item', 10.0, quantity=-1)

    def test_remove_item_existing(self):
        """Test removing an item that exists in the order."""
        self.calculator.add_item('Keyboard', 75.0)
        self.calculator.remove_item('Keyboard')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existing(self):
        """Test removing an item that does not exist."""
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Non-existent Item')

    def test_get_subtotal_empty(self):
        """Test subtotal of an empty order."""
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_with_items(self):
        """Test subtotal with multiple items."""
        self.calculator.add_item('Apple', 0.5, quantity=5)
        self.calculator.add_item('Banana', 0.3, quantity=3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.4)

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 10.0), 90.0)

    def test_apply_discount_zero(self):
        """Test applying a zero discount."""
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_larger_than_subtotal(self):
        """Test applying a discount larger than the subtotal."""
        self.assertAlmostEqual(self.calculator.apply_discount(50.0, 60.0), 0.0)

    def test_apply_discount_invalid(self):
        """Test applying a negative discount."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost when subtotal is below the free shipping threshold."""
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping cost when subtotal is exactly at the threshold."""
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping cost when subtotal is above the threshold."""
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_items(self):
        """Test total for an empty order."""
        self.assertEqual(self.calculator.calculate_total(), 0.0)

    def test_calculate_total_with_shipping_no_discount(self):
        """Test total for an order that requires shipping and has no discount."""
        self.calculator.add_item('Item A', 50.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_free_shipping_no_discount(self):
        """Test total for an order with free shipping and no discount."""
        self.calculator.add_item('Item B', 120.0)
        self.assertAlmostEqual(self.calculator.calculate_total(), 147.6)

    def test_calculate_total_with_discount_and_shipping(self):
        """Test total with a discount that still requires shipping."""
        self.calculator.add_item('Item C', 80.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=10.0), 98.4)

    def test_calculate_total_with_discount_and_free_shipping(self):
        """Test total with a discount but still qualifying for free shipping."""
        self.calculator.add_item('Item D', 150.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=20.0), 159.9)

    def test_calculate_total_with_discount_losing_free_shipping(self):
        """Test total where a discount causes shipping to be added."""
        self.calculator.add_item('Item E', 110.0)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=20.0), 123.0)

    def test_total_items(self):
        """Test the total count of all items."""
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 1, quantity=5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.calculator.add_item('B', 1, quantity=2)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_clear_order(self):
        """Test clearing all items from the order."""
        self.calculator.add_item('Item A', 10.0)
        self.calculator.add_item('Item B', 20.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty(self):
        """Test listing items in an empty order."""
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_with_content(self):
        """Test listing items in a populated order."""
        self.calculator.add_item('Apple', 0.5, quantity=2)
        self.calculator.add_item('Bread', 3.5, quantity=1)
        items_list = self.calculator.list_items()
        self.assertEqual(len(items_list), 2)
        self.assertIn('Apple (x2) - $0.50 each', items_list)
        self.assertIn('Bread (x1) - $3.50 each', items_list)

    def test_is_empty(self):
        """Test the is_empty method."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Test Item', 1.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())