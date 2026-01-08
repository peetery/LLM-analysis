import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        """Test initialization with custom tax, threshold, and shipping cost."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(calc.calculate_shipping(60.0), 0.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_add_item_valid(self):
        """Test adding items with valid inputs."""
        self.calculator.add_item('Laptop', 1000.0, 1)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 1000.0)

    def test_add_item_multiple_quantities(self):
        """Test adding multiple quantities of an item."""
        self.calculator.add_item('Mouse', 20.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 100.0)

    def test_add_item_default_quantity(self):
        """Test adding item uses default quantity of 1."""
        self.calculator.add_item('Keyboard', 50.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 50.0)

    def test_add_item_invalid_price(self):
        """Test adding item with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('Bad Price', -10.0)

    def test_add_item_invalid_quantity(self):
        """Test adding item with zero or negative quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('Zero Qty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Neg Qty', 10.0, -1)

    def test_remove_item(self):
        """Test removing an existing item."""
        self.calculator.add_item('Tablet', 300.0, 1)
        self.calculator.remove_item('Tablet')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises correct exception (KeyError or ValueError)."""
        with self.assertRaises((KeyError, ValueError)):
            self.calculator.remove_item('NonExistentItem')

    def test_get_subtotal_mixed_items(self):
        """Test subtotal calculation with multiple different items."""
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.0)

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        subtotal = 100.0
        discount = 10.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_invalid(self):
        """Test applying negative discount raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -5.0)

    def test_apply_discount_exceeds_subtotal(self):
        """Test discount larger than subtotal (should usually return 0 or raise error)."""
        result = self.calculator.apply_discount(50.0, 100.0)
        self.assertGreaterEqual(result, 0.0)

    def test_calculate_shipping_logic(self):
        """Test shipping cost logic based on threshold."""
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_logic(self):
        """Test tax calculation based on rate."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_workflow(self):
        """Test full total calculation flow."""
        self.calculator.add_item('Item1', 50.0)
        total = self.calculator.calculate_total()
        self.assertTrue(total > 50.0)

    def test_total_items_accumulated(self):
        """Test total item count accumulates correctly."""
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order resets all state."""
        self.calculator.add_item('Data', 100.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        """Test listing items returns a list of strings."""
        self.calculator.add_item('Book', 15.0)
        items = self.calculator.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertIsInstance(items[0], str)
        self.assertIn('Book', items[0])

    def test_is_empty_initial_and_after_add(self):
        """Test is_empty state transitions."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Pen', 1.0)
        self.assertFalse(self.calculator.is_empty())