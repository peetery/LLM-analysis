import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(self.calculator.total_items(), 10)
        self.assertFalse(self.calculator.is_empty())

    def test_add_item_defaults(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_increase_quantity(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_invalid_arguments(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, -5)

    def test_add_item_duplicate_name_different_price(self):
        self.calculator.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)

    def test_remove_item_valid(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertEqual(self.calculator.apply_discount(100.0, 0.2), 80.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(self.calculator.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calculator.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calculator.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-1.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_standard(self):
        self.calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_with_discount_and_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.5), 123.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=1.5)

    def test_calculate_total_type_error(self):
        self.calculator.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 1.0, 5)
        self.calculator.add_item('B', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0, 1)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.calculator.add_item('A', 1.0, 2)
        self.calculator.add_item('B', 2.0, 1)
        items = self.calculator.list_items()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 1.0)
        self.assertFalse(self.calculator.is_empty())