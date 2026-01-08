import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_initial_state(self):
        """Test that a new calculator is empty and has zero totals."""
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_add_item_valid(self):
        """Test adding valid items updates subtotal and item count."""
        self.calculator.add_item('Apple', 2.5, 2)
        self.assertFalse(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity (1)."""
        self.calculator.add_item('Book', 15.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)

    def test_add_item_accumulates(self):
        """Test that adding multiple items accumulates correctly."""
        self.calculator.add_item('Pencil', 1.0, 5)
        self.calculator.add_item('Eraser', 2.0, 2)
        self.assertEqual(self.calculator.total_items(), 7)
        self.assertEqual(self.calculator.get_subtotal(), 9.0)

    def test_add_item_invalid_price(self):
        """Test that adding an item with negative price raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('InvalidItem', -5.0)

    def test_add_item_invalid_quantity(self):
        """Test that adding an item with non-positive quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('ZeroQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('NegQty', 10.0, -1)

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calculator.add_item('Mouse', 20.0)
        self.calculator.remove_item('Mouse')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        """Test removing an item that does not exist raises an error (KeyError or ValueError)."""
        with self.assertRaises((KeyError, ValueError)):
            self.calculator.remove_item('GhostItem')

    def test_apply_discount_valid(self):
        """Test applying a valid discount amount."""
        subtotal = 100.0
        discount = 10.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 90.0)

    def test_apply_discount_exceeds_subtotal(self):
        """Test that discount cannot reduce total below zero."""
        subtotal = 50.0
        discount = 60.0
        result = self.calculator.apply_discount(subtotal, discount)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        """Test that negative discount raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -5.0)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost is applied when below threshold."""
        shipping = self.calculator.calculate_shipping(99.99)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping is free when above threshold."""
        shipping = self.calculator.calculate_shipping(100.01)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping is free exactly at the threshold."""
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_tax(self):
        """Test tax calculation based on tax rate."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_total_simple(self):
        """Test full total calculation without discount."""
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)

    def test_calculate_total_with_free_shipping(self):
        """Test total calculation when threshold is met."""
        self.calculator.add_item('ExpensiveItem', 200.0)
        total = self.calculator.calculate_total()
        expected_total_approx = 200.0 * 1.23
        self.assertAlmostEqual(total, expected_total_approx, places=2)

    def test_calculate_total_with_discount(self):
        """Test total calculation with a discount."""
        self.calculator.add_item('Item', 100.0)
        total = self.calculator.calculate_total(discount=20.0)
        self.assertIsInstance(total, float)
        self.assertLess(total, self.calculator.calculate_total(discount=0.0))

    def test_list_items(self):
        """Test listing item names."""
        self.calculator.add_item('Alpha', 10.0)
        self.calculator.add_item('Beta', 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Alpha', items)
        self.assertIn('Beta', items)

    def test_clear_order(self):
        """Test clearing the order resets all state."""
        self.calculator.add_item('Data', 55.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_negative_discount_in_total(self):
        """Test that calculate_total handles negative discount input as error."""
        self.calculator.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-10.0)