import unittest
from typing import TypedDict, List
from order_calculator import OrderCalculator

# class Item(TypedDict):
#     """
#     Represents a single product entry in the order.
#
#     :key name: The name of the product.
#     :key price: The price per unit of the product.
#     :key quantity: The number of units of the product.
#     """
#     name: str
#     price: float
#     quantity: int
#
#
# class OrderCalculator:
#     """Mock class needed for testing"""
#     pass


class TestOrderCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        """Test initialization with default parameters"""
        calculator = OrderCalculator()
        self.assertEqual(calculator.tax_rate, 0.23)
        self.assertEqual(calculator.free_shipping_threshold, 100.0)
        self.assertEqual(calculator.shipping_cost, 10.0)
        self.assertEqual(calculator.items, [])

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters"""
        calculator = OrderCalculator(tax_rate=0.20, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calculator.tax_rate, 0.20)
        self.assertEqual(calculator.free_shipping_threshold, 50.0)
        self.assertEqual(calculator.shipping_cost, 5.0)

    def test_init_invalid_tax_rate(self):
        """Test initialization with invalid tax rate"""
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_free_shipping_threshold(self):
        """Test initialization with invalid free shipping threshold"""
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost(self):
        """Test initialization with invalid shipping cost"""
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_parameter_types(self):
        """Test initialization with invalid parameter types"""
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate="0.23")
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold="100.0")
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost="10.0")

    def test_add_item_new(self):
        """Test adding a new item"""
        self.calculator.add_item("Book", 20.0, 2)
        expected_item = {"name": "Book", "price": 20.0, "quantity": 2}
        self.assertEqual(len(self.calculator.items), 1)
        self.assertDictEqual(self.calculator.items[0], expected_item)

    def test_add_item_default_quantity(self):
        """Test adding an item with default quantity"""
        self.calculator.add_item("Pen", 2.0)
        expected_item = {"name": "Pen", "price": 2.0, "quantity": 1}
        self.assertEqual(len(self.calculator.items), 1)
        self.assertDictEqual(self.calculator.items[0], expected_item)

    def test_add_item_existing_same_price(self):
        """Test adding an item that already exists with the same price"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.add_item("Book", 20.0, 3)
        expected_item = {"name": "Book", "price": 20.0, "quantity": 5}
        self.assertEqual(len(self.calculator.items), 1)
        self.assertDictEqual(self.calculator.items[0], expected_item)

    def test_add_item_existing_different_price(self):
        """Test adding an item that already exists but with a different price"""
        self.calculator.add_item("Book", 20.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Book", 25.0, 1)

    def test_add_item_invalid_name(self):
        """Test adding an item with an empty name"""
        with self.assertRaises(ValueError):
            self.calculator.add_item("", 20.0, 2)

    def test_add_item_invalid_price(self):
        """Test adding an item with invalid price"""
        with self.assertRaises(ValueError):
            self.calculator.add_item("Book", 0.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Book", -5.0, 2)

    def test_add_item_invalid_quantity(self):
        """Test adding an item with invalid quantity"""
        with self.assertRaises(ValueError):
            self.calculator.add_item("Book", 20.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item("Book", 20.0, -1)

    def test_add_item_invalid_types(self):
        """Test adding an item with invalid types"""
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 20.0, 2)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Book", "20.0", 2)
        with self.assertRaises(TypeError):
            self.calculator.add_item("Book", 20.0, "2")

    def test_remove_item_existing(self):
        """Test removing an existing item"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.add_item("Pen", 2.0, 1)
        self.calculator.remove_item("Book")
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]["name"], "Pen")

    def test_remove_item_nonexistent(self):
        """Test removing a non-existent item"""
        self.calculator.add_item("Book", 20.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.remove_item("Pen")

    def test_remove_item_invalid_type(self):
        """Test removing an item with invalid type"""
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_nonempty(self):
        """Test getting subtotal from a non-empty order"""
        self.calculator.add_item("Book", 20.0, 2)  # 40.0
        self.calculator.add_item("Pen", 2.0, 3)  # 6.0
        self.assertEqual(self.calculator.get_subtotal(), 46.0)

    def test_get_subtotal_empty(self):
        """Test getting subtotal from an empty order"""
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_zero(self):
        """Test applying zero discount"""
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_partial(self):
        """Test applying partial discount"""
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_full(self):
        """Test applying full discount"""
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_negative_subtotal(self):
        """Test applying discount to negative subtotal"""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.2)

    def test_apply_discount_invalid_discount(self):
        """Test applying invalid discount"""
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        """Test applying discount with invalid types"""
        with self.assertRaises(TypeError):
            self.calculator.apply_discount("100.0", 0.2)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, "0.2")

    def test_calculate_shipping_below_threshold(self):
        """Test calculating shipping below free shipping threshold"""
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        """Test calculating shipping at free shipping threshold"""
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        """Test calculating shipping above free shipping threshold"""
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        """Test calculating shipping with invalid type"""
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping("50.0")

    def test_calculate_tax_zero(self):
        """Test calculating tax on zero amount"""
        self.calculator.tax_rate = 0.23
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_positive(self):
        """Test calculating tax on positive amount"""
        self.calculator.tax_rate = 0.23
        self.assertEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_negative_amount(self):
        """Test calculating tax on negative amount"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        """Test calculating tax with invalid type"""
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax("100.0")

    def test_calculate_total_basic(self):
        """Test calculating total with default discount"""
        self.calculator.tax_rate = 0.23
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0

        self.calculator.add_item("Book", 20.0, 2)  # 40.0
        self.calculator.add_item("Pen", 2.0, 3)  # 6.0
        # Subtotal: 46.0
        # Discount: 0.0
        # Discounted subtotal: 46.0
        # Shipping: 10.0
        # Tax: (46.0 + 10.0) * 0.23 = 12.88
        # Total: 46.0 + 10.0 + 12.88 = 68.88
        self.assertAlmostEqual(self.calculator.calculate_total(), 68.88)

    def test_calculate_total_with_discount(self):
        """Test calculating total with discount"""
        self.calculator.tax_rate = 0.23
        self.calculator.free_shipping_threshold = 100.0
        self.calculator.shipping_cost = 10.0

        self.calculator.add_item("Book", 60.0, 2)  # 120.0
        # Subtotal: 120.0
        # Discount: 120.0 * 0.1 = 12.0
        # Discounted subtotal: 120.0 - 12.0 = 108.0
        # Shipping: 0.0 (free shipping)
        # Tax: 108.0 * 0.23 = 24.84
        # Total: 108.0 + 0.0 + 24.84 = 132.84
        self.assertAlmostEqual(self.calculator.calculate_total(0.1), 132.84)

    def test_calculate_total_empty_order(self):
        """Test calculating total with an empty order"""
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        """Test calculating total with invalid discount"""
        self.calculator.add_item("Book", 20.0, 2)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(1.1)

    def test_calculate_total_invalid_discount_type(self):
        """Test calculating total with invalid discount type"""
        self.calculator.add_item("Book", 20.0, 2)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total("0.1")

    def test_total_items_empty(self):
        """Test getting total number of items in an empty order"""
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_nonempty(self):
        """Test getting total number of items in a non-empty order"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.add_item("Pen", 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        """Test clearing an order"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.add_item("Pen", 2.0, 3)
        self.calculator.clear_order()
        self.assertEqual(len(self.calculator.items), 0)

    def test_list_items_empty(self):
        """Test listing items in an empty order"""
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_nonempty(self):
        """Test listing items in a non-empty order"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.add_item("Pen", 2.0, 3)
        self.calculator.add_item("Notebook", 5.0, 1)
        expected_list = ["Book", "Pen", "Notebook"]
        self.assertCountEqual(self.calculator.list_items(), expected_list)

    def test_is_empty_true(self):
        """Test checking if an empty order is empty"""
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        """Test checking if a non-empty order is empty"""
        self.calculator.add_item("Book", 20.0, 2)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        """Test checking if an order is empty after clearing it"""
        self.calculator.add_item("Book", 20.0, 2)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())


if __name__ == '__main__':
    unittest.main()