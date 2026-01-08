import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=15.0)

    def test_init_defaults(self):
        c = OrderCalculator()
        self.assertEqual(c.tax_rate, 0.23)
        self.assertEqual(c.free_shipping_threshold, 100.0)
        self.assertEqual(c.shipping_cost, 10.0)
        self.assertEqual(c.items, [])

    def test_init_custom_values(self):
        c = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(c.tax_rate, 0.1)
        self.assertEqual(c.free_shipping_threshold, 50.0)
        self.assertEqual(c.shipping_cost, 5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')

    def test_init_invalid_type_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_init_invalid_value_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_value_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_value_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_value_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_valid_new_item(self):
        self.calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_valid_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_valid_update_quantity(self):
        self.calc.add_item('Apple', 1.0, 5)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 8)

    def test_add_item_invalid_conflict_price(self):
        self.calc.add_item('Apple', 1.0, 5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_bad_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Freebie', 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)

    def test_add_item_invalid_bad_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 1.0, 0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '10.0')
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 10.0, 1.5)

    def test_remove_item_valid(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Banana', 2.0)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Banana')

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Ghost')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calc.add_item('Item1', 10.0, 2)
        self.calc.add_item('Item2', 5.5, 4)
        self.assertAlmostEqual(self.calc.get_subtotal(), 42.0)

    def test_get_subtotal_single_item(self):
        self.calc.add_item('Item1', 10.0, 1)
        self.assertAlmostEqual(self.calc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_exception(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero_percent(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full_percent(self):
        self.assertAlmostEqual(self.calc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_cost_applied(self):
        self.assertEqual(self.calc.calculate_shipping(99.9), 15.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_standard(self):
        self.calc.add_item('Item1', 50.0, 2)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 126.0)

    def test_calculate_total_free_shipping(self):
        self.calc.add_item('Item1', 100.0, 2)
        total = self.calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 216.0)

    def test_calculate_total_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        self.calc.add_item('Item', 10, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 10, 2)
        self.calc.add_item('B', 20, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('A', 10, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.items), 0)

    def test_list_items(self):
        self.calc.add_item('Apple', 1, 1)
        self.calc.add_item('Banana', 1, 1)
        self.calc.add_item('Apple', 1, 5)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Item', 1)
        self.assertFalse(self.calc.is_empty())