import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom_valid_values(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        self.assertEqual(calc.calculate_tax(100), 10.0)
        self.assertEqual(calc.calculate_shipping(150), 15.0)
        self.assertEqual(calc.calculate_shipping(250), 0.0)

    def test_init_invalid_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_shipping_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single_default_quantity(self):
        self.calculator.add_item('Apple', 2.0)
        self.assertEqual(self.calculator.total_items(), 1)
        self.assertIn('Apple', self.calculator.list_items()[0])

    def test_add_item_custom_quantity(self):
        self.calculator.add_item('Apple', 2.0, 5)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_multiple_items(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)
        self.assertEqual(len(self.calculator.list_items()), 2)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -2.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, 0)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0, -1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 2.0)

    def test_remove_existing_item(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_non_existent_item(self):
        with self.assertRaises((ValueError, KeyError)):
            self.calculator.remove_item('Orange')

    def test_clear_non_empty_order(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_empty_order(self):
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_new_instance(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 2.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_removing_all(self):
        self.calculator.add_item('Apple', 2.0)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_total_items_count(self):
        self.calculator.add_item('Apple', 2.0, 2)
        self.calculator.add_item('Orange', 3.0, 1)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_list_items_format(self):
        self.calculator.add_item('Apple', 2.0, 1)
        items = self.calculator.list_items()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], str)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 10.0, 2)
        self.calculator.add_item('Orange', 5.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_apply_discount_zero(self):
        subtotal = 100.0
        self.assertEqual(self.calculator.apply_discount(subtotal, 0.0), 100.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        threshold = self.calculator.free_shipping_threshold
        self.assertEqual(self.calculator.calculate_shipping(threshold), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_standard(self):
        self.calculator = OrderCalculator(tax_rate=0.2)
        self.assertEqual(self.calculator.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_zero_rate(self):
        calc = OrderCalculator(tax_rate=0.0)
        self.assertEqual(calc.calculate_tax(100.0), 0.0)

    def test_calculate_total_without_discount(self):
        self.calculator.add_item('Item', 50.0, 1)
        subtotal = 50.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calculator.calculate_total(), expected)