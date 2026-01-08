import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold='100')
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost='10')

    def test_init_invalid_values(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_valid_new(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_valid_existing(self):
        self.calculator.add_item('Apple', 1.5, 10)
        self.calculator.add_item('Apple', 1.5, 5)
        self.assertEqual(len(self.calculator.items), 1)
        self.assertEqual(self.calculator.items[0]['quantity'], 15)

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.items[0]['quantity'], 1)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0, 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.0', 1)
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.0, '1')

    def test_add_item_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.0, 0)

    def test_add_item_duplicate_name_different_price(self):
        self.calculator.add_item('Apple', 1.0, 1)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 1)

    def test_remove_item_valid(self):
        self.calculator.add_item('Apple', 1.0, 1)
        self.calculator.remove_item('Apple')
        self.assertEqual(len(self.calculator.items), 0)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('Apple', 2.0, 3)
        self.calculator.add_item('Banana', 1.0, 5)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 11.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '0.1')

    def test_apply_discount_invalid_values(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-50.0)

    def test_calculate_total_standard_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 66.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 110.0)

    def test_calculate_total_with_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 100.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.2), 99.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('A', 10, 1)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total(discount='0.1')

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_total_items(self):
        self.assertEqual(self.calculator.total_items(), 0)
        self.calculator.add_item('A', 10, 2)
        self.calculator.add_item('B', 5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('A', 10, 1)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.items, [])
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items(self):
        self.assertEqual(self.calculator.list_items(), [])
        self.calculator.add_item('A', 10, 1)
        self.calculator.add_item('B', 5, 1)
        self.calculator.add_item('A', 10, 1)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('A', 10, 1)
        self.assertFalse(self.calculator.is_empty())
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())