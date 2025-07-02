import unittest
            calc.calculate_tax(-1)

    def test_calculate_tax_invalid_type(self):
        calc = OrderCalculator()
        with self.assertRaises(TypeError):
            calc.calculate_tax("100")

    def test_calculate_total_with_shipping_and_tax(self):
        calc = OrderCalculator()
        calc.add_item("A", 50, 1)
        calc.add_item("B", 20, 2)
        total = calc.calculate_total(0.1)
        expected_subtotal = 50 + 20 * 2
        discounted = expected_subtotal * 0.9
        shipping = 10
        tax = (discounted + shipping) * 0.23
        expected_total = discounted + shipping + tax
        self.assertAlmostEqual(total, expected_total)

    def test_calculate_total_free_shipping(self):
        calc = OrderCalculator()
        calc.add_item("A", 120, 1)
        total = calc.calculate_total()
        discounted = 120
        shipping = 0
        tax = (discounted + shipping) * 0.23
        self.assertAlmostEqual(total, discounted + shipping + tax)

    def test_calculate_total_invalid_discount_type(self):
        calc = OrderCalculator()
        calc.add_item("A", 10, 1)
        with self.assertRaises(TypeError):
            calc.calculate_total("0.1")

    def test_calculate_total_empty_order_value_error(self):
        calc = OrderCalculator()
        with self.assertRaises(ValueError):
            calc.calculate_total()

    def test_total_items(self):
        calc = OrderCalculator()
        calc.add_item("A", 1, 2)
        calc.add_item("B", 1, 3)
        self.assertEqual(calc.total_items(), 5)

    def test_clear_order_resets(self):
        calc = OrderCalculator()
        calc.add_item("A", 1, 1)
        calc.clear_order()
        self.assertTrue(calc.is_empty())

    def test_list_items_unique(self):
        calc = OrderCalculator()
        calc.add_item("A", 1, 1)
        calc.add_item("A", 1, 2)
        calc.add_item("B", 2, 1)
        self.assertEqual(set(calc.list_items()), {"A", "B"})

    def test_is_empty_true(self):
        calc = OrderCalculator()
        self.assertTrue(calc.is_empty())

    def test_is_empty_false(self):
        calc = OrderCalculator()
        calc.add_item("A", 1, 1)
        self.assertFalse(calc.is_empty())


if __name__ == "__main__":
    unittest.main()