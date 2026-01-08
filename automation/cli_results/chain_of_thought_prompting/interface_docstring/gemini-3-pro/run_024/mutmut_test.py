import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = OrderCalculator()

    def test_init_defaults(self):
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)

    def test_init_custom_valid_parameters(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(calc.is_empty())
        calc.add_item('Test', 100.0)
        self.assertAlmostEqual(calc.calculate_total(), 110.0)

    def test_init_invalid_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.01)

    def test_init_invalid_high_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.01)

    def test_init_invalid_negative_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_negative_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_valid(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.assertEqual(self.calculator.total_items(), 2)
        self.assertIn('Apple', self.calculator.list_items())

    def test_add_item_default_quantity(self):
        self.calculator.add_item('Banana', 0.5)
        self.assertEqual(self.calculator.total_items(), 1)

    def test_add_existing_item_increments_quantity(self):
        self.calculator.add_item('Apple', 1.5, 2)
        self.calculator.add_item('Apple', 1.5, 3)
        self.assertEqual(self.calculator.total_items(), 5)

    def test_add_item_empty_name(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('', 1.0)

    def test_add_item_zero_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Freebie', 0.0)

    def test_add_item_negative_price(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Debt', -5.0)

    def test_add_item_zero_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('Ghost', 1.0, 0)

    def test_add_item_negative_quantity(self):
        with self.assertRaises(ValueError):
            self.calculator.add_item('AntiMatter', 1.0, -1)

    def test_add_item_price_conflict(self):
        self.calculator.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            self.calculator.add_item('Apple', 2.0)

    def test_add_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.add_item(123, 1.0)

    def test_remove_item_existing(self):
        self.calculator.add_item('Apple', 1.5)
        self.calculator.remove_item('Apple')
        self.assertTrue(self.calculator.is_empty())

    def test_remove_item_non_existent(self):
        with self.assertRaises(ValueError):
            self.calculator.remove_item('Ghost')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.remove_item(123)

    def test_get_subtotal_valid(self):
        self.calculator.add_item('A', 10.0, 2)
        self.calculator.add_item('B', 5.0, 3)
        self.assertAlmostEqual(self.calculator.get_subtotal(), 35.0)

    def test_get_subtotal_empty(self):
        with self.assertRaises(ValueError):
            self.calculator.get_subtotal()

    def test_apply_discount_valid(self):
        result = self.calculator.apply_discount(100.0, 0.2)
        self.assertAlmostEqual(result, 80.0)

    def test_apply_discount_zero_percent(self):
        result = self.calculator.apply_discount(100.0, 0.0)
        self.assertAlmostEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        result = self.calculator.apply_discount(100.0, 1.0)
        self.assertAlmostEqual(result, 0.0)

    def test_apply_discount_negative_rate(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, -0.1)

    def test_apply_discount_over_hundred_percent(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calculator.apply_discount(-10.0, 0.1)

    def test_apply_discount_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.apply_discount(100.0, '10%')

    def test_calculate_shipping_below_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(99.99), 10.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertAlmostEqual(self.calculator.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_shipping('high')

    def test_calculate_tax_valid(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(100.0), 23.0)

    def test_calculate_tax_zero_amount(self):
        self.assertAlmostEqual(self.calculator.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calculator.calculate_tax('money')

    def test_calculate_total_with_shipping(self):
        self.calculator.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 73.8)

    def test_calculate_total_free_shipping(self):
        self.calculator.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(), 246.0)

    def test_calculate_total_with_specific_discount(self):
        self.calculator.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(self.calculator.calculate_total(discount=0.2), 110.7)

    def test_calculate_total_empty_order(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_total()

    def test_calculate_total_invalid_discount(self):
        self.calculator.add_item('Item', 10.0)
        with self.assertRaises(ValueError):
            self.calculator.calculate_total(discount=2.0)

    def test_total_items_empty(self):
        self.assertEqual(self.calculator.total_items(), 0)

    def test_total_items_populated(self):
        self.calculator.add_item('A', 1.0, 5)
        self.calculator.add_item('B', 1.0, 3)
        self.assertEqual(self.calculator.total_items(), 8)

    def test_list_items_empty(self):
        self.assertEqual(self.calculator.list_items(), [])

    def test_list_items_populated(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.add_item('B', 1.0)
        items = self.calculator.list_items()
        self.assertEqual(len(items), 2)
        self.assertIn('A', items)
        self.assertIn('B', items)

    def test_is_empty_true(self):
        self.assertTrue(self.calculator.is_empty())

    def test_is_empty_false(self):
        self.calculator.add_item('A', 1.0)
        self.assertFalse(self.calculator.is_empty())

    def test_clear_order(self):
        self.calculator.add_item('A', 1.0)
        self.calculator.clear_order()
        self.assertTrue(self.calculator.is_empty())
        self.assertEqual(self.calculator.total_items(), 0)