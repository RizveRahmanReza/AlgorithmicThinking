"""
Unit Test Suite for Problem MATH-0001
Tests differential equivalence between Two-Pointer and Quadratic Oracle.
"""

import unittest
from solutions.python.MATH_0001 import find_sorted_two_sum, find_sorted_two_sum_oracle, PairIndices


class TestMath0001(unittest.TestCase):
    def test_standard_hit(self):
        arr = [1, 3, 5, 8, 12, 15, 19]
        res_tp = find_sorted_two_sum(arr, 17)
        res_or = find_sorted_two_sum_oracle(arr, 17)
        self.assertEqual(res_tp, res_or)
        self.assertEqual(res_tp, PairIndices(2, 4))

    def test_boundary_elements(self):
        arr = [2, 7, 11, 15]
        res_tp = find_sorted_two_sum(arr, 17)
        res_or = find_sorted_two_sum_oracle(arr, 17)
        self.assertEqual(res_tp, res_or)
        self.assertEqual(res_tp, PairIndices(0, 3))

    def test_target_not_found(self):
        arr = [1, 2, 3, 4]
        self.assertIsNone(find_sorted_two_sum(arr, 10))
        self.assertIsNone(find_sorted_two_sum_oracle(arr, 10))

    def test_duplicate_values(self):
        arr = [3, 3]
        res_tp = find_sorted_two_sum(arr, 6)
        res_or = find_sorted_two_sum_oracle(arr, 6)
        self.assertEqual(res_tp, res_or)
        self.assertEqual(res_tp, PairIndices(0, 1))

    def test_small_lengths(self):
        self.assertIsNone(find_sorted_two_sum([], 5))
        self.assertIsNone(find_sorted_two_sum([5], 5))


if __name__ == "__main__":
    unittest.main()
