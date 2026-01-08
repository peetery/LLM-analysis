import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        self.assertEqual(self.calc.tax_rate, 0.23)
        self.assertEqual(self.calc.free_shipping_threshold, 100.0)
        self.assertEqual(self.calc.shipping_cost, 10.0)
        self.assertEqual(self.calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        with self.assertRaisesRegex(TypeError, 'Tax rate must be a float or int'):
            OrderCalculator(tax_rate='0.2')
        with self.assertRaisesRegex(TypeError, 'Free shipping threshold must be a float or int'):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaisesRegex(TypeError, 'Shipping cost must be a float or int'):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_values(self):
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaisesRegex(ValueError, 'Tax rate must be between 0.0 and 1.0'):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaisesRegex(ValueError, 'Free shipping threshold cannot be negative'):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaisesRegex(ValueError, 'Shipping cost cannot be negative'):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_success(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 2})

    def test_add_item_update_quantity(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_invalid_types(self):
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calc.add_item(123, 10.0)
        with self.assertRaisesRegex(TypeError, 'Price must be a number'):
            self.calc.add_item('Apple', '10')
        with self.assertRaisesRegex(TypeError, 'Quantity must be an integer'):
            self.calc.add_item('Apple', 10.0, 1.5)

    def test_add_item_invalid_values(self):
        with self.assertRaisesRegex(ValueError, 'Item name cannot be empty'):
            self.calc.add_item('', 10.0)
        with self.assertRaisesRegex(ValueError, 'Price must be greater than 0'):
            self.calc.add_item('Apple', 0)
        with self.assertRaisesRegex(ValueError, 'Quantity must be at least 1'):
            self.calc.add_item('Apple', 10.0, 0)

    def test_add_item_price_conflict(self):
        self.calc.add_item('Apple', 1.5)
        with self.assertRaisesRegex(ValueError, 'Item with the same name but different price already exists'):
            self.calc.add_item('Apple', 2.0)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 1.5)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        with self.assertRaisesRegex(ValueError, "Item with name 'Apple' does not exist"):
            self.calc.remove_item('Apple')

    def test_remove_item_invalid_type(self):
        with self.assertRaisesRegex(TypeError, 'Item name must be a string'):
            self.calc.remove_item(123)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Banana', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order'):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_types(self):
        with self.assertRaisesRegex(TypeError, 'Subtotal must be a number'):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calc.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_values(self):
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calc.apply_discount(100.0, 1.5)
        with self.assertRaisesRegex(ValueError, 'Discount must be between 0.0 and 1.0'):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaisesRegex(ValueError, 'Cannot apply discount on negative subtotal'):
            self.calc.apply_discount(-10.0, 0.1)

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaisesRegex(TypeError, 'Discounted subtotal must be a number'):
            self.calc.calculate_shipping('100')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaisesRegex(TypeError, 'Amount must be a number'):
            self.calc.calculate_tax('100')

    def test_calculate_tax_negative(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate tax on negative amount'):
            self.calc.calculate_tax(-10.0)

    def test_calculate_total_simple(self):
        self.calc.add_item('Item1', 50.0)
        self.assertAlmostEqual(self.calc.calculate_total(), 73.8)

    def test_calculate_total_with_discount_and_shipping(self):
        self.calc.add_item('Item1', 100.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 123.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item1', 200.0)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.1), 221.4)

    def test_calculate_total_empty(self):
        with self.assertRaisesRegex(ValueError, 'Cannot calculate subtotal on empty order'):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('A', 10)
        with self.assertRaisesRegex(TypeError, 'Discount must be a number'):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 5, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10)
        self.calc.clear_order()
        self.assertEqual(self.calc.items, [])
        self.assertTrue(self.calc.is_empty())

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 10)
        self.calc.add_item('B', 5)
        self.calc.add_item('A', 10, 2)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 10)
        self.assertFalse(self.calc.is_empty())