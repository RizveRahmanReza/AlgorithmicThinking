/**
 * LIST-0001: Floyd's Cycle Detection and In-Place List Inversion
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(1) Auxiliary Space
 * Companion: Contains Cycle Entry Locator and In-Place Inverter
 */

#include <iostream>
#include <memory>
#include <optional>
#include <cassert>

struct ListNode {
    int64_t val;
    ListNode* next;

    explicit ListNode(int64_t v) noexcept : val(v), next(nullptr) {}
};

struct ListAuditResult {
    bool has_cycle;
    ListNode* cycle_entry;
    ListNode* new_head_if_reversed;
};

namespace alg {

/**
 * Detects cycle and locates cycle entry using Floyd's Tortoise and Hare algorithm.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 */
ListNode* find_cycle_entry(ListNode* head) noexcept {
    if (!head || !head->next) {
        return nullptr;
    }

    ListNode* slow = head;
    ListNode* fast = head;

    // Phase 1: Detect Collision
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            // Collision detected! Phase 2: Find Entry
            ListNode* ptr1 = head;
            ListNode* ptr2 = slow;

            while (ptr1 != ptr2) {
                ptr1 = ptr1->next;
                ptr2 = ptr2->next;
            }
            return ptr1; // Exact Cycle Entry Node
        }
    }

    return nullptr; // Acyclic
}

/**
 * Inverts a singly linked list in place using the three-pointer invariant.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 */
ListNode* reverse_list_in_place(ListNode* head) noexcept {
    ListNode* prev = nullptr;
    ListNode* curr = head;

    while (curr != nullptr) {
        ListNode* next_temp = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next_temp;
    }

    return prev;
}

/**
 * Complete Audit: detects cycle; if acyclic, reverses list.
 */
ListAuditResult audit_and_process_list(ListNode* head) noexcept {
    ListNode* cycle_node = find_cycle_entry(head);
    if (cycle_node != nullptr) {
        return ListAuditResult{
            .has_cycle = true,
            .cycle_entry = cycle_node,
            .new_head_if_reversed = nullptr
        };
    }

    ListNode* reversed_head = reverse_list_in_place(head);
    return ListAuditResult{
        .has_cycle = false,
        .cycle_entry = nullptr,
        .new_head_if_reversed = reversed_head
    };
}

} // namespace alg

int main() {
    // Test 1: Cyclic list: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> (back to 3)
    ListNode n1(1), n2(2), n3(3), n4(4), n5(5), n6(6);
    n1.next = &n2;
    n2.next = &n3;
    n3.next = &n4;
    n4.next = &n5;
    n5.next = &n6;
    n6.next = &n3; // Cycle back to 3

    auto res1 = alg::audit_and_process_list(&n1);
    assert(res1.has_cycle == true);
    assert(res1.cycle_entry == &n3);

    // Test 2: Acyclic list: 10 -> 20 -> 30 -> nullptr
    ListNode a1(10), a2(20), a3(30);
    a1.next = &a2;
    a2.next = &a3;

    auto res2 = alg::audit_and_process_list(&a1);
    assert(res2.has_cycle == false);
    assert(res2.cycle_entry == nullptr);
    assert(res2.new_head_if_reversed == &a3);
    assert(a3.next == &a2);
    assert(a2.next == &a1);
    assert(a1.next == nullptr);

    std::cout << "All C++20 assertions for LIST-0001 passed successfully." << std::endl;
    return 0;
}
