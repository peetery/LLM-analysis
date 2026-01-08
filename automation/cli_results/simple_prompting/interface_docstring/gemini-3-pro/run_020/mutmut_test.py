import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        """Test initialization with custom valid values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())
        calc.add_item('Test', 40.0)
        self.assertAlmostEqual(calc.calculate_total(), 49.5)

    def test_init_invalid_tax_rate(self):
        """Test init raises ValueError for invalid tax_rate."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        """Test init raises ValueError for negative free_shipping_threshold."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        """Test init raises ValueError for negative shipping_cost."""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        """Test init raises TypeError for incorrect types."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_add_item_new(self):
        """Test adding a new item."""
        self.calc.add_item('Apple', 1.5, 2)
        self.assertFalse(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_existing(self):
        """Test adding an existing item updates quantity."""
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_defaults(self):
        """Test adding item with default quantity."""
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_invalid_name(self):
        """Test add_item raises ValueError for empty name."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)

    def test_add_item_invalid_price(self):
        """Test add_item raises ValueError for invalid price."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)

    def test_add_item_invalid_quantity(self):
        """Test add_item raises ValueError for invalid quantity."""
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -5)

    def test_add_item_same_name_diff_price(self):
        """Test add_item raises ValueError for same name but different price."""
        self.calc.add_item('Apple', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        """Test add_item raises TypeError for incorrect types."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_success(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        """Test remove_item raises ValueError if item does not exist."""
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        """Test remove_item raises TypeError if name is not a string."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        """Test subtotal calculation."""
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        """Test get_subtotal raises ValueError if order is empty."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        """Test applying 0% discount."""
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        """Test applying 100% discount."""
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_subtotal(self):
        """Test apply_discount raises ValueError for negative subtotal."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate(self):
        """Test apply_discount raises ValueError for invalid discount rate."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        """Test apply_discount raises TypeError for incorrect types."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost applied when below threshold."""
        self.assertEqual(self.calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test shipping is free when above threshold."""
        self.assertEqual(self.calc.calculate_shipping(100.01), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        """Test shipping is free when exactly at threshold."""
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_custom_config(self):
        """Test shipping with custom configuration."""
        calc = OrderCalculator(free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_calculate_shipping_type_error(self):
        """Test calculate_shipping raises TypeError for non-number input."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        """Test tax on zero amount."""
        self.assertAlmostEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount(self):
        """Test calculate_tax raises ValueError for negative amount."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        """Test calculate_tax raises TypeError for non-number input."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_simple(self):
        """Test total calculation without discount, below free shipping."""
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        """Test total calculation with free shipping."""
        self.calc.add_item('Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 246.0)

    def test_calculate_total_with_discount_and_shipping(self):
        """Test total calculation with discount that brings subtotal below free shipping."""
        self.calc.add_item('Item', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_empty(self):
        """Test calculate_total raises ValueError if order is empty."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        """Test calculate_total raises ValueError for invalid discount."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        """Test calculate_total raises TypeError if discount is not a number."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 20, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        """Test listing item names."""
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 20)
        self.calc.add_item('A', 10)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertCountEqual(items, ['A', 'B'])

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())