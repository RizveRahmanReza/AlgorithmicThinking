"""
Unit Test Suite for Problem STR-0001
Tests differential equivalence between Dual-Pointer scanner and Allocation Oracle.
"""

import unittest
from solutions.python.STR_0001 import is_valid_palindrome, is_valid_palindrome_oracle


class TestStr0001(unittest.TestCase):
    def test_standard_valid_palindromes(self):
        cases = [
            "A man, a plan, a canal: Panama",
            "Was it a car or a cat I saw?",
            "No 'x' in Nixon",
            "Madam, in Eden, I'm Adam"
        ]
        for s in cases:
            self.assertTrue(is_valid_palindrome(s))
            self.assertTrue(is_valid_palindrome_oracle(s))

    def test_invalid_palindromes(self):
        cases = [
            "race a car",
            "hello world",
            "0P",
            "ab2a"
        ]
        for s in cases:
            self.assertFalse(is_valid_palindrome(s))
            self.assertFalse(is_valid_palindrome_oracle(s))

    def test_boundary_empty_and_whitespace(self):
        cases = ["", " ", "   ", ", , ; -", "!!!"]
        for s in cases:
            self.assertTrue(is_valid_palindrome(s))
            self.assertTrue(is_valid_palindrome_oracle(s))

    def test_single_characters(self):
        self.assertTrue(is_valid_palindrome("a"))
        self.assertTrue(is_valid_palindrome("Z"))
        self.assertTrue(is_valid_palindrome("9"))


if __name__ == "__main__":
    unittest.main()
