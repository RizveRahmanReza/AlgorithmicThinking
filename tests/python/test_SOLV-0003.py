"""
Unit Test Suite for Problem SOLV-0003
Tests differential equivalence between Kadane and Quadratic Oracle.
"""

import unittest
from solutions.python.SOLV_0003 import find_max_subarray_kadane, find_max_subarray_oracle, SubarrayResult


class TestSolv0003(unittest.TestCase):
    def test_mixed_array(self):
        arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
        res_k = find_max_subarray_kadane(arr)
        res_o = find_max_subarray_oracle(arr)
        self.assertEqual(res_k, res_o)
        self.assertEqual(res_k, SubarrayResult(6, 3, 6))

    def test_all_negative(self):
        arr = [-5, -2, -9, -3]
        res_k = find_max_subarray_kadane(arr)
        res_o = find_max_subarray_oracle(arr)
        self.assertEqual(res_k, res_o)
        self.assertEqual(res_k, SubarrayResult(-2, 1, 1))

    def test_all_positive(self):
        arr = [10, 20, 30]
        res_k = find_max_subarray_kadane(arr)
        res_o = find_max_subarray_oracle(arr)
        self.assertEqual(res_k, res_o)
        self.assertEqual(res_k, SubarrayResult(60, 0, 2))

    def test_single_element(self):
        arr = [-99]
        res_k = find_max_subarray_kadane(arr)
        res_o = find_max_subarray_oracle(arr)
        self.assertEqual(res_k, res_o)
        self.assertEqual(res_k, SubarrayResult(-99, 0, 0))

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            find_max_subarray_kadane([])
        with self.assertRaises(ValueError):
            find_max_subarray_oracle([])


if __name__ == "__main__":
    unittest.main()
