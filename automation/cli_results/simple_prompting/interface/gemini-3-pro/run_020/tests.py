import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        c = OrderCalculator()
        self.assertTrue(c.is_empty())
        self.assertEqual(c.total_items(), 0)
        self.assertEqual(c.get_subtotal(), 0.0)

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        c = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(c.calculate_tax(100.0), 10.0)
        self.assertAlmostEqual(c.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(c.calculate_shipping(60.0), 0.0)

    def test_add_item_valid(self):
        """Test adding valid items."""
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertAlmostEqual(self.calc.get_subtotal(), 15.0)
        self.calc.add_item('Banana', 0.5, 5)
        self.assertEqual(self.calc.total_items(), 15)
        self.assertAlmostEqual(self.calc.get_subtotal(), 17.5)

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Orange', 2.0)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 2.0)

    def test_add_item_invalid_inputs(self):
        """Test adding items with invalid price or quantity."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Price', -5.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Quantity', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Quantity', 10.0, -1)

    def test_remove_item(self):
        """Test removing an item."""
        self.calc.add_item('Laptop', 1000.0, 1)
        self.calc.add_item('Mouse', 50.0, 1)
        self.calc.remove_item('Laptop')
        self.assertEqual(self.calc.total_items(), 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 50.0)
        self.assertEqual(self.calc.list_items(), ['Mouse'])

    def test_remove_non_existent_item(self):
        """Test removing an item that does not exist."""
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Ghost')

    def test_get_subtotal(self):
        """Test subtotal calculation."""
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 2)
        self.assertAlmostEqual(self.calc.get_subtotal(), 31.0)

    def test_apply_discount(self):
        """Test discount logic."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.2)
        self.assertAlmostEqual(discounted, 80.0)
        discounted = self.calc.apply_discount(subtotal, 0.0)
        self.assertAlmostEqual(discounted, 100.0)

    def test_apply_discount_invalid(self):
        """Test invalid discount values."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping(self):
        """Test shipping cost logic based on threshold."""
        self.assertAlmostEqual(self.calc.calculate_shipping(99.99), 10.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount(self):
        """Test total calculation without discount."""
        self.calc.add_item('Book', 50.0, 1)
        self.calc.add_item('Expensive Item', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_shipping(self):
        """Test total calculation including shipping."""
        self.calc.add_item('Cheap Item', 10.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 22.3)

    def test_calculate_total_with_discount(self):
        """Test total calculation with discount passed."""
        self.calc.add_item('Item', 100.0)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 120.7)

    def test_total_items(self):
        """Test total items count."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.calc.add_item('B', 1, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 10, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        """Test listing item names."""
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('Apple', 1, 1)
        self.calc.add_item('Banana', 1, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1)
        self.assertFalse(self.calc.is_empty())