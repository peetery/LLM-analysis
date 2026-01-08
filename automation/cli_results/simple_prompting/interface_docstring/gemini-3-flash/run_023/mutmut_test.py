import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_raises_value_error_tax_rate(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_raises_value_error_threshold(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_raises_value_error_shipping_cost(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_raises_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.2')
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[10])

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.assertEqual(self.calc.total_items(), 4)
        self.assertIn('Apple', self.calc.list_items())

    def test_add_item_increment_quantity(self):
        self.calc.add_item('Apple', 2.5, 4)
        self.calc.add_item('Apple', 2.5, 2)
        self.assertEqual(self.calc.total_items(), 6)

    def test_add_item_raises_value_error_empty_name(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 2.5, 1)

    def test_add_item_raises_value_error_invalid_price(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 0.0, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', -1.0, 1)

    def test_add_item_raises_value_error_invalid_quantity(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, 0)

    def test_add_item_raises_value_error_conflicting_price(self):
        self.calc.add_item('Apple', 2.5, 1)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0, 1)

    def test_add_item_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 2.5, 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', '2.5', 1)
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.5, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.5, 1)
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())

    def test_remove_item_raises_value_error_not_found(self):
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 2.0, 5)
        self.calc.add_item('Banana', 5.0, 2)
        self.assertEqual(self.calc.get_subtotal(), 20.0)

    def test_get_subtotal_raises_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        self.assertEqual(self.calc.apply_discount(200.0, 0.1), 180.0)
        self.assertEqual(self.calc.apply_discount(200.0, 0.0), 200.0)
        self.assertEqual(self.calc.apply_discount(200.0, 1.0), 0.0)

    def test_apply_discount_raises_value_error_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_raises_value_error_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, None)

    def test_calculate_shipping_standard(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)
        self.assertEqual(self.calc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_free(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping('50')

    def test_calculate_tax_success(self):
        self.assertAlmostEqual(self.calc.calculate_tax(100.0), 23.0)
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_raises_value_error_negative(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax(None)

    def test_calculate_total_full_process(self):
        self.calc.add_item('Box', 25.0, 2)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.2), 61.5)

    def test_calculate_total_with_free_shipping(self):
        self.calc.add_item('TV', 200.0, 1)
        self.assertAlmostEqual(self.calc.calculate_total(discount=0.0), 246.0)

    def test_calculate_total_raises_value_error_empty(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_raises_value_error_invalid_discount(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            self.calc.calculate_total(discount=1.5)

    def test_calculate_total_raises_type_error(self):
        self.calc.add_item('Item', 10.0, 1)
        with self.assertRaises(TypeError):
            self.calc.calculate_total(discount='high')

    def test_total_items_empty_and_multiple(self):
        self.assertEqual(self.calc.total_items(), 0)
        self.calc.add_item('A', 1.0, 5)
        self.calc.add_item('B', 1.0, 10)
        self.assertEqual(self.calc.total_items(), 15)

    def test_clear_order(self):
        self.calc.add_item('A', 1.0, 1)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(self.calc.total_items(), 0)

    def test_list_items(self):
        self.assertEqual(self.calc.list_items(), [])
        self.calc.add_item('A', 1.0, 1)
        self.calc.add_item('B', 1.0, 1)
        self.calc.add_item('A', 1.0, 1)
        items = self.calc.list_items()
        self.assertEqual(len(items), 2)
        self.assertCountEqual(items, ['A', 'B'])

    def test_is_empty(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('A', 1.0, 1)
        self.assertFalse(self.calc.is_empty())