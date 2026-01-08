import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default parameters."""
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        """Test initialization with custom valid parameters."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        """Test initialization raises TypeError for incorrect parameter types."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_invalid_values(self):
        """Test initialization raises ValueError for out-of-range parameters."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid(self):
        """Test adding a valid item."""
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calculator.add_item('Banana', 2.0)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        """Test adding an existing item updates its quantity."""
        self.calculator.add_item('Apple', 1.5, 5)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 8)

    def test_add_item_invalid_types(self):
        """Test adding item with invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 'cheap')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, 2.5)

    def test_add_item_invalid_values(self):
        """Test adding item with invalid values raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -1)

    def test_add_item_price_conflict(self):
        """Test adding same item name with different price raises ValueError."""
        self.calculator.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_remove_item_valid(self):
        """Test removing an existing item."""
        self.calculator.add_item('Apple', 1.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.items, [])

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        self.calculator.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        """Test removing item with invalid name type raises TypeError."""
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        """Test calculating subtotal for items."""
        self.calculator.add_item('Item1', 10.0, 2)
        self.calculator.add_item('Item2', 5.5, 1)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        """Test get_subtotal on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying discount correctly."""
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_types(self):
        """Test apply_discount raises TypeError for invalid types."""
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_values(self):
        """Test apply_discount raises ValueError for invalid values."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-50.0, 0.2)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_cost_applied(self):
        """Test shipping cost applied when below threshold."""
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        """Test shipping is free when threshold is met or exceeded."""
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculate_shipping raises TypeError for invalid input."""
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        """Test tax calculation based on configured rate."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculate_tax raises TypeError for invalid input."""
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        """Test calculate_tax raises ValueError for negative amount."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_total_standard(self):
        """
        Test full total calculation flow.
        Subtotal: 100, Discount: 0.1 -> 90.
        Shipping (threshold 100): 10.
        Taxable: 90 + 10 = 100.
        Tax (0.23): 23.
        Total: 90 + 10 + 23 = 123.
        """
        self.calculator.add_item('Item1', 50.0, 2)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_free_shipping(self):
        """
        Test total calculation with free shipping.
        Subtotal: 200, Discount: 0.1 -> 180.
        Shipping (threshold 100): 0.
        Taxable: 180.
        Tax (0.23): 41.4.
        Total: 180 + 0 + 41.4 = 221.4.
        """
        self.calculator.add_item('Item1', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.1), 221.4)

    def test_calculate_total_empty_order(self):
        """Test calculate_total raises ValueError on empty order."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test calculate_total raises TypeError for invalid discount type."""
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='high')

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.items, [])

    def test_list_items(self):
        """Test listing unique item names."""
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 5)
        self.calculator.add_item('A', 10)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        """Test is_empty checks."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())