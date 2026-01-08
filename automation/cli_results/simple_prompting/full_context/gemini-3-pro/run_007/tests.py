import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a default calculator before each test."""
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default parameters."""
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        """Test initialization with custom parameters."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        """Test initialization with incorrect types raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Tax rate must be a float or int'):
            OrderCalculator(tax_rate='0.2')
        with self.assertRaisesRegex(TypeError, 'Free shipping threshold must be a float or int'):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaisesRegex(TypeError, 'Shipping cost must be a float or int'):
            OrderCalculator(shipping_cost=[])

    def test_init_invalid_values(self):
        """Test initialization with values out of range raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaisesRegex(ValueError, 'Free shipping threshold cannot be negative'):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaisesRegex(ValueError, 'Shipping cost cannot be negative'):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        """Test adding a new item."""
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 2})

    def test_add_item_existing_update(self):
        """Test adding an item that already exists updates the quantity."""
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_default_quantity(self):
        """Test adding an item uses default quantity of 1."""
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_invalid_types(self):
        """Test add_item with invalid parameter types raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calculator.add_item(123, 10.0)
        with self.assertRaisesRegex(TypeError, 'Price must be a number'):
            self.calculator.add_item('Apple', '10.0')
        with self.assertRaisesRegex(TypeError, 'Quantity must be an integer'):
            self.calculator.add_item('Apple', 10.0, 1.5)

    def test_add_item_invalid_values(self):
        """Test add_item with invalid values raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'Item name cannot be empty'):
            self.calculator.add_item('', 10.0)
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0'):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0'):
            self.calculator.add_item('Apple', -5.0)
        with self.assertRaisesRegex(ValueError, 'Quantity must be at least 1'):
            self.calculator.add_item('Apple', 10.0, 0)

    def test_add_item_conflict(self):
        """Test adding item with same name but different price raises ValueError."""
        self.calculator.add_item('Apple', 1.5)
        with self.assertRaisesRegex(ValueError, 'Item with the same name but different price already exists'):
            self.calculator.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        """Test removing an existing item."""
        self.calculator.add_item('Apple', 1.5)
        self.calculator.add_item('Banana', 0.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        with self.assertRaisesRegex(ValueError, "Item with name 'Apple' does not exist"):
            self.calculator.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        """Test removing with non-string name raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calculator.remove_item(123)

    def test_get_subtotal_success(self):
        """Test subtotal calculation."""
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Banana', 5.0, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty_raises(self):
        """Test get_subtotal on empty order raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order'):
            self.calculator.get_subtotal()

    def test_apply_discount_standard(self):
        """Test applying a standard discount."""
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        """Test applying 0% discount."""
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        """Test applying 100% discount."""
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_types(self):
        """Test apply_discount with invalid types raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Subtotal must be a number'):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_values(self):
        """Test apply_discount with invalid values raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calculator.apply_discount(100.0, 1.1)
        with self.assertRaisesRegex(ValueError, 'Cannot apply discount on negative subtotal'):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_standard(self):
        """Test shipping cost applied when below threshold."""
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        """Test free shipping when at or above threshold."""
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculate_shipping with invalid type raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Discounted subtotal must be a number'):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_standard(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        """Test tax on zero amount."""
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculate_tax with invalid type raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Amount must be a number'):
            self.calculator.calculate_tax(None)

    def test_calculate_tax_negative(self):
        """Test calculate_tax with negative amount raises ValueError."""
        with self.assertRaisesRegex(ValueError, 'Cannot calculate tax on negative amount'):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_total_standard(self):
        """
        Test total calculation flow.
        Subtotal: 10 * 5 = 50.0
        Discount: 10% -> 45.0
        Shipping: 45 < 100 -> +10.0 shipping
        Taxable: 45 + 10 = 55.0
        Tax: 55 * 0.23 = 12.65
        Total: 55 + 12.65 = 67.65
        """
        self.calculator.add_item('Item1', 10.0, 5)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 67.65)

    def test_calculate_total_free_shipping(self):
        """
        Test total calculation with free shipping.
        Subtotal: 200.0
        Discount: 0% -> 200.0
        Shipping: 200 >= 100 -> 0.0
        Taxable: 200 + 0 = 200.0
        Tax: 200 * 0.23 = 46.0
        Total: 246.0
        """
        self.calculator.add_item('ExpensiveItem', 200.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 246.0)

    def test_calculate_total_empty_order(self):
        """Test calculate_total on empty order raises ValueError (propagated from get_subtotal)."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test calculate_total with invalid discount type raises TypeError."""
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calculator.calculate_total(discount='high')

    def test_total_items(self):
        """Test total quantity calculation."""
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 20, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.items, [])

    def test_list_items(self):
        """Test listing item names."""
        self.calculator.add_item('A', 10)
        self.calculator.add_item('B', 20)
        items = self.calculator.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_list_items_empty(self):
        """Test list_items on empty order."""
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10)
        self.assertFalse(self.calculator.is_empty())