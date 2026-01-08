import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh OrderCalculator instance before each test."""
        self.calculator = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        """Test initialization with custom values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_type(self):
        """Test __init__ raises TypeError for invalid tax_rate type."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_tax_rate_value(self):
        """Test __init__ raises ValueError for tax_rate out of range."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_shipping_threshold_value(self):
        """Test __init__ raises ValueError for negative free_shipping_threshold."""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_value(self):
        """Test __init__ raises ValueError for negative shipping_cost."""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        """Test adding a new item."""
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_defaults(self):
        """Test adding an item with default quantity."""
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_existing_same_price(self):
        """Test adding an existing item updates quantity."""
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 5)

    def test_add_item_existing_diff_price(self):
        """Test adding an existing item with different price raises ValueError."""
        self.calculator.add_item('Apple', 1.5, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_types(self):
        """Test add_item raises TypeError for invalid inputs."""
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5')
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, 1.5)

    def test_add_item_invalid_values(self):
        """Test add_item raises ValueError for invalid values."""
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, 0)

    def test_remove_item_success(self):
        """Test removing an existing item."""
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_not_found(self):
        """Test removing a non-existent item raises ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        """Test removing item with non-string name raises TypeError."""
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        """Test calculating subtotal for items."""
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 1.0, 5)
        self.assertEqual(self.calculator.get_subtotal(), 11.0)

    def test_get_subtotal_empty(self):
        """Test get_subtotal raises ValueError if order is empty."""
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_and_full(self):
        """Test applying 0% and 100% discounts."""
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_range(self):
        """Test apply_discount raises ValueError for discount out of range."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        """Test apply_discount raises ValueError for negative subtotal."""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_types(self):
        """Test apply_discount raises TypeError for invalid inputs."""
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100, '0.2')

    def test_calculate_shipping_below_threshold(self):
        """Test shipping cost applied when below threshold."""
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_at_threshold(self):
        """Test free shipping when at threshold."""
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        """Test free shipping when above threshold."""
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculate_shipping raises TypeError for invalid input."""
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative(self):
        """Test calculate_tax raises ValueError for negative amount."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-50.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculate_tax raises TypeError for invalid input."""
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_with_shipping(self):
        """
        Test total calculation with shipping.
        Subtotal: 50
        Discount: 0
        Shipping: 10 (since 50 < 100)
        Taxable: 60
        Tax (20%): 12
        Total: 72
        """
        self.calculator.add_item('Item1', 50.0, 1)
        total = self.calculator.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 72.0)

    def test_calculate_total_free_shipping_after_discount(self):
        """
        Test total calculation where discount keeps it above threshold.
        Subtotal: 200
        Discount: 0.1 (10%) -> 180
        Shipping: 0 (180 > 100)
        Taxable: 180
        Tax (20%): 36
        Total: 216
        """
        self.calculator.add_item('Item1', 200.0, 1)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_calculate_total_shipping_triggered_by_discount(self):
        """
        Test total calculation where discount drops it below threshold.
        Subtotal: 105
        Discount: 0.1 -> 94.5
        Shipping: 10 (94.5 < 100)
        Taxable: 104.5
        Tax (20%): 20.9
        Total: 125.4
        """
        self.calculator.add_item('Item1', 105.0, 1)
        total = self.calculator.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 125.4)

    def test_calculate_total_empty_order(self):
        """Test calculate_total raises ValueError via get_subtotal for empty order."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test calculate_total raises TypeError for invalid discount."""
        self.calculator.add_item('Item1', 10.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items(self):
        """Test counting total items."""
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_total_items_empty(self):
        """Test total items is 0 for empty order."""
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calculator.add_item('A', 10.0)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)
        self.assertTrue(self.calculator.is_empty())

    def test_list_items(self):
        """Test listing item names."""
        self.calculator.add_item('A', 10.0)
        self.calculator.add_item('B', 5.0)
        names = self.calculator.list_items()
        self.assertCountEqual(names, ['A', 'B'])

    def test_list_items_empty(self):
        """Test listing items for empty order."""
        self.assertEqual(self.calculator.list_items(), [])

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1.0)
        self.assertFalse(self.calculator.is_empty())