import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_default_parameters(self):
        calc = OrderCalculator()
        self.assertEqual(calc.calculate_total(), 0.0)

    def test_init_custom_tax_rate(self):
        calc = OrderCalculator(tax_rate=0.15)
        calc.add_item('Item', 100.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 125.0)

    def test_init_custom_free_shipping_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=50.0)
        calc.add_item('Item', 60.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_init_custom_shipping_cost(self):
        calc = OrderCalculator(shipping_cost=15.0)
        calc.add_item('Item', 10.0)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 30.75)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.get_subtotal(), 1.5)

    def test_add_item_with_quantity(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_add_item_multiple_different(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.add_item('Banana', 2.0)
        self.assertEqual(self.calculator.get_subtotal(), 3.5)

    def test_add_item_same_name_accumulates(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 7.5)

    def test_add_item_zero_quantity(self):
        self.calculator.add_item('Apple', 1.5, 0)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, -1)

    def test_add_item_zero_price(self):
        self.calculator.add_item('Free', 0.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)

    def test_add_item_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.5)

    def test_add_item_invalid_price_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', '1.5')

    def test_add_item_invalid_quantity_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item('Apple', 1.5, '3')

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_remove_item_nonexistent(self):
        with self.assertRaises(KeyError):
            self.calculator.remove_item('Apple')

    def test_remove_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_empty(self):
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_get_subtotal_single_item(self):
        self.calculator.add_item('Apple', 2.5)
        self.assertEqual(self.calculator.get_subtotal(), 2.5)

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 2.5)
        self.calculator.add_item('Banana', 3.0)
        self.assertEqual(self.calculator.get_subtotal(), 5.5)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_partial(self):
        result = self.calculator.apply_discount(100.0, 20.0)
        self.assertEqual(result, 80.0)

    def test_apply_discount_full(self):
        result = self.calculator.apply_discount(100.0, 100.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_over_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 101.0)

    def test_apply_discount_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_apply_discount_invalid_subtotal_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount('100', 10.0)

    def test_apply_discount_invalid_discount_type(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10')

    def test_calculate_shipping_below_threshold(self):
        result = self.calculator.calculate_shipping(50.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_at_threshold(self):
        result = self.calculator.calculate_shipping(100.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_above_threshold(self):
        result = self.calculator.calculate_shipping(150.0)
        self.assertEqual(result, 0.0)

    def test_calculate_shipping_zero_amount(self):
        result = self.calculator.calculate_shipping(0.0)
        self.assertEqual(result, 10.0)

    def test_calculate_shipping_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_shipping(-10.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('50')

    def test_calculate_tax_positive_amount(self):
        result = self.calculator.calculate_tax(100.0)
        self.assertAlmostEqual(result, 23.0)

    def test_calculate_tax_zero_amount(self):
        result = self.calculator.calculate_tax(0.0)
        self.assertEqual(result, 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('100')

    def test_calculate_total_empty_order(self):
        total = self.calculator.calculate_total()
        self.assertEqual(total, 0.0)

    def test_calculate_total_no_discount(self):
        self.calculator.add_item('Item', 100.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 133.3)

    def test_calculate_total_with_discount(self):
        self.calculator.add_item('Item', 100.0)
        total = self.calculator.calculate_total(20.0)
        self.assertAlmostEqual(total, 110.64)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 150.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 184.5)

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item', 50.0)
        total = self.calculator.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_negative_discount(self):
        self.calculator.add_item('Item', 100.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(-10.0)

    def test_calculate_total_discount_exceeds_subtotal(self):
        self.calculator.add_item('Item', 50.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(60.0)

    def test_calculate_total_invalid_discount_type(self):
        self.calculator.add_item('Item', 100.0)
        with self.assertRaises(TypeError):
            self.calculator.calculate_total('10')

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_single(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_total_items_multiple(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Banana', 2.0, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_clear_order(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)
        self.assertEqual(self.calculator.total_items(), 0)

    def test_clear_order_already_empty(self):
        self.calculator.clear_order()
        self.assertEqual(self.calculator.get_subtotal(), 0.0)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_single(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.list_items(), ['Apple'])

    def test_list_items_multiple(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.add_item('Banana', 2.0)
        items = self.calculator.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_is_empty_initially(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_add(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertFalse(self.calculator.is_empty())

    def test_is_empty_after_remove(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_after_clear(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())