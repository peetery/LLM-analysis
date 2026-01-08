import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertEqual(calc.is_empty(), True)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=200.0, shipping_cost=15.0)
        calc.add_item('Test', 100.0, 1)
        self.assertEqual(calc.calculate_shipping(100.0), 15.0)

    def test_init_boundaries(self):
        calc_min = OrderCalculator(tax_rate=0.0)
        calc_max = OrderCalculator(tax_rate=1.0)
        self.assertEqual(calc_min.calculate_tax(100.0), 0.0)
        self.assertEqual(calc_max.calculate_tax(100.0), 100.0)

    def test_init_zero_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertEqual(calc.calculate_shipping(50.0), 0.0)

    def test_init_invalid_tax_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.total_items(), 5)
        self.assertIn('Apple', calc.list_items())

    def test_add_item_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Banana', 1.0, 10)
        self.assertEqual(calc.total_items(), 15)

    def test_add_item_increase_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Apple', 2.0, 3)
        self.assertEqual(calc.total_items(), 8)

    def test_add_item_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 2.0, 1)

    def test_add_item_zero_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0.0, 1)

    def test_add_item_negative_price(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', -1.0, 1)

    def test_add_item_zero_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0, 0)

    def test_add_item_price_mismatch(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 1)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 3.0, 1)

    def test_add_item_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 2.0, 1)

    def test_remove_item_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.remove_item('Apple')
        self.assertTrue(calc.is_empty())

    def test_remove_item_not_found(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(None)

    def test_get_subtotal_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        self.assertEqual(calc.get_subtotal(), 10.0)

    def test_get_subtotal_multiple(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 5)
        calc.add_item('Banana', 1.5, 2)
        self.assertEqual(calc.get_subtotal(), 13.0)

    def test_get_subtotal_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_rate_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_rate_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_basic(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.0), 66.0)

    def test_calculate_total_with_discount_and_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(calc.calculate_total(0.5), 110.0)

    def test_calculate_total_full_flow(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=50.0, shipping_cost=5.0)
        calc.add_item('A', 10.0, 2)
        calc.add_item('B', 5.0, 2)
        self.assertAlmostEqual(calc.calculate_total(0.1), 38.4)

    def test_calculate_total_empty_order(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            calc.calculate_total(1.5)

    def test_calculate_total_invalid_type(self):
        calc = OrderCalculator()
        calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total('0.1')

    def test_total_items_multiple(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 2)
        calc.add_item('B', 1.0, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_list_items_valid(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.add_item('B', 1.0, 1)
        self.assertCountEqual(calc.list_items(), ['A', 'B'])

    def test_list_items_no_duplicates(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        calc.add_item('A', 1.0, 2)
        self.assertEqual(calc.list_items(), ['A'])

    def test_list_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.list_items(), [])

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('A', 1.0, 1)
        self.assertFalse(calc.is_empty())