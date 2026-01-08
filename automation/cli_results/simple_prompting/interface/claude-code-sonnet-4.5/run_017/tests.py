import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_total(), 0.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 125.0)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=200.0)
        calc.add_item('Item', 150.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertEqual(shipping, 10.0)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('Item', 50.0)
        shipping = calc.calculate_shipping(50.0)
        self.assertEqual(shipping, 15.0)

    def test_add_item_single(self):
        self.calculator.add_item('Book', 20.0)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_add_item_with_quantity(self):
        self.calculator.add_item('Pen', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 15.0)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.add_item('Pen', 5.0)
        self.assertEqual(self.calculator.get_subtotal(), 25.0)

    def test_add_item_same_name_updates_quantity(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Book', 20.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 100.0)

    def test_add_item_zero_quantity(self):
        self.calculator.add_item('Item', 10.0, 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', 10.0, -1)

    def test_add_item_zero_price(self):
        self.calculator.add_item('Free', 0.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Item', -10.0, 1)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 10.0, 1)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 10.0, 1)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 'ten', 1)

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Item', 10.0, 'one')

    def test_remove_item_existing(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.remove_item('Book')
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('NonExistent')

    def test_remove_item_from_empty(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Item')

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Book', 20.0)
        self.assertEqual(self.calculator.get_subtotal(), 20.0)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Pen', 5.0, 3)
        self.assertEqual(self.calculator.get_subtotal(), 55.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.1)
        self.assertAlmostEqual(result, 90.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_over_one(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.5)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-100.0, 0.1)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, 'ten')

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('hundred', 0.1)

    def test_calculate_shipping_below_threshold(self):
        shipping = self.calculator.calculate_shipping(50.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_at_threshold(self):
        shipping = self.calculator.calculate_shipping(100.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_above_threshold(self):
        shipping = self.calculator.calculate_shipping(150.0)
        self.assertEqual(shipping, 0.0)

    def test_calculate_shipping_zero_amount(self):
        shipping = self.calculator.calculate_shipping(0.0)
        self.assertEqual(shipping, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-50.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('fifty')

    def test_calculate_tax_zero(self):
        tax = self.calculator.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_positive(self):
        tax = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 23.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('hundred')

    def test_calculate_total_empty(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Book', 50.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Book', 100.0)
        total = self.calculator.calculate_total(0.1)
        self.assertAlmostEqual(total, 110.7)

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Book', 50.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 71.5)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Book', 100.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('Book', 50.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-0.1)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Book', 50.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('ten')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Book', 20.0, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Pen', 5.0, 5)
        self.assertEqual(self.calculator.total_items(), 7)

    def test_clear_order_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_clear_order_with_items(self):
        self.calculator.add_item('Book', 20.0, 2)
        self.calculator.add_item('Pen', 5.0)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.total_items(), 0)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single(self):
        self.calculator.add_item('Book', 20.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 1)
        self.assertIn('Book', items)

    def test_list_items_multiple(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.add_item('Pen', 5.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('Book', items)
        self.assertIn('Pen', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('Book', 20.0)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_remove_all(self):
        self.calculator.add_item('Book', 20.0)
        self.calculator.remove_item('Book')
        self.assertTrue(self.calculator.is_empty())