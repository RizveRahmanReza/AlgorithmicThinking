"""
Unit Test Suite for Problem LIST-0001
Tests cycle detection, cycle entry location, and in-place reversal.
"""

import unittest
from solutions.python.LIST_0001 import (
    ListNode,
    find_cycle_entry,
    reverse_list_in_place,
    audit_and_process_list,
    ListAuditResult
)


class TestList0001(unittest.TestCase):
    def test_cyclic_list(self):
        nodes = [ListNode(i) for i in range(1, 7)]
        for i in range(5):
            nodes[i].next = nodes[i + 1]
        nodes[5].next = nodes[2]  # Cycle back to node 3

        res = audit_and_process_list(nodes[0])
        self.assertTrue(res.has_cycle)
        self.assertIs(res.cycle_entry, nodes[2])
        self.assertIsNone(res.new_head_if_reversed)

    def test_acyclic_reversal(self):
        a1, a2, a3 = ListNode(1), ListNode(2), ListNode(3)
        a1.next, a2.next = a2, a3

        res = audit_and_process_list(a1)
        self.assertFalse(res.has_cycle)
        self.assertIsNone(res.cycle_entry)
        self.assertIs(res.new_head_if_reversed, a3)
        self.assertIs(a3.next, a2)
        self.assertIs(a2.next, a1)
        self.assertIsNone(a1.next)

    def test_single_node_self_cycle(self):
        node = ListNode(42)
        node.next = node

        entry = find_cycle_entry(node)
        self.assertIs(entry, node)

    def test_empty_list(self):
        res = audit_and_process_list(None)
        self.assertFalse(res.has_cycle)
        self.assertIsNone(res.new_head_if_reversed)


if __name__ == "__main__":
    unittest.main()
