# CHAPTER 9: POINTER-BASED STRUCTURES AND LINKED LISTS

> *"Contiguous arrays conquer the cache; linked lists conquer dynamic re-linking. To master linked structures, one must master pointer invariants and prevent memory leaks."*

---

## 9.1 Memory Layout: Contiguity vs. Heap-Dispersed Pointer Storage

Throughout Chapters 7 and 8, we emphasized the hardware supremacy of contiguous memory. Why, then, does computer science study **Linked Lists**?

A linked list trades away cache locality and $\mathcal{O}(1)$ random access in exchange for two unique structural capabilities:
1. **True $\mathcal{O}(1)$ Non-Amortized Splices and Removals**: Once a target pointer is located, inserting or removing an element requires updating exactly two pointers ($8$ or $16$ bytes), with zero elements shifted.
2. **Zero Contiguous Reallocation Overhead**: A linked list never reallocates a backing buffer. It allocates memory node-by-node on demand.

```
Contiguous Vector Memory Layout (Cache-Friendly):
[ Node 0 | Node 1 | Node 2 | Node 3 | Node 4 | Node 5 ] -> Contiguous 64-byte lines

Linked List Heap Memory Layout (Cache-Hostile Pointer Chasing):
Address 0x1040: [ Val: 10 | Next: 0x8F20 ] 
                                  | (Cache Miss!)
Address 0x8F20: [ Val: 20 | Next: 0x3100 ]
                                  | (Cache Miss!)
Address 0x3100: [ Val: 30 | Next: nullptr ]
```

### The Architectural Memory Penalty
On a 64-bit architecture:
- A `std::vector<int32_t>` stores each integer in exactly **4 bytes** of memory.
- A singly linked list node storing `int32_t` requires:
  - 4 bytes (data) + 4 bytes (compiler structure padding) + 8 bytes (`next` pointer) + 16 bytes (heap allocator chunk header metadata) = **32 bytes per integer!**
- This represents an **$800\%$ memory dilation**, accompanied by complete loss of hardware prefetcher tracking.

Therefore, senior engineers do not use linked lists for general sequence storage; they use them for specialized lock-free queues, kernel scheduler run-queues, memory arena free-lists, and LRU eviction chains.

---

## 9.2 The Foundational Linked List Archetypes

```
+---------------------------------------------------------------------------------+
| Archetype           | Pointers per Node | Key Capabilities                      |
+---------------------------------------------------------------------------------+
| Singly Linked List  | 1 (next)          | Forward traversal; minimal overhead   |
| Doubly Linked List  | 2 (prev, next)    | Bidirectional traversal; O(1) removal |
| Circular List       | 1 or 2 (tail->head)| Round-robin scheduling; token rings  |
| Sentinel-Head List  | Dummy head node   | Eliminates edge-case null branch checks|
+---------------------------------------------------------------------------------+
```

### The Sentinel (Dummy Head) Invariant
In naive linked list implementations, inserting or deleting at the head requires special conditional checks:
```cpp
if (head == nullptr) { head = new_node; }
else if (target == head) { head = head->next; }
```
By allocating a permanent, empty **Sentinel Node** at the front of the list (`dummy.next = head`), every valid node—including the first logical element—always has a preceding predecessor. This eliminates null-pointer branch mispredictions and eliminates bug-prone conditional branches.

---

## 9.3 In-Place Reversal: The Three-Pointer State Invariant

Reversing a singly linked list in place without allocating new heap nodes is the canonical test of pointer mastery.

To reverse a list in $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ space, we maintain three adjacent pointers across each state transition:
- `prev`: The head of the already reversed prefix (initially `nullptr`).
- `curr`: The node currently being inverted (initially `head`).
- `next_temp`: A temporary anchor preserving the unvisited suffix (`curr->next`).

