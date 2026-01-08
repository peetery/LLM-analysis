import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_add_item_valid(self):
        """Test adding valid items."""
        self.calculator.add_item('Apple', 2.5, 4)
        self.calculator.add_item('Banana', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 6)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 12.0)
        self.assertFalse(self.calculator.is_empty())
        self.assertIn('Apple', self.calculator.list_items())
        self.assertIn('Banana', self.calculator.list_items())

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calculator.add_item('Orange', 3.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_invalid_inputs(self):
        """Test adding items with invalid inputs raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Price', -5.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Qty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Qty Negative', 10.0, -1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0)

    def test_remove_item_non_existing(self):
        """Test removing an item that does not exist raises error."""
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Ghost')

    def test_get_subtotal(self):
        """Test subtotal calculation."""
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.5, 2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 31.0)

    def test_apply_discount(self):
        """Test discount application logic (assuming discount is a percentage 0.0-1.0)."""
        subtotal = 100.0
        discounted = self.calculator.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(discounted, 80.0)
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_invalid(self):
        """Test invalid discount values."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost when subtotal is below threshold."""
        self.assertEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping cost when subtotal is above threshold (free shipping)."""
        self.assertEqual(self.calculator.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        """Test shipping cost when subtotal equals threshold (edge case)."""
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_free_shipping_after_discount(self):
        """Test case where discounted total still qualifies for free shipping."""
        self.calculator.add_item('Expensive', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.25), 180.0)

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 1)
        self.calculator.add_item('B', 10, 5)
        self.assertEqual(self.calculator.total_items(), 6)

    def test_list_items(self):
        """Test listing item names."""
        self.calculator.add_item('Apple', 1, 1)
        self.calculator.add_item('Banana', 2, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        """Test checking if order is empty."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1)
        self.assertFalse(self.calculator.is_empty())