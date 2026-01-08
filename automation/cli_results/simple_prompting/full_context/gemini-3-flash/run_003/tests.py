import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(len(calc.items), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_type_errors(self):
        with self.assertRaisesRegex(TypeError, 'Tax rate must be a float or int'):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaisesRegex(TypeError, 'Free shipping threshold must be a float or int'):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaisesRegex(TypeError, 'Shipping cost must be a float or int'):
            OrderCalculator(shipping_cost=[])

    def test_init_value_errors(self):
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaisesRegex(ValueError, 'Free shipping threshold cannot be negative'):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaisesRegex(ValueError, 'Shipping cost cannot be negative'):
            OrderCalculator(shipping_cost=-10.0)

    def test_add_item_success(self):
        self.calc.add_item('Laptop', 1000.0, 1)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Laptop')
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_increase_quantity(self):
        self.calc.add_item('Mouse', 25.0, 2)
        self.calc.add_item('Mouse', 25.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_type_errors(self):
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calc.add_item(123, 10.0)
        with self.assertRaisesRegex(TypeError, 'Price must be a number'):
            self.calc.add_item('Item', '10.0')
        with self.assertRaisesRegex(TypeError, 'Quantity must be an integer'):
            self.calc.add_item('Item', 10.0, 1.5)

    def test_add_item_value_errors(self):
        with self.assertRaisesRegex(ValueError, 'Item name cannot be empty'):
            self.calc.add_item('', 10.0)
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0'):
            self.calc.add_item('Item', 0)
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0'):
            self.calc.add_item('Item', -5.0)
        with self.assertRaisesRegex(ValueError, 'Quantity must be at least 1'):
            self.calc.add_item('Item', 10.0, 0)
        with self.assertRaisesRegex(ValueError, 'Item with the same name but different price already exists'):
            self.calc.add_item('Item', 10.0, 1)
            self.calc.add_item('Item', 20.0, 1)

    def test_remove_item_success(self):
        self.calc.add_item('Item1', 10.0)
        self.calc.add_item('Item2', 20.0)
        self.calc.remove_item('Item1')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Item2')

    def test_remove_item_type_error(self):
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calc.remove_item(None)

    def test_remove_item_not_found(self):
        with self.assertRaisesRegex(ValueError, "Item with name 'Ghost' does not exist"):
            self.calc.remove_item('Ghost')

    def test_get_subtotal_success(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 15.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 35.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order'):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_type_errors(self):
        with self.assertRaisesRegex(TypeError, 'Subtotal must be a number'):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_value_errors(self):
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calc.apply_discount(100.0, 1.1)
        with self.assertRaisesRegex(ValueError, 'Cannot apply discount on negative subtotal'):
            self.calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_standard(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 15.0
        self.assertEqual(self.calc.calculate_shipping(50.0), 15.0)
        self.assertEqual(self.calc.calculate_shipping(99.99), 15.0)

    def test_calculate_shipping_free(self):
        self.calc.free_shipping_threshold = 100.0
        self.calc.shipping_cost = 15.0
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaisesRegex(TypeError, 'Discounted subtotal must be a number'):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.calc.tax_rate = 0.2
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaisesRegex(TypeError, 'Amount must be a number'):
            self.calc.calculate_tax('100')

    def test_calculate_tax_value_error(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate tax on negative amount'):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_no_discount_with_shipping(self):
        self.calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.0), 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(0.5), 123.0)

    def test_calculate_total_type_error(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calc.calculate_total('0.1')

    def test_calculate_total_empty_order(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order'):
            self.calc.calculate_total()

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 20.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('Item1', 10.0)
        self.calc.clear_order()
        self.assertEqual(len(self.calc.items), 0)
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item('A', 10.0)
        self.calc.add_item('B', 10.0)
        self.calc.add_item('A', 10.0)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 10.0)
        self.assertFalse(self.calc.is_empty())