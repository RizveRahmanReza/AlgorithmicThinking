"""
LIST-0001: Floyd's Cycle Detection and In-Place List Inversion
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Floyd's Cycle Locator and In-Place Three-Pointer Reversal.
"""

from typing import Optional, NamedTuple


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node


class ListAuditResult(NamedTuple):
    has_cycle: bool
    cycle_entry: Optional[ListNode]
    new_head_if_reversed: Optional[ListNode]


def find_cycle_entry(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Detects cycle and locates cycle entry using Floyd's Tortoise and Hare.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    if not head or not head.next:
        return None

    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head

    # Phase 1: Detect Collision
    while fast and fast.next:
        slow = slow.next  # type: ignore
        fast = fast.next.next

        if slow is fast:
            # Phase 2: Find Cycle Entry
            ptr1 = head
            ptr2 = slow
            while ptr1 is not ptr2:
                ptr1 = ptr1.next  # type: ignore
                ptr2 = ptr2.next  # type: ignore
            return ptr1

    return None


def reverse_list_in_place(head: Optional[ListNode]) -> Optional[ListNode]:
    """Inverts singly linked list in place using three-pointer invariant."""
    prev: Optional[ListNode] = None
    curr: Optional[ListNode] = head

    while curr is not None:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp

    return prev


def audit_and_process_list(head: Optional[ListNode]) -> ListAuditResult:
    """Audits linked list for cycles; if acyclic, inverts pointers in place."""
    cycle_entry = find_cycle_entry(head)
    if cycle_entry is not None:
        return ListAuditResult(
            has_cycle=True,
            cycle_entry=cycle_entry,
            new_head_if_reversed=None
        )

    reversed_head = reverse_list_in_place(head)
    return ListAuditResult(
        has_cycle=False,
        cycle_entry=None,
        new_head_if_reversed=reversed_head
    )


if __name__ == "__main__":
    # Test 1: Cyclic list
    nodes = [ListNode(i) for i in range(1, 7)]
    for i in range(5):
        nodes[i].next = nodes[i + 1]
    nodes[5].next = nodes[2]  # Cycle back to node 3 (val 3)

    r1 = audit_and_process_list(nodes[0])
    assert r1.has_cycle is True
    assert r1.cycle_entry is nodes[2]

    # Test 2: Acyclic list
    a1, a2, a3 = ListNode(10), ListNode(20), ListNode(30)
    a1.next, a2.next = a2, a3
    r2 = audit_and_process_list(a1)
    assert r2.has_cycle is False
    assert r2.new_head_if_reversed is a3
    assert a3.next is a2 and a2.next is a1 and a1.next is None

    print("All Python 3 self-tests for LIST-0001 passed successfully.")
