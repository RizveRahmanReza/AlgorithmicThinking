"""
Unit Test Suite for Problem STACK-0001
Tests differential equivalence between LIFO stack parser and Quadratic Replacement Oracle.
"""

import unittest
from solutions.python.STACK_0001 import is_valid_parentheses, is_valid_parentheses_oracle


class TestStack0001(unittest.TestCase):
    def test_valid_patterns(self):
        cases = [
            "()",
            "()[]{}",
            "{[]}",
            "((((()))))",
            "{[()()]}",
            ""
        ]
        for s in cases:
            self.assertTrue(is_valid_parentheses(s))
            self.assertTrue(is_valid_parentheses_oracle(s))

    def test_invalid_interleaved(self):
        cases = [
            "(]",
            "([)]",
            "{[(])}",
            ")(",
            "((((",
            "))))"
        ]
        for s in cases:
            self.assertFalse(is_valid_parentheses(s))
            self.assertFalse(is_valid_parentheses_oracle(s))

    def test_odd_length_fast_reject(self):
        self.assertFalse(is_valid_parentheses("("))
        self.assertFalse(is_valid_parentheses(")"))
        self.assertFalse(is_valid_parentheses("((("))
        self.assertFalse(is_valid_parentheses("()("))


if __name__ == "__main__":
    unittest.main()
