import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default(self):
        calc = OrderCalculator()
        self.assertEqual(calc.tax_rate, 0.23)
        self.assertEqual(calc.free_shipping_threshold, 100.0)
        self.assertEqual(calc.shipping_cost, 10.0)
        self.assertEqual(calc.items, [])

    def test_init_custom(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(calc.tax_rate, 0.1)
        self.assertEqual(calc.free_shipping_threshold, 50.0)
        self.assertEqual(calc.shipping_cost, 5.0)

    def test_init_invalid_type_tax_rate(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_init_invalid_type_threshold(self):
        with self.assertRaises(TypeError):
            OrderCalculator(free_shipping_threshold=None)

    def test_init_invalid_type_shipping_cost(self):
        with self.assertRaises(TypeError):
            OrderCalculator(shipping_cost=[])

    def test_init_invalid_value_tax_rate_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_value_tax_rate_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_value_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_value_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_add_item_new(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 10)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0], {'name': 'Apple', 'price': 1.5, 'quantity': 10})

    def test_add_item_default_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Banana', 0.5)
        self.assertEqual(calc.items[0]['quantity'], 1)

    def test_add_item_update_quantity(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5, 5)
        calc.add_item('Apple', 1.5, 3)
        self.assertEqual(len(calc.items), 1)
        self.assertEqual(calc.items[0]['quantity'], 8)

    def test_add_item_invalid_type_name(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item(123, 1.0)

    def test_add_item_invalid_type_price(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', '1.0')

    def test_add_item_invalid_type_quantity(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.add_item('Apple', 1.0, 1.5)

    def test_add_item_invalid_value_empty_name(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('', 1.0)

    def test_add_item_invalid_value_price_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 0)

    def test_add_item_invalid_value_quantity_zero(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 1.0, 0)

    def test_add_item_price_conflict(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        with self.assertRaises(ValueError):
            calc.add_item('Apple', 2.0)

    def test_remove_item_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 1.5)
        calc.remove_item('Apple')
        self.assertEqual(len(calc.items), 0)

    def test_remove_item_non_existent(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.remove_item('Banana')

    def test_remove_item_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.remove_item(123)

    def test_get_subtotal_valid(self):
        calc = OrderCalculator()
        calc.add_item('Apple', 2.0, 3)
        calc.add_item('Banana', 1.0, 2)
        self.assertEqual(calc.get_subtotal(), 8.0)

    def test_get_subtotal_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.get_subtotal()

    def test_apply_discount_valid(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_hundred_percent(self):
        calc = OrderCalculator()
        result = calc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_invalid_type_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.apply_discount('100', 0.2)

    def test_apply_discount_invalid_value_range_high(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_value_negative_subtotal(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.apply_discount(-50.0, 0.2)

    def test_calculate_shipping_standard(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calc.calculate_shipping(99.9)
        self.assertEqual(cost, 10.0)

    def test_calculate_shipping_free(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calc.calculate_shipping(101.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_boundary(self):
        calc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        cost = calc.calculate_shipping(100.0)
        self.assertEqual(cost, 0.0)

    def test_calculate_shipping_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_shipping('50')

    def test_calculate_tax_valid(self):
        calc = OrderCalculator(tax_rate=0.2)
        tax = calc.calculate_tax(100.0)
        self.assertEqual(tax, 20.0)

    def test_calculate_tax_zero_amount(self):
        calc = OrderCalculator()
        tax = calc.calculate_tax(0.0)
        self.assertEqual(tax, 0.0)

    def test_calculate_tax_negative_amount(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax(None)

    def test_calculate_total_standard(self):
        calc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        calc.add_item('Item1', 50.0, 1)
        total = calc.calculate_total(discount=0.0)
        self.assertEqual(total, 72.0)

    def test_calculate_total_discounted(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=150.0, shipping_cost=10.0)
        calc.add_item('Item1', 200.0, 1)
        total = calc.calculate_total(discount=0.5)
        self.assertEqual(total, 121.0)

    def test_calculate_total_threshold_edge(self):
        calc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=90.0, shipping_cost=10.0)
        calc.add_item('Item1', 100.0, 1)
        total = calc.calculate_total(discount=0.1)
        self.assertEqual(total, 99.0)

    def test_calculate_total_empty(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        with self.assertRaises(TypeError):
            calc.calculate_total(discount='0.1')

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10, 2)
        calc.add_item('B', 20, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_total_items_empty(self):
        calc = OrderCalculator()
        self.assertEqual(calc.total_items(), 0)

    def test_list_items(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        calc.add_item('B', 20)
        calc.add_item('A', 10, 2)
        names = calc.list_items()
        self.assertEqual(len(names), 2)
        self.assertIn('A', names)
        self.assertIn('B', names)

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        self.assertFalse(calc.is_empty())

    def test_clear_order(self):
        calc = OrderCalculator()
        calc.add_item('A', 10)
        calc.clear_order()
        self.assertTrue(calc.is_empty())
        self.assertEqual(calc.items, [])