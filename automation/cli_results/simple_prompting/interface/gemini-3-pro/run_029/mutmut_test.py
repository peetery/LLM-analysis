import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance for each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default parameter values."""
        self.assertAlmostEqual(self.calc.tax_rate, 0.23)
        self.assertAlmostEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(self.calc.shipping_cost, 10.0)
        self.assertTrue(self.calc.is_empty())

    def test_init_custom_values(self):
        """Test initialization with custom parameter values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.tax_rate, 0.1)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calc.shipping_cost, 5.0)

    def test_add_item_valid(self):
        """Test adding a valid item."""
        self.calc.add_item('Widget', 10.0, 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 20.0)

    def test_add_item_defaults(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Gadget', 15.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 15.0)

    def test_add_item_invalid_price(self):
        """Test that adding an item with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Price', -5.0)

    def test_add_item_invalid_quantity(self):
        """Test that adding an item with non-positive quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Qty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Qty', 10.0, -1)

    def test_add_item_empty_name(self):
        """Test that adding an item with an empty name raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_remove_item_non_existent(self):
        """Test that removing a non-existent item raises an error (KeyError or ValueError)."""
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('Ghost Item')

    def test_get_subtotal_multiple_items(self):
        """Test subtotal calculation with multiple items."""
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount(self):
        """Test applying a discount to a subtotal."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(discounted, 80.0)

    def test_apply_discount_invalid(self):
        """Test that invalid discount values raise ValueError."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost when subtotal is below threshold."""
        cost = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping cost when subtotal is exactly at threshold."""
        cost = self.calc.calculate_shipping(100.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping cost when subtotal is above threshold."""
        cost = self.calc.calculate_shipping(150.0)
        self.assertAlmostEqual(cost, 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_total_simple(self):
        """Test total calculation with no discount and shipping applied."""
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        """Test total calculation with discount that qualifies for free shipping."""
        self.calc.add_item('Expensive', 200.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_total_items_count(self):
        """Test counting total number of items (sum of quantities)."""
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_list_items(self):
        """Test listing items returns a list of strings."""
        self.calc.add_item('Apple', 1.5, 2)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], str)
        self.assertIn('Apple', items[0])

    def test_is_empty_state(self):
        """Test is_empty reflects state correctly."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Thing', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Thing')
        self.assertTrue(self.calc.is_empty())