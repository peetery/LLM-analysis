import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh instance for each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertEqual(calc.get_subtotal(), 0.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        """Test initialization with custom tax, threshold, and shipping."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Test Item', 100.0)
        self.assertAlmostEqual(calc.calculate_total(), 110.0)

    def test_add_item_valid(self):
        """Test adding a valid item."""
        self.calc.add_item('Book', 20.0, 1)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 20.0)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Pen', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_multiple_quantities(self):
        """Test adding an item with quantity > 1."""
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_update_existing(self):
        """Test adding the same item name updates quantity/price or adds separate entry.
        Assuming aggregation by name for standard shopping cart behavior."""
        self.calc.add_item('Apple', 2.0, 2)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_invalid_price(self):
        """Test adding item with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Item', -10.0)

    def test_add_item_invalid_quantity(self):
        """Test adding item with zero or negative quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Ghost Item', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Anti Item', 10.0, -1)

    def test_add_item_empty_name(self):
        """Test adding item with empty name raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calc.add_item('Laptop', 1000.0)
        self.calc.remove_item('Laptop')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        """Test removing a non-existent item raises Error or handles gracefully.
        Assuming KeyError or ValueError for non-existent items."""
        with self.assertRaises((KeyError, ValueError)):
            self.calc.remove_item('NonExistent')

    def test_get_subtotal(self):
        """Test subtotal calculation with multiple items."""
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_apply_discount(self):
        """Test discount calculation logic."""
        subtotal = 100.0
        discount_rate = 0.2
        expected = 80.0
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, discount_rate), expected)

    def test_apply_discount_zero(self):
        """Test 0 discount leaves subtotal unchanged."""
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost added when below threshold."""
        subtotal = 50.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test free shipping when above threshold."""
        subtotal = 150.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping behavior exactly at threshold (usually inclusive of free shipping)."""
        subtotal = 100.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        amount = 100.0
        self.assertAlmostEqual(self.calc.calculate_tax(amount), 23.0)

    def test_calculate_total_no_discount(self):
        """Test total calculation without discount."""
        self.calc.add_item('Item A', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        """Test total with discount that keeps it above free shipping."""
        self.calc.add_item('Expensive Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 221.4)

    def test_calculate_total_empty(self):
        """Test total of empty order is 0."""
        self.assertEqual(self.calc.calculate_total(), 0.0)

    def test_total_items(self):
        """Test total items count."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 10, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order resets everything."""
        self.calc.add_item('Stuff', 50.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_list_items(self):
        """Test listing items returns list of strings."""
        self.calc.add_item('Item 1', 10.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIn('Item 1', items[0])

    def test_is_empty(self):
        """Test is_empty state."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('I', 1)
        self.assertFalse(self.calc.is_empty())