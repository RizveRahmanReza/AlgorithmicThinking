"""
Unit Test Suite for Problem STACK-0002
Tests differential equivalence between Monotonic Stack and Circular Oracle.
"""

import unittest
from solutions.python.STACK_0002 import next_greater_elements, next_greater_oracle


class TestStack0002(unittest.TestCase):
    def test_circular_wrap(self):
        arr = [1, 2, 1]
        self.assertEqual(next_greater_elements(arr), [2, -1, 2])
        self.assertEqual(next_greater_elements(arr), next_greater_oracle(arr))

    def test_standard_array(self):
        arr = [1, 2, 3, 4, 3]
        self.assertEqual(next_greater_elements(arr), [2, 3, 4, -1, 4])
        self.assertEqual(next_greater_elements(arr), next_greater_oracle(arr))

    def test_all_identical(self):
        arr = [5, 5, 5]
        self.assertEqual(next_greater_elements(arr), [-1, -1, -1])
        self.assertEqual(next_greater_elements(arr), next_greater_oracle(arr))

    def test_strictly_descending(self):
        arr = [5, 4, 3, 2, 1]
        self.assertEqual(next_greater_elements(arr), [-1, 5, 5, 5, 5])
        self.assertEqual(next_greater_elements(arr), next_greater_oracle(arr))

    def test_single_element_and_empty(self):
        self.assertEqual(next_greater_elements([]), [])
        self.assertEqual(next_greater_elements([42]), [-1])


if __name__ == "__main__":
    unittest.main()
