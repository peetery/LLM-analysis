import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = OrderCalculator()

    def test_init_default_values(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom_values(self):
        calc = OrderCalculator(0.05, 50.0, 5.0)
        self.assertEqual(calc.tax_rate, 0.05)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_tax_rate_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_threshold_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=[100])

    def test_init_shipping_cost_type_error(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=None)

    def test_init_tax_rate_below_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_tax_rate_above_range(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-5.0)

    def test_init_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_add_item_success(self):
        self.calc.add_item('Apple', 2.5)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['name'], 'Apple')
        self.assertEqual(self.calc.items[0]['price'], 2.5)
        self.assertEqual(self.calc.items[0]['quantity'], 1)

    def test_add_item_with_quantity(self):
        self.calc.add_item('Orange', 3.0, 5)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_merge_quantity(self):
        self.calc.add_item('Apple', 2.5, 2)
        self.calc.add_item('Apple', 2.5, 3)
        self.assertEqual(len(self.calc.items), 1)
        self.assertEqual(self.calc.items[0]['quantity'], 5)

    def test_add_item_empty_name_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('', 10.0)

    def test_add_item_zero_price_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Freebie', 0)

    def test_add_item_negative_price_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Debt', -5.0)

    def test_add_item_zero_quantity_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, 0)

    def test_add_item_negative_quantity_error(self):
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 2.5, -1)

    def test_add_item_price_conflict_error(self):
        self.calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            self.calc.add_item('Apple', 3.0)

    def test_add_item_name_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item(123, 10.0)

    def test_add_item_price_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 'expensive')

    def test_add_item_quantity_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.add_item('Apple', 2.5, 1.5)

    def test_remove_item_success(self):
        self.calc.add_item('Apple', 2.5)
        self.calc.remove_item('Apple')
        self.assertEqual(len(self.calc.items), 0)

    def test_remove_item_not_found_error(self):
        self.calc.add_item('Apple', 2.5)
        with self.assertRaises(ValueError):
            self.calc.remove_item('Banana')

    def test_remove_item_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.remove_item(None)

    def test_get_subtotal_success(self):
        self.calc.add_item('Apple', 10.0, 2)
        self.calc.add_item('Orange', 5.0, 1)
        self.assertEqual(self.calc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_error(self):
        with self.assertRaises(ValueError):
            self.calc.get_subtotal()

    def test_apply_discount_success(self):
        result = self.calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        result = self.calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        result = self.calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_out_of_range_low(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, -0.1)

    def test_apply_discount_out_of_range_high(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(100.0, 1.1)

    def test_apply_discount_negative_subtotal(self):
        with self.assertRaises(ValueError):
            self.calc.apply_discount(-50.0, 0.1)

    def test_apply_discount_subtotal_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount('100', 0.1)

    def test_apply_discount_rate_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.apply_discount(100.0, '10%')

    def test_calculate_shipping_below_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_above_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(150.0), 0.0)

    def test_calculate_shipping_at_threshold(self):
        self.assertEqual(self.calc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_shipping(None)

    def test_calculate_tax_success(self):
        self.calc.tax_rate = 0.2
        self.assertEqual(self.calc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero(self):
        self.assertEqual(self.calc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_tax(-10.0)

    def test_calculate_tax_type_error(self):
        with self.assertRaises(TypeError):
            self.calc.calculate_tax('100')

    def test_calculate_total_no_discount_shipping(self):
        self.calc.add_item('Gadget', 40.0, 1)
        subtotal = 40.0
        shipping = 10.0
        tax = (subtotal + shipping) * 0.23
        expected = subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.0), expected)

    def test_calculate_total_with_discount_free_shipping(self):
        self.calc.add_item('Gadget', 200.0, 1)
        discounted_subtotal = 160.0
        shipping = 0.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected)

    def test_calculate_total_discount_triggers_shipping(self):
        self.calc.add_item('Gadget', 110.0, 1)
        discounted_subtotal = 88.0
        shipping = 10.0
        tax = (discounted_subtotal + shipping) * 0.23
        expected = discounted_subtotal + shipping + tax
        self.assertAlmostEqual(self.calc.calculate_total(0.2), expected)

    def test_calculate_total_empty_order_error(self):
        with self.assertRaises(ValueError):
            self.calc.calculate_total()

    def test_calculate_total_discount_type_error(self):
        self.calc.add_item('Apple', 2.0)
        with self.assertRaises(TypeError):
            self.calc.calculate_total('20%')

    def test_total_items_empty(self):
        self.assertEqual(self.calc.total_items(), 0)

    def test_total_items_multiple(self):
        self.calc.add_item('Apple', 1.0, 2)
        self.calc.add_item('Orange', 1.0, 3)
        self.assertEqual(self.calc.total_items(), 5)

    def test_clear_order(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.clear_order()
        self.assertTrue(self.calc.is_empty())
        self.assertEqual(len(self.calc.items), 0)

    def test_list_items_unique(self):
        self.calc.add_item('Apple', 1.0)
        self.calc.add_item('Orange', 2.0)
        self.calc.add_item('Apple', 1.0)
        names = self.calc.list_items()
        self.assertEqual(len(names), 2)
        self.assertIn('Apple', names)
        self.assertIn('Orange', names)

    def test_is_empty_lifecycle(self):
        self.assertTrue(self.calc.is_empty())
        self.calc.add_item('Apple', 1.0)
        self.assertFalse(self.calc.is_empty())
        self.calc.remove_item('Apple')
        self.assertTrue(self.calc.is_empty())