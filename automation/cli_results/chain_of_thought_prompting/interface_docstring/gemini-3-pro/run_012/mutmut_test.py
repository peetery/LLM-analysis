import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertAlmostEqual(calc.tax_rate, 0.23)
        self.assertAlmostEqual(calc.free_shipping_threshold, 100.0)
        self.assertAlmostEqual(calc.shipping_cost, 10.0)
        self.assertTrue(calc.is_empty())

    def test_init_custom_values(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertAlmostEqual(calc.tax_rate, 0.05)
        self.assertAlmostEqual(calc.free_shipping_threshold, 50.0)
        self.assertAlmostEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid_single(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 1)
        self.assertEqual(calc.total_items(), 1)
        self.assertFalse(calc.is_empty())

    def test_add_item_valid_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5, 10)
        self.assertEqual(calc.total_items(), 10)

    def test_add_item_stacking(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 2)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(calc.total_items(), 5)
        self.assertEqual(len(calc.list_items()), 1)

    def test_add_item_invalid_name_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 10.0)

    def test_add_item_invalid_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Freebie', 0.0)

    def test_add_item_invalid_price_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Debt', -10.0)

    def test_add_item_invalid_quantity_low(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Ghost', 10.0, 0)

    def test_add_item_price_conflict(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            calc.add_item('ItemA', 12.0)

    def test_add_item_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('ItemA', '10.0')

    def test_remove_item_existing(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        calc.remove_item('ItemA')
        self.assertTrue(calc.is_empty())

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            calc.remove_item('ItemB')

    def test_remove_item_from_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('ItemA')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_valid(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0, 2)
        calc.add_item('ItemB', 5.0, 1)
        self.assertAlmostEqual(calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_full(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_invalid_negative(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-10.0, 0.1)

    def test_apply_discount_invalid_types(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount(100.0, '0.1')

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(99.99)
        self.assertAlmostEqual(shipping, 10.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(100.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        shipping = calc.calculate_shipping(150.0)
        self.assertAlmostEqual(shipping, 0.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('100')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(100.0)
        self.assertAlmostEqual(tax, 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(0.0)
        self.assertAlmostEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax('100')

    def test_calculate_total_no_discount_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('ItemA', 50.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 73.8)

    def test_calculate_total_no_discount_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('ItemA', 150.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 184.5)

    def test_calculate_total_with_discount_drops_below_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('ItemA', 100.0, 1)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 123.0)

    def test_calculate_total_with_discount_stays_above_threshold(self):
        calc = OrderCalculator(tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('ItemA', 200.0, 1)
        total = calc.calculate_total(discount=0.1)
        self.assertAlmostEqual(total, 221.4)

    def test_calculate_total_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        calc = OrderCalculator()
        calc.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            calc.calculate_total(discount=-0.1)

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 1, 2)
        calc.add_item('B', 1, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        calc.add_item('B', 20)
        items = calc.list_items()
        self.assertEqual(sorted(items), ['A', 'B'])

    def test_is_empty(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        calc.add_item('A', 10)
        self.assertFalse(calc.is_empty())

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)