import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        """Set up a fresh instance for each test."""
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        """Test initialization with default values."""
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        """Test initialization with custom valid values."""
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        """Test initialization with invalid parameter types."""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_invalid_values(self):
        """Test initialization with values out of allowed ranges."""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        """Test adding a new item."""
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_existing_same_price(self):
        """Test adding an item that already exists (should increase quantity)."""
        self.calc.add_item('Apple', 1.5, 10)
        self.calc.add_item('Apple', 1.5, 5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 15)

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity."""
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_existing_different_price(self):
        """Test adding an existing item with a different price raises ValueError."""
        self.calc.add_item('Apple', 1.5, 10)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 5)

    def test_add_item_invalid_types(self):
        """Test adding item with invalid types."""
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 1.5)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '1.5')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 1.5, 2.5)

    def test_add_item_invalid_values(self):
        """Test adding item with invalid values."""
        with self.assertRaises(ValueError):
            self.calc.add_item('', 1.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.5, 0)

    def test_remove_item_success(self):
        """Test removing an existing item."""
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        """Test removing an item that does not exist."""
        with self.assertRaises(ValueError):
            self.calc.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        """Test removing item with invalid name type."""
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        """Test subtotal calculation."""
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.0, 3)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        """Test subtotal raises ValueError on empty order."""
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        """Test applying a valid discount."""
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        """Test applying 0% discount."""
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        """Test applying 100% discount."""
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range(self):
        """Test applying discount outside 0-1 range."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        """Test applying discount on negative subtotal."""
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        """Test apply_discount with invalid types."""
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_standard(self):
        """Test shipping cost when below threshold."""
        cost = self.calc.calculate_shipping(99.99)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_free(self):
        """Test free shipping when at or above threshold."""
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculate_shipping with invalid type."""
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        """Test tax calculation."""
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        """Test tax calculation on negative amount."""
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculate_tax with invalid type."""
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_standard(self):
        """
        Test total calculation flow.
        Subtotal: 50.0 (below free shipping 100.0)
        Discount: 0.0
        Shipping: 10.0
        Taxable: 50 + 10 = 60
        Tax: 60 * 0.23 = 13.8
        Total: 60 + 13.8 = 73.8
        """
        self.calc.add_item('Item1', 50.0, 1)
        total = self.calc.calculate_total(discount=0.0)
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        """
        Test total with discount qualifying for free shipping logic.
        Subtotal: 200.0
        Discount: 0.5 -> 100.0 (At threshold) -> Free shipping
        Shipping: 0.0
        Taxable: 100 + 0 = 100
        Tax: 100 * 0.23 = 23.0
        Total: 123.0
        """
        self.calc.add_item('Item1', 200.0, 1)
        total = self.calc.calculate_total(discount=0.5)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount_losing_free_shipping(self):
        """
        Test total where discount drops value below free shipping threshold.
        Subtotal: 100.0
        Discount: 0.1 -> 90.0 (Below 100) -> Add shipping
        Shipping: 10.0
        Taxable: 90 + 10 = 100
        Tax: 100 * 0.23 = 23.0
        Total: 123.0
        """
        self.calc.add_item('Item1', 100.0, 1)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_empty_order(self):
        """Test total calculation on empty order raises ValueError."""
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        """Test calculate_total with invalid discount type."""
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_calculate_total_negative_subtotal_protection(self):
        """
        Indirectly test negative subtotal check in calculate_total.
        Since we cannot add negative price items normally via add_item,
        we manually inject a negative item to test the safeguard in calculate_total
        calling apply_discount/get_subtotal.
        """
        self.calc.items.append({'name': 'Hack', 'price': -50.0, 'quantity': 1})
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_total_items(self):
        """Test counting total items."""
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        """Test clearing the order."""
        self.calc.add_item('A', 10)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        """Test listing item names."""
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 1.0)
        names = self.calc.list_items()
        self.assertCountEqual(names, ['Apple', 'Banana'])

    def test_list_items_empty(self):
        """Test listing items on empty order."""
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty(self):
        """Test is_empty status."""
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1.0)
        self.assertFalse(self.calc.is_empty())