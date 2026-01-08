import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('Item', 100.0)
        self.assertEqual(calc.calculate_total(), 110.0)

    def test_add_item_valid(self):
        """Test adding valid items."""
        self.calculator.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calculator.total_items(), 4)
        self.assertEqual(self.calculator.get_subtotal(), 10.0)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_multiple(self):
        """Test adding multiple different items."""
        self.calculator.add_item('Apple', 2.0, 1)
        self.calculator.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 8.0)

    def test_add_item_invalid_input(self):
        """Test adding items with invalid input (negative price/quantity)."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -5.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 5.0, -1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('BadType', 'Expensive')

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calculator.add_item('Apple', 2.0)
        self.calculator.add_item('Banana', 3.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertNotIn('Apple', self.calculator.list_items())
        self.assertIn('Banana', self.calculator.list_items())
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_remove_item_non_existent(self):
        """Test removing an item that does not exist."""
        self.calculator.add_item('Apple', 2.0)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_apply_discount(self):
        """Test discount application logic."""
        subtotal = 100.0
        discount_rate = 0.2
        expected = 80.0
        self.assertEqual(self.calculator.apply_discount(subtotal, discount_rate), expected)

    def test_apply_discount_invalid(self):
        """Test apply_discount with invalid values."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost when subtotal is below threshold."""
        subtotal = 50.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping cost when subtotal is above threshold."""
        subtotal = 150.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        """Test shipping cost when subtotal equals threshold."""
        subtotal = 100.0
        self.assertEqual(self.calculator.calculate_shipping(subtotal), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        amount = 100.0
        self.assertEqual(self.calculator.calculate_tax(amount), 20.0)

    def test_calculate_total_no_discount(self):
        """Test total calculation without discount."""
        self.calculator.add_item('Item', 50.0)
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertTrue(total > 50.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        """Test total calculation meeting free shipping after discount."""
        self.calculator.add_item('ExpensiveItem', 200.0)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_total_items(self):
        """Test item counting logic."""
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_list_items(self):
        """Test listing item names."""
        self.calculator.add_item('Item A', 10.0)
        self.calculator.add_item('Item B', 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Item A', items)
        self.assertIn('Item B', items)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())