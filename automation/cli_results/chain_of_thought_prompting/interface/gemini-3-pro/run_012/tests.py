import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default_values(self):
        oc = OrderCalculator()
        self.assertEqual(oc.tax_rate, 0.23)
        self.assertEqual(oc.free_shipping_threshold, 100.0)
        self.assertEqual(oc.shipping_cost, 10.0)

    def test_init_custom_values(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertEqual(oc.tax_rate, 0.1)
        self.assertEqual(oc.free_shipping_threshold, 50.0)
        self.assertEqual(oc.shipping_cost, 5.0)

    def test_init_invalid_tax_rate_too_low(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_too_high(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-10.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-5.0)

    def test_init_invalid_type(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_new_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 10)
        self.assertIn('Apple', oc.list_items())
        self.assertEqual(oc.total_items(), 10)

    def test_add_item_update_quantity(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 5)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(oc.total_items(), 8)

    def test_add_item_conflict_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 5)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 2.0, 3)

    def test_add_item_invalid_name_empty(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 1.5)

    def test_add_item_invalid_price_zero(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 0.0)

    def test_add_item_invalid_price_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', -1.5)

    def test_add_item_invalid_quantity_low(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 1.5, 0)

    def test_add_item_invalid_type_price(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Apple', '1.5')

    def test_remove_item_success(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5)
        oc.remove_item('Apple')
        self.assertTrue(oc.is_empty())

    def test_remove_item_not_found(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('Banana')

    def test_is_empty_initially(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_is_empty_after_add(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        self.assertFalse(oc.is_empty())

    def test_clear_order(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.total_items(), 0)

    def test_total_items_sum(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0, 5)
        oc.add_item('Banana', 2.0, 3)
        self.assertEqual(oc.total_items(), 8)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_list_items(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0)
        oc.add_item('Banana', 2.0)
        items = oc.list_items()
        self.assertIn('Apple', items)
        self.assertIn('Banana', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    def test_get_subtotal_calculation(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 2.0, 3)
        oc.add_item('Banana', 1.0, 4)
        self.assertEqual(oc.get_subtotal(), 10.0)

    def test_get_subtotal_empty_error(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_logic(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100.0, 0.2), 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100.0, 0.0), 100.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        self.assertAlmostEqual(oc.apply_discount(100.0, 1.0), 0.0)

    def test_apply_discount_invalid_high(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_low(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)

    def test_apply_discount_invalid_subtotal_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-100.0, 0.1)

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(50.0), 10.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(150.0), 0.0)

    def test_calculate_tax_logic(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_invalid_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-50.0)

    def test_calculate_total_full_flow(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item1', 40.0, 1)
        oc.add_item('Item2', 10.0, 1)
        self.assertAlmostEqual(oc.calculate_total(discount=0.0), 72.0)

    def test_calculate_total_edge_case_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 100.0, 1)
        self.assertAlmostEqual(oc.calculate_total(), 110.0)

    def test_calculate_total_just_below_threshold(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 99.0, 1)
        self.assertAlmostEqual(oc.calculate_total(), 119.9)

    def test_calculate_total_empty_error(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()