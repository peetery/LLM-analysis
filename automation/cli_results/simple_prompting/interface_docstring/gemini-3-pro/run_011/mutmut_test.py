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

    def test_init_custom_values(self):
        """Test initialization with valid custom values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 10.0)

    def test_init_invalid_tax_rate(self):
        """Test ValueError for invalid tax_rate."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold(self):
        """Test ValueError for negative free_shipping_threshold."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost(self):
        """Test ValueError for negative shipping_cost."""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        """Test TypeError for incorrect parameter types."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10.0])

    def test_add_item_valid_new(self):
        """Test adding a new item."""
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_defaults(self):
        """Test adding item with default quantity."""
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_existing_accumulate(self):
        """Test adding an existing item updates quantity."""
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calc.total_items(), 5)
        self.assertEqual(len(self.calc.list_items()), 1)

    def test_add_item_invalid_values(self):
        """Test ValueError for invalid name, price, quantity."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, -1)

    def test_add_item_clashing_price(self):
        """Test ValueError for same name but different price."""
        self.calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0)

    def test_add_item_invalid_types(self):
        """Test TypeError for inputs."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.0, '1')

    def test_remove_item_valid(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.0)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())
        self.assertNotIn('Apple', self.calc.list_items())

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        """Test TypeError if name is not a string."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        """Test subtotal calculation."""
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.5, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.5)

    def test_get_subtotal_empty(self):
        """Test get_subtotal raises ValueError on empty order."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        """Test standard discount application."""
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_limits(self):
        """Test 0% and 100% discounts."""
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        """Test ValueError for invalid subtotal or discount range."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        """Test TypeError for invalid types."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_standard(self):
        """Test shipping cost below threshold."""
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        """Test shipping cost above or equal threshold."""
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test TypeError if input is not a number."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero(self):
        """Test tax on zero amount."""
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        """Test ValueError for negative amount."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        """Test TypeError for invalid input."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_flow(self):
        """
        Test full total calculation.
        Subtotal: 200.0
        Discount: 10% -> 180.0
        Shipping: 180.0 > 100.0 (threshold) -> 0.0
        Taxable: 180.0 + 0.0 = 180.0
        Tax: 180 * 0.23 = 41.4
        Total: 180.0 + 41.4 = 221.4
        """
        self.calc.add_item('Expensive Item', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 221.4)

    def test_calculate_total_with_shipping(self):
        """
        Test total calculation with shipping.
        Subtotal: 50.0
        Discount: 0.0 -> 50.0
        Shipping: 50.0 < 100.0 -> 10.0
        Taxable: 50.0 + 10.0 = 60.0
        Tax: 60.0 * 0.23 = 13.8
        Total: 60.0 + 13.8 = 73.8
        """
        self.calc.add_item('Item', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.0), 73.8)

    def test_calculate_total_empty(self):
        """Test calculating total on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        """Test calculating total with invalid discount."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_invalid_type(self):
        """Test TypeError when input to calculate_total is bad (though defined as optional, passing wrong type)."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 2.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        """Test listing item names."""
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 2.0)
        items = self.calc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())