```
Initial State:
prev(null)    curr(1) -> next_temp(2) -> (3) -> null

Step 1: Save next node:
next_temp = curr->next;

Step 2: Invert pointer:
curr->next = prev;

Step 3: Advance state:
prev = curr;
curr = next_temp;

Result after Step 1:
(1) -> null   curr(2) -> (3) -> null
 ^
prev
```

At loop termination (`curr == nullptr`), `prev` points to the new head of the completely reversed list.

---

## 9.4 Worked Problem: LIST-0001 — Floyd's Cycle Detection and In-Place List Inversion

We now apply the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify: **Detecting Cyclic Corruption in Linked Memory and Reconstructing Structural Traversal**.

---

### Step 1: Real-World Motivation
In operating system kernels (e.g., Linux slab allocator) and embedded microcontrollers, memory blocks and driver event queues are linked via intrusive pointers. If a race condition or memory corruption bug causes a node to point back to an earlier node in the list, any subsequent kernel traversal enters an infinite loop, freezing the CPU core and causing a system watchdog panic.

The kernel memory auditor must verify whether a linked list contains a cycle using strictly $\mathcal{O}(1)$ auxiliary memory (without allocating hash tables or marking visited bitsets, which might trigger memory allocation inside an interrupt context). Furthermore, if acyclic, the auditor must invert the link pointers in place to verify link integrity.

### Step 2: Problem Identification
Given the head of a singly linked list:
1. Determine whether the list contains a cycle.
2. If a cycle exists, locate the exact node where the cycle begins.
3. If acyclic, reverse the list in-place and return the new head pointer.

### Step 3: Formal Problem Statement
Let a singly linked list be a finite directed graph where each node $u$ has an out-degree of at most 1:
$$\text{Next}(u) \in V \cup \{\text{null}\}$$
- A **cycle** exists if and only if there exists a node $v$ reachable from $\text{head}$ such that following $\text{Next}$ links from $v$ eventually returns to $v$.
- If a cycle exists, return `(has_cycle = true, cycle_entry_node = v)`.
- If no cycle exists, reverse all directed edges in place ($u \to v$ becomes $v \to u$) and return `(has_cycle = false, new_head)`.

#### Constraints:
- Number of nodes: $0 \le n \le 10^6$
- Node values: $-10^9 \le \text{val} \le 10^9$
- Time budget: Strictly $\mathcal{O}(n)$
- Auxiliary memory budget: Strictly $\mathcal{O}(1)$ (Zero dynamic allocations; no hash sets; no node modifications during cycle detection).

### Step 4: Thinking Before Coding
1. **Can we use a Hash Set of visited pointers?**
   No. Storing $10^6$ 64-bit pointers in an `std::unordered_set` requires $32 \text{ MB}$ to $64 \text{ MB}$ of dynamic heap memory, violating our $\mathcal{O}(1)$ auxiliary space constraint and failing embedded/kernel safety rules.
2. **Can we modify the node struct to add a `visited` boolean flag?**
   No. Modifying node memory layout alters cache alignment and is prohibited on read-only or kernel-intrusive data.
