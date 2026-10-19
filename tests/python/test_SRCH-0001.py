"""
Unit Test Suite for Problem SRCH-0001
Tests differential equivalence between Binary Search on Answer and Linear Search Oracle.
"""

import unittest
from solutions.python.SRCH_0001 import ship_within_days, ship_within_days_oracle


class TestSrch0001(unittest.TestCase):
    def test_standard_cases(self):
        w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(ship_within_days(w1, 5), 15)
        self.assertEqual(ship_within_days(w1, 5), ship_within_days_oracle(w1, 5))

        w2 = [3, 2, 2, 4, 1, 4]
        self.assertEqual(ship_within_days(w2, 3), 6)
        self.assertEqual(ship_within_days(w2, 3), ship_within_days_oracle(w2, 3))

    def test_days_equal_length(self):
        w = [1, 2, 3, 1, 1]
        # With D = 5, answer should be max element = 3
        self.assertEqual(ship_within_days(w, 5), 3)

    def test_single_day(self):
        w = [10, 20, 30]
        # With D = 1, ship must take entire sum = 60
        self.assertEqual(ship_within_days(w, 1), 60)

    def test_invalid_parameters_raise(self):
        with self.assertRaises(ValueError):
            ship_within_days([], 5)
        with self.assertRaises(ValueError):
            ship_within_days([1, 2, 3], 0)


if __name__ == "__main__":
    unittest.main()
