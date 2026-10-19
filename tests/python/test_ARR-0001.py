"""
Unit Test Suite for Problem ARR-0001
Tests differential equivalence between Three-Step Reversal and Quadratic Oracle.
"""

import unittest
from solutions.python.ARR_0001 import rotate_right_in_place, rotate_right_oracle


class TestArr0001(unittest.TestCase):
    def test_standard_rotation(self):
        arr = [1, 2, 3, 4, 5, 6, 7]
        oracle = list(arr)
        rotate_right_in_place(arr, 3)
        rotate_right_oracle(oracle, 3)
        self.assertEqual(arr, [5, 6, 7, 1, 2, 3, 4])
        self.assertEqual(arr, oracle)

    def test_rotation_greater_than_length(self):
        arr = [10, 20, 30, 40]
        rotate_right_in_place(arr, 10)  # 10 % 4 = 2
        self.assertEqual(arr, [30, 40, 10, 20])

    def test_full_cycle_rotation(self):
        arr = [1, 2, 3]
        rotate_right_in_place(arr, 3)
        self.assertEqual(arr, [1, 2, 3])

    def test_single_element_and_empty(self):
        empty = []
        rotate_right_in_place(empty, 5)
        self.assertEqual(empty, [])

        single = [99]
        rotate_right_in_place(single, 7)
        self.assertEqual(single, [99])


if __name__ == "__main__":
    unittest.main()
