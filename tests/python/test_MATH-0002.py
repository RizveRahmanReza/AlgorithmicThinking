"""
Unit Test Suite for Problem MATH-0002
Tests differential equivalence between MergeSort inversion counter and Quadratic Oracle.
"""

import unittest
from solutions.python.MATH_0002 import count_inversions, count_inversions_oracle


class TestMath0002(unittest.TestCase):
    def test_reverse_sorted(self):
        arr = [8, 4, 2, 1]
        self.assertEqual(count_inversions(arr), 6)
        self.assertEqual(count_inversions(arr), count_inversions_oracle(arr))

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(count_inversions(arr), 0)
        self.assertEqual(count_inversions(arr), count_inversions_oracle(arr))

    def test_arbitrary_permutation(self):
        arr = [2, 4, 1, 3, 5]
        self.assertEqual(count_inversions(arr), 3)
        self.assertEqual(count_inversions(arr), count_inversions_oracle(arr))

    def test_single_element_and_empty(self):
        self.assertEqual(count_inversions([]), 0)
        self.assertEqual(count_inversions([42]), 0)

    def test_duplicates(self):
        arr = [2, 2, 1, 1]
        # (2, 1), (2, 1), (2, 1), (2, 1) -> 4 inversions
        self.assertEqual(count_inversions(arr), 4)
        self.assertEqual(count_inversions(arr), count_inversions_oracle(arr))


if __name__ == "__main__":
    unittest.main()
