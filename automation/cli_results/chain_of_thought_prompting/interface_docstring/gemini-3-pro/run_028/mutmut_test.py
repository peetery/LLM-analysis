import unittest
from order_calculator import OrderCalculator

class TestOrderCalculator(unittest.TestCase):

    def test_init_default(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())

    def test_init_custom_valid(self):
        oc = OrderCalculator(tax_rate=0.1, free_shipping_threshold=50.0, shipping_cost=5.0)
        self.assertTrue(oc.is_empty())

    def test_init_invalid_tax_rate_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=-0.1)

    def test_init_invalid_tax_rate_gt_one(self):
        with self.assertRaises(ValueError):
            OrderCalculator(tax_rate=1.1)

    def test_init_invalid_shipping_threshold_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(free_shipping_threshold=-1.0)

    def test_init_invalid_shipping_cost_negative(self):
        with self.assertRaises(ValueError):
            OrderCalculator(shipping_cost=-1.0)

    def test_init_invalid_types(self):
        with self.assertRaises(TypeError):
            OrderCalculator(tax_rate='0.23')

    def test_add_item_single_valid(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        self.assertEqual(oc.total_items(), 2)
        self.assertEqual(oc.get_subtotal(), 3.0)

    def test_add_item_duplicate_same_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 2)
        oc.add_item('Apple', 1.5, 3)
        self.assertEqual(oc.total_items(), 5)
        self.assertEqual(oc.get_subtotal(), 7.5)

    def test_add_item_multiple_distinct(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 1)
        oc.add_item('Banana', 2.0, 1)
        self.assertEqual(oc.total_items(), 2)
        self.assertEqual(oc.get_subtotal(), 3.5)

    def test_add_item_duplicate_name_diff_price(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.5, 1)
        with self.assertRaises(ValueError):
            oc.add_item('Apple', 2.0, 1)

    def test_add_item_empty_name(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('', 1.0, 1)

    def test_add_item_price_zero_or_negative(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('FreeItem', 0.0, 1)
        with self.assertRaises(ValueError):
            oc.add_item('NegativeItem', -5.0, 1)

    def test_add_item_quantity_less_than_one(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.add_item('Item', 1.0, 0)

    def test_add_item_name_not_string(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item(123, 1.0, 1)

    def test_add_item_invalid_types_price_qty(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.add_item('Item', '1.0', 1)
        with self.assertRaises(TypeError):
            oc.add_item('Item', 1.0, '1')

    def test_remove_item_existing(self):
        oc = OrderCalculator()
        oc.add_item('Apple', 1.0, 1)
        oc.remove_item('Apple')
        self.assertTrue(oc.is_empty())

    def test_remove_item_non_existent(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.remove_item('NonExistent')

    def test_remove_item_name_not_string(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.remove_item(123)

    def test_get_subtotal_normal(self):
        oc = OrderCalculator()
        oc.add_item('A', 10.0, 2)
        oc.add_item('B', 5.0, 1)
        self.assertEqual(oc.get_subtotal(), 25.0)

    def test_get_subtotal_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.get_subtotal()

    def test_apply_discount_normal(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 0.2)
        self.assertEqual(result, 80.0)

    def test_apply_discount_zero(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 0.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_full(self):
        oc = OrderCalculator()
        result = oc.apply_discount(100.0, 1.0)
        self.assertEqual(result, 0.0)

    def test_apply_discount_negative_subtotal(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(-10.0, 0.2)

    def test_apply_discount_invalid_range(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, -0.1)
        with self.assertRaises(ValueError):
            oc.apply_discount(100.0, 1.1)

    def test_apply_discount_invalid_types(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.apply_discount('100', 0.2)
        with self.assertRaises(TypeError):
            oc.apply_discount(100.0, '0.2')

    def test_calculate_shipping_below_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(99.9), 10.0)

    def test_calculate_shipping_above_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.1), 0.0)

    def test_calculate_shipping_at_threshold(self):
        oc = OrderCalculator(free_shipping_threshold=100.0, shipping_cost=10.0)
        self.assertEqual(oc.calculate_shipping(100.0), 0.0)

    def test_calculate_shipping_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_shipping('50')

    def test_calculate_tax_normal(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertAlmostEqual(oc.calculate_tax(100.0), 20.0)

    def test_calculate_tax_zero_amount(self):
        oc = OrderCalculator(tax_rate=0.2)
        self.assertEqual(oc.calculate_tax(0.0), 0.0)

    def test_calculate_tax_negative_amount(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_tax(-10.0)

    def test_calculate_tax_invalid_type(self):
        oc = OrderCalculator()
        with self.assertRaises(TypeError):
            oc.calculate_tax('100')

    def test_calculate_total_full_flow_shipping_applied(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 50.0, 1)
        self.assertAlmostEqual(oc.calculate_total(discount=0.1), 66.0)

    def test_calculate_total_full_flow_free_shipping(self):
        oc = OrderCalculator(tax_rate=0.2, free_shipping_threshold=100.0, shipping_cost=10.0)
        oc.add_item('Item', 200.0, 1)
        self.assertAlmostEqual(oc.calculate_total(discount=0.1), 216.0)

    def test_calculate_total_empty_order(self):
        oc = OrderCalculator()
        with self.assertRaises(ValueError):
            oc.calculate_total()

    def test_calculate_total_invalid_discount(self):
        oc = OrderCalculator()
        oc.add_item('Item', 10.0, 1)
        with self.assertRaises(ValueError):
            oc.calculate_total(discount=-0.1)

    def test_total_items_sum(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0, 2)
        oc.add_item('B', 1.0, 3)
        self.assertEqual(oc.total_items(), 5)

    def test_total_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.total_items(), 0)

    def test_clear_order_normal(self):
        oc = OrderCalculator()
        oc.add_item('Item', 1.0, 1)
        oc.clear_order()
        self.assertTrue(oc.is_empty())
        self.assertEqual(oc.total_items(), 0)

    def test_list_items_populated(self):
        oc = OrderCalculator()
        oc.add_item('A', 1.0, 1)
        oc.add_item('B', 1.0, 1)
        items = oc.list_items()
        self.assertIn('A', items)
        self.assertIn('B', items)
        self.assertEqual(len(items), 2)

    def test_list_items_empty(self):
        oc = OrderCalculator()
        self.assertEqual(oc.list_items(), [])

    def test_is_empty_normal(self):
        oc = OrderCalculator()
        self.assertTrue(oc.is_empty())
        oc.add_item('Item', 1.0, 1)
        self.assertFalse(oc.is_empty())