3. **The Two-Pointer Phase (Floyd's Tortoise and Hare Algorithm)**:
   If two runners race on a circular track, with one running at speed 1 (slow) and the other running at speed 2 (fast), the fast runner is guaranteed to lap and collide with the slow runner if and only if a closed loop exists!

### Step 5: First-Principles Reasoning (Relative Velocity Invariant)
Why must the fast and slow pointers meet inside a cycle?
Let the cycle have length $C$.
Once both pointers have entered the cycle:
- At each step, the slow pointer advances by 1 position.
- At each step, the fast pointer advances by 2 positions.
- The relative distance between fast and slow decreases by:
  $$\Delta = (2 - 1) = 1 \text{ position per step!}$$
Because the distance decreases by exactly 1 at each tick, **the fast runner cannot leap over or bypass the slow runner!** The distance must decrement to 0, guaranteeing a collision within at most $C$ steps after both pointers enter the cycle.

### Step 6: Brute-Force Implementation (The Hash Set Oracle)

```python
# Reference Baseline: Hash Set Visited Tracker (O(N) Time, O(N) Space)
def detect_cycle_oracle(head):
    visited = set()
    curr = head
    while curr is not None:
        if id(curr) in visited:
            return True, curr
        visited.add(id(curr))
        curr = curr.next
    return False, None
```

### Step 7: Bottleneck Analysis
- The baseline oracle requires $\Theta(n)$ auxiliary space to store pointer hashes.
- For $n = 10^6$, hash set operations incur millions of pointer hash calculations and memory allocator overheads.
- Floyd's two-pointer algorithm uses exactly two pointer variables (`slow`, `fast`), reducing auxiliary space from $\Theta(n)$ to strictly $\mathcal{O}(1)$.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Auxiliary Space | Mutates Node Memory? | Viable for Kernel / OOM? |
| :--- | :--- | :--- | :--- | :--- |
| **Hash Set Visited Registry** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | No | No (OOM on constrained memory) |
| **Node Visited Flag / Tagging**| $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Yes** (Mutates structs)| No (Violates read-only invariants) |
| **Pointer Reversal Marking** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Yes** (Destructive) | No (Crashes concurrent readers) |
| **Floyd's Tortoise and Hare** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **No** (Pure read-only)| **Optimal** |

### Step 9: Derivation of the Cycle Entry Detection Theorem
Once `slow` and `fast` collide, how do we find the **exact entry node** of the cycle?

Let:
- $L_1$: Distance from `head` to the cycle entry node.
- $L_2$: Distance from the cycle entry node to the collision point.
- $C$: Total circumference (length) of the cycle.

```
head -----( L1 )-----> [Cycle Entry] -----( L2 )-----> [Collision Point]
                             ^                                |
                             |------------( C - L2 )----------|
```

When they collide:
- Total distance traveled by `slow`: $D_{\text{slow}} = L_1 + L_2$.
- Total distance traveled by `fast`: $D_{\text{fast}} = L_1 + L_2 + k \cdot C$ (where $k \ge 1$ is the number of full cycle loops completed by fast).

Because `fast` travels at exactly twice the speed of `slow`:
$$D_{\text{fast}} = 2 \cdot D_{\text{slow}}$$
$$L_1 + L_2 + k \cdot C = 2(L_1 + L_2) = 2 L_1 + 2 L_2$$
Subtracting $(L_1 + L_2)$ from both sides:
$$L_1 = k \cdot C - L_2 = (k - 1)C + (C - L_2)$$

**The Winning Mathematical Insight**:
The distance from `head` to the cycle entry ($L_1$) is **strictly equal** to the distance from the collision point to the cycle entry traveling along the cycle ($(C - L_2)$ modulo $C$)!

Therefore:
1. Leave `slow` at the collision point.
2. Reset `fast` (or a new pointer `entry_ptr`) back to `head`.
3. Advance both pointers at the **same speed of 1 step per tick**.
4. They are mathematically guaranteed to meet at the exact **Cycle Entry Node** after traversing $L_1$ steps!

### Step 10: Step-by-Step Dry Run

Consider a list with 6 nodes: $1 \to 2 \to 3 \to 4 \to 5 \to 6 \to 3$ (Cycle entry is node 3; $L_1 = 2$, $C = 4$).

1. **Phase 1: Collision Detection**:
   - Step 0: `slow` at 1, `fast` at 1.
   - Step 1: `slow` at 2, `fast` at 3.
   - Step 2: `slow` at 3, `fast` at 5.
   - Step 3: `slow` at 4, `fast` at 3.
   - Step 4: `slow` at 5, `fast` at 5. **Collision at node 5!** ($L_2 = 2$).
2. **Phase 2: Cycle Entry Discovery**:
   - Reset `ptr1` to `head` (node 1); leave `ptr2` at collision point (node 5).
   - Tick 1: `ptr1` advances to 2; `ptr2` advances to 6.
   - Tick 2: `ptr1` advances to 3; `ptr2` advances to 3. **Pointers meet at node 3!**
   - **Correct Cycle Entry Identified**: Node 3.

### Step 11: Full C++20 Implementation

```cpp
// solutions/cpp/LIST-0001.cpp
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
            return ptr1; // Exact Cycle Entry
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
```

### Step 12: Full Python Implementation

```python
# solutions/python/LIST-0001.py
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
```

### Step 13: Complexity Analysis
- **Time Complexity**: $\Theta(N)$
  - Phase 1 (Collision): `slow` travels at most $L_1 + C$ steps before collision; `fast` travels $2(L_1 + C)$. Total steps $\le 3N \implies \mathcal{O}(N)$.
  - Phase 2 (Entry Identification): Both pointers advance exactly $L_1 \le N$ steps.
  - Reversal Pass: Each pointer in an acyclic list is visited and inverted exactly once ($\Theta(N)$).
- **Space Complexity**: $\Theta(1)$ auxiliary space. Only scalar pointers (`slow`, `fast`, `prev`, `curr`, `next_temp`) are maintained. Zero memory allocation.

### Step 14: Edge Cases and Failure Modes
- Empty list (`nullptr` / `None`): Returns `has_cycle = false, reversed = nullptr`.
- Single-node acyclic (`1 -> nullptr`): Returns `has_cycle = false, reversed = 1`.
- Single-node self-loop (`1 -> 1`): `fast` and `slow` collide immediately on node 1; cycle entry is node 1.
- Two-node cycle (`1 -> 2 -> 1`): Handled cleanly without null dereference.

### Step 15: Real-World Engineering Application
- Linux Kernel Slab/Slub Allocator integrity auditing.
- Garbage collection tracing: Cycle detection in reference-counting runtimes (CPython GC cycle breaker).
- Distributed deadlock detection in transaction wait-for graphs.

### Step 16: Further Optimization & Systems Insights
- **Cache Pre-fetching in Linked Lists**: In systems software, jumping to `curr->next` can be accelerated using compiler intrinsic prefetch instructions (`__builtin_prefetch(curr->next)`) to initiate DRAM line fetches before dereferencing.

### Step 17: Related Patterns
- **Middle of the Linked List**: When `fast` reaches the end, `slow` is located at the exact mathematical midpoint ($\lfloor N/2 \rfloor$).
- **Palindrome Linked List**: Combining midpoint finding, second-half reversal, and simultaneous dual-pointer comparison.

### Step 18: Reader Challenges
1. **Challenge 9.1 (Cycle Length Computation)**: Once a cycle is detected, derive an $\mathcal{O}(1)$ space algorithm to compute the exact cycle circumference $C$.
2. **Challenge 9.2 (Reverse Nodes in K-Group)**: Reverse nodes in a linked list $K$ at a time, leaving remaining sub-segments unchanged if length $< K$. Prove the multi-sentinel invariant.

---

## 9.5 Synthesis of Part III: Arrays, Strings, and Linked Lists

With the completion of Chapter 9, we conclude **Part III: Arrays, Strings, and Linked Lists**. 

Across Chapters 7, 8, and 9, we have established the foundational linear memory paradigms:
1. **Contiguous Flat Vectors (Chapter 7)**: Harnessing cache lines, spatial locality, and in-place reversal transforms.
2. **Encoded Character Streams (Chapter 8)**: Navigating UTF-8 variable-length encodings, grapheme clusters, and zero-allocation read/write filter invariants.
3. **Dispersed Pointer Chains (Chapter 9)**: Sentinel dummy nodes, Floyd's cycle detection invariants, and in-place link inversions.

In **Part IV: Stacks, Queues, Hashing, and Sets**, we ascend to foundational abstract data types: monotonic stacks, circular ring buffers, hash functions, and collision resolution architectures.
