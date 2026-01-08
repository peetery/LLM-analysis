import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.2
        self.free_shipping_threshold = 100.0
        self.shipping_cost = 10.0
        self.calc = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.free_shipping_threshold, shipping_cost=self.shipping_cost)

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc_default = OrderCalculator()
        self.assertTrue(calc_default.is_empty())
        self.assertEqual(calc_default.get_subtotal(), 0.0)

    def test_add_item_valid(self):
        """Test adding valid items."""
        self.calc.add_item('Apple', 2.5, 4)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 4)
        self.assertEqual(self.calc.get_subtotal(), 10.0)

    def test_add_item_multiple_distinct(self):
        """Test adding multiple different items."""
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(self.calc.get_subtotal(), 8.0)

    def test_add_item_increment_quantity(self):
        """Test that adding an existing item increments its quantity."""
        self.calc.add_item('Apple', 2.0, 1)
        self.calc.add_item('Apple', 2.0, 2)
        self.assertEqual(self.calc.total_items(), 3)
        self.assertEqual(self.calc.get_subtotal(), 6.0)

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Orange', 1.5)
        self.assertEqual(self.calc.total_items(), 1)
        self.assertEqual(self.calc.get_subtotal(), 1.5)

    def test_add_item_invalid_inputs(self):
        """Test adding items with invalid price or quantity."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Price', -5.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Bad Qty', 5.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Negative Qty', 5.0, -1)

    def test_remove_item_existing(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_remove_item_non_existent(self):
        """Test removing an item that does not exist."""
        with self.assertRaises((ValueError, KeyError)):
            self.calc.remove_item('Ghost')

    def test_get_subtotal_empty(self):
        """Test subtotal for an empty order."""
        self.assertEqual(self.calc.get_subtotal(), 0.0)

    def test_apply_discount_valid(self):
        """Test applying a valid percentage discount."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.2)
        self.assertEqual(discounted, 80.0)

    def test_apply_discount_zero(self):
        """Test applying zero discount."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 0.0)
        self.assertEqual(discounted, 100.0)

    def test_apply_discount_full(self):
        """Test applying 100% discount."""
        subtotal = 100.0
        discounted = self.calc.apply_discount(subtotal, 1.0)
        self.assertEqual(discounted, 0.0)

    def test_apply_discount_invalid(self):
        """Test applying invalid discount values."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping calculation below free shipping threshold."""
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping calculation exactly at threshold."""
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping calculation above free shipping threshold."""
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_total_no_discount_below_threshold(self):
        """Test total calculation without discount, paying shipping."""
        self.calc.add_item('Item', 50.0)
        total = self.calc.calculate_total()
        self.assertIsInstance(total, float)
        self.assertGreater(total, 50.0)
        sub = self.calc.get_subtotal()
        ship = self.calc.calculate_shipping(sub)
        self.assertTrue(total >= sub + ship)

    def test_calculate_total_with_discount_free_shipping(self):
        """Test total calculation with discount that enables/disables shipping or just calculates correctly."""
        self.calc.add_item('Expensive Item', 200.0)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 120.0, delta=5.0)

    def test_list_items(self):
        """Test listing item names."""
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.get_subtotal(), 0.0)
        self.assertEqual(self.calc.total_items(), 0)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())