import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Initialize a standard calculator before each test."""
        self.calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        """Test initialization with default values (implicit check via behavior) and custom values."""
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        custom_calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(custom_calc.is_empty())

    def test_add_item_valid(self):
        """Test adding valid items."""
        self.calc.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 10.0)
        self.calc.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(self.calc.get_subtotal(), 13.0)

    def test_add_item_existing_update(self):
        """Test adding an item that already exists updates the quantity/price."""
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Apple', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_add_item_invalid_inputs(self):
        """Test adding items with invalid prices or quantities."""
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('NegativeQty', 5.0, -1)

    def test_apply_discount(self):
        """Test discount logic helper."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.1)
        self.assertEqual(discounted, 90.0)
        self.assertEqual(self.calc.apply_discount(subtotal, 0.0), 100.0)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost when below threshold."""
        subtotal = 50.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test free shipping when above threshold."""
        subtotal = 150.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        """Test shipping at exact threshold boundary."""
        subtotal = 100.0
        self.assertEqual(self.calc.calculate_shipping(subtotal), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        amount = 100.0
        self.assertEqual(self.calc.calculate_tax(amount), 23.0)

    def test_calculate_total_simple(self):
        """Test total calculation without discount, below free shipping."""
        self.calc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(), 123.0)

    def test_calculate_total_with_shipping(self):
        """Test total with shipping costs."""
        self.calc.add_item('Item', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertTrue(total > 50.0)
        self.assertIsInstance(total, float)

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 10, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_list_items(self):
        """Test listing item names."""
        self.calc.add_item('Apple', 1, 1)
        self.calc.add_item('Banana', 1, 1)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        """Test empty check."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1, 1)
        self.assertFalse(self.calc.is_empty())