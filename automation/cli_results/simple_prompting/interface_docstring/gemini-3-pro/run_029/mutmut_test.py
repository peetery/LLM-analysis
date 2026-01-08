import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Create a default instance for basic testing."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_valid(self):
        """Test initialization with valid custom values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        """Test initialization with invalid tax rates."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        """Test initialization with negative free shipping threshold."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        """Test initialization with negative shipping cost."""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        """Test initialization with incorrect types."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_add_item_valid(self):
        """Test adding a single valid item."""
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calc.total_items(), 10)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Banana', 2.0)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_increment_existing(self):
        """Test adding an existing item updates its quantity."""
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_add_item_invalid_values(self):
        """Test adding items with invalid values (empty name, bad price/qty)."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -5)

    def test_add_item_conflict_price(self):
        """Test adding item with same name but different price raises ValueError."""
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        """Test adding item with incorrect types."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_valid(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.5, 5)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        """Test removing item with non-string name raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        """Test subtotal calculation."""
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        """Test get_subtotal raises ValueError on empty order."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero_and_full(self):
        """Test boundary discount values 0.0 and 1.0."""
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        """Test apply_discount with invalid ranges."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        """Test apply_discount with incorrect types."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost applied when below threshold."""
        cost = self.calc.calculate_shipping(99.99)
        self.assertAlmostEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping is free when above or equal threshold."""
        self.assertAlmostEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertAlmostEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        """Test calculate_shipping with invalid type."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        """Test tax calculation based on default tax rate (0.23)."""
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_invalid_amount(self):
        """Test calculate_tax with negative amount."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-50.0)

    def test_calculate_tax_type_error(self):
        """Test calculate_tax with non-numeric input."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_standard(self):
        """
        Test total calculation flow:
        Subtotal: 50 (below 100 threshold)
        Shipping: 10
        Taxable: 50 + 10 = 60
        Tax (23%): 13.8
        Total: 60 + 13.8 = 73.8
        """
        self.calc.add_item('Item1', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_free_shipping(self):
        """
        Test total with free shipping:
        Subtotal: 100 (threshold reached)
        Shipping: 0
        Taxable: 100
        Tax (23%): 23
        Total: 123
        """
        self.calc.add_item('Item1', 100.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount(self):
        """
        Test total with discount:
        Items: 200.0
        Discount 50%: -> 100.0 (Eligible for free shipping)
        Shipping: 0.0
        Tax (23% on 100): 23.0
        Total: 123.0
        """
        self.calc.add_item('Expensive', 200.0, 1)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_discount_drops_below_free_shipping(self):
        """
        Test logic where discount drops value below free shipping threshold.
        Items: 100.0
        Discount 10%: -> 90.0 (Below 100 threshold, shipping adds 10.0)
        Taxable: 90 + 10 = 100
        Tax: 23.0
        Total: 123.0
        """
        self.calc.add_item('Item', 100.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_empty(self):
        """Test calculate_total on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        """Test calculate_total with invalid discount values."""
        self.calc.add_item('A', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=-0.1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        """Test calculate_total with invalid discount type."""
        self.calc.add_item('A', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        """Test total item count."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)
        self.assertEqual(self.calc.list_items(), [])

    def test_list_items(self):
        """Test listing item names."""
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 1.0)
        items = self.calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        """Test is_empty status check."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())