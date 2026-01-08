import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.tax_rate = 0.2
        self.free_shipping_threshold = 100.0
        self.shipping_cost = 10.0
        self.calculator = OrderCalculator(tax_rate=self.tax_rate, free_shipping_threshold=self.free_shipping_threshold, shipping_cost=self.shipping_cost)

    def test_initial_state(self):
        """Test that a new calculator is empty and has correct defaults."""
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_add_item_valid(self):
        """Test adding items with valid inputs."""
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)
        self.assertFalse(self.calculator.is_empty())
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_default_quantity(self):
        """Test adding an item uses default quantity of 1."""
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.5)

    def test_add_item_multiple_entries(self):
        """Test adding the same item multiple times accumulates quantity."""
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.add_item('Apple', 1.0, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 3.0)

    def test_add_item_invalid_inputs(self):
        """Test that adding items with invalid prices or quantities raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadPrice', -10.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('BadQtyNegative', 10.0, -1)

    def test_remove_item(self):
        """Test removing an item completely."""
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertNotIn('Apple', self.calculator.list_items())

    def test_remove_nonexistent_item(self):
        """Test removing an item that does not exist (should handle gracefully or raise)."""
        try:
            self.calculator.remove_item('Ghost')
        except KeyError:
            pass
        except Exception as e:
            self.fail(f'remove_item raised unexpected exception for missing item: {e}')

    def test_clear_order(self):
        """Test clearing the order resets all state."""
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 20.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.list_items(), [])

    def test_apply_discount_logic(self):
        """Test the logic for calculating discounted amount."""
        subtotal = 100.0
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 0.1), 90.0)
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)
        self.assertAlmostEqual(self.calculator.apply_discount(subtotal, 1.0), 0.0)

    def test_apply_discount_invalid(self):
        """Test apply_discount with invalid rates."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost application below threshold."""
        cost = self.calculator.calculate_shipping(50.0)
        self.assertEqual(cost, self.shipping_cost)

    def test_calculate_shipping_above_threshold(self):
        """Test free shipping above threshold."""
        cost = self.calculator.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_at_threshold(self):
        """Test shipping at exact threshold (usually free)."""
        cost = self.calculator.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_tax(self):
        """Test tax calculation."""
        amount = 100.0
        expected_tax = 100.0 * self.tax_rate
        self.assertAlmostEqual(self.calculator.calculate_tax(amount), expected_tax)

    def test_calculate_total_simple(self):
        """Test total calculation flow without discount."""
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 70.0)

    def test_calculate_total_with_free_shipping(self):
        """Test total calculation with amount qualifying for free shipping."""
        self.calculator.add_item('ExpensiveItem', 200.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 240.0)

    def test_calculate_total_with_discount(self):
        """Test total calculation with a discount applied."""
        self.calculator.add_item('Item', 100.0)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 118.0)

    def test_calculate_total_invalid_discount(self):
        """Test calculate_total propagates errors for invalid discounts."""
        self.calculator.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=-0.5)

    def test_is_empty_behavior(self):
        """Test is_empty state transitions."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Item', 1.0)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.remove_item('Item')
        self.assertTrue(self.calculator.is_empty())