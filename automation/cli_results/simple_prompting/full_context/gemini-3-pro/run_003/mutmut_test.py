import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom_values(self):
        """Test initialization with custom valid values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        """Test initialization with invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_values(self):
        """Test initialization with invalid value ranges raises ValueError."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        """Test adding a new item."""
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_existing_same_price(self):
        """Test adding an existing item with the same price increases quantity."""
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 15)

    def test_add_item_default_quantity(self):
        """Test adding an item uses default quantity of 1."""
        self.calc.add_item('Apple', 1.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_invalid_types(self):
        """Test add_item with invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, '10')

    def test_add_item_invalid_values(self):
        """Test add_item with invalid values raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_add_item_conflict_price(self):
        """Test adding existing item name with different price raises ValueError."""
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        """Test removing item with invalid type name raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        """Test subtotal calculation."""
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 3.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 16.0)

    def test_get_subtotal_empty(self):
        """Test get_subtotal on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero_subtotal(self):
        """Test applying discount on zero subtotal."""
        result = self.calc.apply_discount(0.0, 0.5)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_types(self):
        """Test apply_discount with invalid types raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.2')

    def test_apply_discount_invalid_values(self):
        """Test apply_discount with invalid values raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-100.0, 0.2)

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost applied when below threshold."""
        cost = self.calc.calculate_shipping(99.9)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_above_threshold(self):
        """Test free shipping when above or equal to threshold."""
        cost = self.calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)
        cost = self.calc.calculate_shipping(150.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculate_shipping with invalid type raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('99.9')

    def test_calculate_tax_valid(self):
        """Test tax calculation (default 23%)."""
        tax = self.calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_zero(self):
        """Test tax on zero amount."""
        tax = self.calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculate_tax with invalid type raises TypeError."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        """Test calculate_tax with negative amount raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_standard(self):
        """
        Test total calculation flow.
        Items: 10 * 10.0 = 100.0
        Discount: 0.0
        Shipping: Free (>= 100) -> 0.0
        Taxable: 100.0
        Tax: 23.0
        Total: 100.0 + 0.0 + 23.0 = 123.0
        """
        self.calc.add_item('Item1', 10.0, 10)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_shipping(self):
        """
        Items: 1 * 50.0 = 50.0
        Discount: 0.0
        Shipping: < 100 -> Adds 10.0
        Taxable: 50.0 + 10.0 = 60.0
        Tax: 0.23 * 60.0 = 13.8
        Total: 50.0 + 10.0 + 13.8 = 73.8
        """
        self.calc.add_item('Item1', 50.0, 1)
        total = self.calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_with_discount(self):
        """
        Items: 1 * 200.0 = 200.0
        Discount: 0.5 -> Subtotal 100.0
        Shipping: >= 100 -> 0.0
        Taxable: 100.0
        Tax: 23.0
        Total: 123.0
        """
        self.calc.add_item('Item1', 200.0, 1)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_discount_triggers_shipping(self):
        """
        Items: 1 * 100.0 = 100.0
        Discount: 0.1 -> Subtotal 90.0
        Shipping: 90 < 100 -> Adds 10.0
        Taxable: 90.0 + 10.0 = 100.0
        Tax: 23.0
        Total: 90.0 + 10.0 + 23.0 = 123.0
        """
        self.calc.add_item('Item1', 100.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_empty_order(self):
        """Test calculate_total on empty order raises ValueError (from get_subtotal)."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test calculate_total with invalid discount type raises TypeError."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        """Test total items count."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 20, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 10)
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        """Test listing unique item names."""
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 20)
        self.calc.add_item('A', 10)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())