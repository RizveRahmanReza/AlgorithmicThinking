"""
Unit Test Suite for Problem HASH-0001
Tests open-addressing hash table collision, update, tombstone recycling, and rehash integrity.
"""

import unittest
from solutions.python.HASH_0001 import FlatHashMap


class TestHash0001(unittest.TestCase):
    def test_basic_crud(self):
        m = FlatHashMap(8)
        self.assertTrue(m.insert(10, 100))
        self.assertEqual(m.get(10), 100)
        self.assertFalse(m.insert(10, 150))  # Update
        self.assertEqual(m.get(10), 150)
        self.assertTrue(m.remove(10))
        self.assertIsNone(m.get(10))
        self.assertFalse(m.remove(10))

    def test_collision_probing_past_tombstones(self):
        # Force collisions on capacity 4
        m = FlatHashMap(4)
        m.insert(1, 10)
        m.insert(5, 50)
        m.insert(9, 90)

        # Remove middle element
        self.assertTrue(m.remove(5))
        self.assertIsNone(m.get(5))

        # Probe for 9 must skip tombstone at 5 and succeed
        self.assertEqual(m.get(9), 90)
        self.assertEqual(m.get(1), 10)

    def test_large_scale_rehash(self):
        m = FlatHashMap(8)
        n = 1000
        for i in range(n):
            self.assertTrue(m.insert(i, i * 7))

        self.assertEqual(m.size, n)
        for i in range(n):
            self.assertEqual(m.get(i), i * 7)


if __name__ == "__main__":
    unittest.main()
