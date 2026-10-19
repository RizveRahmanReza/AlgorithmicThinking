"""
Unit Test Suite for Problem SOLV-0001
Tests normal, boundary, edge, and adversarial cases.
"""

import unittest
from solutions.python.SOLV_0001 import find_maximum_anomaly_subsegment, SubarrayResult


class TestSolv0001(unittest.TestCase):
    def test_standard_case(self):
        arr = [2, -4, 3, -1, 4, -6, 2]
        res = find_maximum_anomaly_subsegment(arr)
        self.assertEqual(res, SubarrayResult(6, 2, 4))

    def test_all_negatives(self):
        arr = [-8, -3, -9, -4]
        res = find_maximum_anomaly_subsegment(arr)
        self.assertEqual(res, SubarrayResult(-3, 1, 1))

    def test_all_positives(self):
        arr = [1, 2, 3, 4]
        res = find_maximum_anomaly_subsegment(arr)
        self.assertEqual(res, SubarrayResult(10, 0, 3))

    def test_single_element(self):
        arr = [42]
        res = find_maximum_anomaly_subsegment(arr)
        self.assertEqual(res, SubarrayResult(42, 0, 0))

    def test_empty_sequence_raises(self):
        with self.assertRaises(ValueError):
            find_maximum_anomaly_subsegment([])

    def test_tie_breaking_shortest_length(self):
        # 5 alone is length 1; 5, -6, 5, -6, 5 could sum to various values but peak single 5 is shortest
        arr = [5, -6, 5, -6, 5]
        res = find_maximum_anomaly_subsegment(arr)
        self.assertEqual(res, SubarrayResult(5, 0, 0))


if __name__ == "__main__":
    unittest.main()
