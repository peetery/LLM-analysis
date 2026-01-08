import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.5)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='high')

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertFalse(calc.is_empty())
        self.assertEqual(calc.total_items(), 10)

    def test_add_item_existing_update(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        calc.add_item('Apple', 1.5, 5)
        self.assertEqual(calc.total_items(), 15)

    def test_add_item_invalid_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.5)

    def test_add_item_invalid_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)
        with self.assertRaises(ValueError):
            calc.add_item('Banana', -1.0)

    def test_add_item_invalid_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.5, 0)

    def test_add_item_duplicate_name_diff_price(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 'cheap')

    def test_remove_item_success(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('NonExistent')

    def test_remove_item_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_calculation(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.0, 5)
        self.assertEqual(calc.get_subtotal(), 11.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_calculation(self):
        calc = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calc.apply_discount(subtotal, 0.2), 80.0)

    def test_apply_discount_limits(self):
        calc = OrderCalculator()
        subtotal = 100.0
        self.assertEqual(calc.apply_discount(subtotal, 0.0), 100.0)
        self.assertEqual(calc.apply_discount(subtotal, 1.0), 0.0)

    def test_apply_discount_invalid_value(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_calculation(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_flow(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(discount=0.0), 66.0)
        self.assertAlmostEqual(calc.calculate_total(discount=0.5), 38.5)

    def test_calculate_total_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=2.0)

    def test_total_items(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 2.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.0)
        calc.add_item('Banana', 1.0)
        items = calc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('A', 1.0)
        self.assertFalse(calc.is_empty())