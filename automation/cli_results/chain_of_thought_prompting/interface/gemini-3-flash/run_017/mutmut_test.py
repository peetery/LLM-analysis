import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_custom_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.calculate_tax(100.0), 10.0)
        self.assertEqual(calc.calculate_shipping(40.0), 5.0)
        self.assertEqual(calc.calculate_shipping(60.0), 0.0)

    def test_init_invalid_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_single(self):
        self.calculator.add_item('Apple', 1.5)
        self.assertEqual(self.calculator.get_subtotal(), 1.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_item_quantity_greater_than_one(self):
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)
        self.assertEqual(self.calculator.total_items(), 3)

    def test_add_item_duplicate_name_updates_quantity(self):
        self.calculator.add_item('Apple', 1.5, 1)
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 3)
        self.assertEqual(self.calculator.get_subtotal(), 4.5)

    def test_add_item_invalid_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', -1.0)

    def test_add_item_invalid_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 1.5, 0)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.5)

    def test_remove_item_normal(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_get_subtotal_multiple_items(self):
        self.calculator.add_item('Apple', 1.0, 2)
        self.calculator.add_item('Banana', 2.0, 1)
        self.assertEqual(self.calculator.get_subtotal(), 4.0)

    def test_get_subtotal_after_item_removal(self):
        self.calculator.add_item('Apple', 10.0)
        self.calculator.add_item('Banana', 5.0)
        self.calculator.remove_item('Apple')
        self.assertEqual(self.calculator.get_subtotal(), 5.0)

    def test_apply_discount_zero(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_negative_raises_exception(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -10.0)

    def test_calculate_shipping_below_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(99.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(101.0), 0.0)

    def test_calculate_shipping_exact_threshold(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_zero_subtotal(self):
        self.assertEqual(self.calculator.calculate_shipping(0.0), 10.0)

    def test_calculate_tax_normal(self):
        calc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        self.assertEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_raises_exception(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-100.0)

    def test_calculate_total_no_discount_provided(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Product', 100.0, 1)
        total = calc.calculate_total()
        self.assertAlmostEqual(total, 110.0)

    def test_total_items_returns_sum_of_quantities(self):
        self.calculator.add_item('Apple', 1.0, 5)
        self.calculator.add_item('Banana', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_list_items_returns_names(self):
        self.calculator.add_item('Apple', 1.0)
        self.calculator.add_item('Banana', 1.0)
        names = self.calculator.list_items()
        self.assertCountEqual(names, ['Apple', 'Banana'])

    def test_is_empty_reflects_state(self):
        self.assertTrue(self.calculator.is_empty())
        self.calculator.add_item('Apple', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_precision_with_floating_point_values(self):
        self.calculator.add_item('Item 1', 0.1)
        self.calculator.add_item('Item 2', 0.2)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 0.3)