import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_defaults(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.total_items(), 0)

    def test_init_custom_valid(self):
        calc = OrderCalculator(tax_rate=0.05, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())

    def test_init_boundary_tax(self):
        calc_low = OrderCalculator(tax_rate=0.0)
        calc_high = OrderCalculator(tax_rate=1.0)
        self.assertTrue(calc_low.is_empty())
        self.assertTrue(calc_high.is_empty())

    def test_init_zero_threshold_shipping(self):
        calc = OrderCalculator(free_shipping_threshold=0.0, shipping_cost=0.0)
        self.assertTrue(calc.is_empty())

    def test_init_invalid_tax_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_negative_shipping(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calc.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calc.total_items(), 2)
        self.assertFalse(self.calc.is_empty())

    def test_add_item_default_quantity(self):
        self.calc.add_item('Banana', 0.5)
        self.assertEqual(self.calc.total_items(), 1)

    def test_add_item_accumulate_quantity(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Apple', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', 0.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadPrice', -5.0)

    def test_add_item_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, 0)
        with self.assertRaises(ValueError):
            self.calc.add_item('BadQty', 10.0, -1)

    def test_add_item_name_conflict_diff_price(self):
        self.calc.add_item('ItemA', 10.0)
        with self.assertRaises(ValueError):
            self.calc.add_item('ItemA', 12.0)

    def test_add_item_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('ItemB', '10.0')

    def test_remove_item_valid(self):
        self.calc.add_item('RemoveMe', 10.0)
        self.calc.remove_item('RemoveMe')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('GhostItem')

    def test_remove_item_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(123)

    def test_get_subtotal_multiple_items(self):
        self.calc.add_item('A', 10.0, 1)
        self.calc.add_item('B', 20.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 30.0)

    def test_get_subtotal_with_quantities(self):
        self.calc.add_item('A', 10.0, 2)
        self.calc.add_item('B', 5.0, 4)
        self.assertEqual(self.calc.get_subtotal(), 40.0)

    def test_get_subtotal_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_range(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_invalid_types(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_standard(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertEqual(calc.calculate_total(), 66.0)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=40.0, shipping_cost=10.0)
        calc.add_item('Item', 50.0, 1)
        self.assertEqual(calc.calculate_total(), 55.0)

    def test_calculate_total_zero_discount(self):
        calc = OrderCalculator(tax_rate=0.0, free_shipping_threshold=1000.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        self.assertEqual(calc.calculate_total(discount=0.0), 110.0)

    def test_calculate_total_full_discount(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item', 100.0, 1)
        self.assertEqual(calc.calculate_total(discount=1.0), 11.0)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_invalid_type_discount(self):
        self.calc.add_item('Item', 10.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='0.1')

    def test_total_items_multiple(self):
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 8)

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0)
        self.assertFalse(self.calc.is_empty())

    def test_list_items(self):
        self.calc.add_item('A', 1.0)
        self.calc.add_item('B', 1.0)
        items = self.calc.list_items()
        self.assertEqual(set(items), {'A', 'B'})

    def test_list_items_empty(self):
        self.assertEqual(self.calc.list_items(), [])

    def test_clear_order(self):
        self.calc.add_item('A', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)