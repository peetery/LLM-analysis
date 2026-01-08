import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        """Test initialization with custom tax, threshold, and shipping cost."""
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        custom_calc.add_item('Test', 40.0)
        self.assertEqual(custom_calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(custom_calc.calculate_tax(40.0), 4.0)

    def test_add_item_valid(self):
        """Test adding valid items updates subtotal and quantity correctly."""
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 15.0)
        self.calc.add_item('Banana', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 15)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.0)

    def test_add_item_default_quantity(self):
        """Test adding an item uses default quantity of 1."""
        self.calc.add_item('Orange', 3.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 3.0)

    def test_add_item_invalid_inputs(self):
        """Test that adding items with invalid inputs raises appropriate errors."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', -5.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Item', 5.0, -1)

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Banana', 2.0, 3)
        self.calc.remove_item('Apple')
        self.assertEqual(self.calc.total_items(), 3)
        self.assertAlmostEqual(self.calc.get_subtotal(), 6.0)
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_non_existent(self):
        """Test that removing a non-existent item raises an error."""
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('NonExistentItem')

    def test_get_subtotal(self):
        """Test subtotal calculation."""
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount_valid(self):
        """Test applying a valid percentage discount."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(discounted, 80.0)
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(subtotal, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        """Test that invalid discount rates raise errors."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping(self):
        """Test shipping cost logic based on threshold."""
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation based on tax rate."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        """Test total calculation without discount."""
        self.calc.add_item('Item1', 50.0)
        self.calc.add_item('Item2', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_with_discount_and_shipping(self):
        """Test total calculation where discount triggers shipping cost."""
        self.calc.add_item('Item1', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.2), 108.4)

    def test_total_items(self):
        """Test counting total number of items."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1, 5)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.calc.remove_item('A')
        self.assertEqual(self.calc.total_items(), 3)

    def test_clear_order(self):
        """Test clearing the order resets all state."""
        self.calc.add_item('A', 10.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items(self):
        """Test listing item names."""
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Pear', 2.0)
        items = self.calc.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Pear', items)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())