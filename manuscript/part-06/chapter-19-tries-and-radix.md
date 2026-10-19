# CHAPTER 19: TRIES, RADIX TREES, AND PREFIX PROCESSING

> *"In comparison-based trees, keys are atomic, opaque monoliths compared by wholesale relation. In a Trie, keys are disassembled into their elementary alphabetical constituents: each edge represents a single symbol transition, transforming prefix matching, autocomplete, and IP routing from costly string comparisons into single-step pointer traversals."*

---

## 19.1 The Trie Abstraction: Digital Search Trees

The term **Trie** (derived from re**trie**val, coined by Edward Fredkin and René de la Briandais) describes a multiway search tree where:
1. Keys are sequences of symbols drawn from a finite alphabet $\Sigma$.
2. Nodes do not store complete keys; instead, a node's position in the tree defines the key associated with it.
3. All descendants of a node share a common string prefix associated with that node.
4. The root node is associated with the empty sequence $\varepsilon$.

```
                      ( root )
                     /        \
                   'a'        't'
                   /            \
                 ( a )          ( t )
                 /   \            \
               'p'   'r'          'o'
               /       \            \
             ( ap )   ( ar )       ( to )*
             /           \
           'p'           't'
           /               \
        ( app )*          ( art )*
          /
        'l'
        /
     ( appl )
       /
     'e'
     /
   ( apple )*
   
   [* indicates terminal node marking end of a valid key]
```

### The Complexity Advantage
In a balanced BST storing $N$ strings of average length $L$:
- Comparing two strings costs $O(L)$ character comparisons.
- Search time is $O(L \cdot \log N)$.
In a **Trie**:
- Search time depends **only on the length of the query string $L$**:
$$\text{Search Time} = \Theta(L)$$
- The lookup time is completely **independent of the number of keys $N$** stored in the trie!

---

## 19.2 Memory Topologies of Trie Nodes

The primary challenge of standard tries is **memory consumption**. For an alphabet of size $|\Sigma|$:

### 1. Fixed-Size Array Pointers
Each node contains an array of $|\Sigma|$ pointers:
```cpp
struct TrieNode {
    bool is_terminal;
    TrieNode* children[26]; // 26 * 8 bytes = 208 bytes per node!
};
```
- **Lookup**: Blindingly fast $O(1)$ array indexing `children[c - 'a']`.
- **Memory Cost**: Catastrophic sparsity. If the average branching factor is only $2$ or $3$, over $90\%$ of pointers are `nullptr`. For large alphabets (e.g. Unicode or 256-byte ASCII), memory explodes to $2048$ bytes per node.

### 2. Associative Hash Map / Dynamic Vector
Each node stores a hash table or sorted vector of active outgoing transitions.
- **Memory**: Dense, storing only active edges.
- **Lookup**: Slight overhead of hash lookup or binary search per character transition.

### 3. Bitwise Binary Tries (Alphabet $\Sigma = \{0, 1\}$)
When keys are numbers, IP addresses, or binary hashes:
- $|\Sigma| = 2$.
- Each node has at most two children (`left = 0`, `right = 1`).
- Used extensively in routing tables (CIDR prefix matching) and bitwise XOR queries.

---

## 19.3 Radix Trees (Patricia Tries): Edge Compression

In a standard trie, non-branching paths (chains of nodes where each node has exactly one child) create severe pointer chasing and cache waste:
```
( a ) --> 'p' --> ( ap ) --> 'p' --> ( app ) --> 'l' --> ( appl ) --> 'e' --> ( apple )*
```
Five pointer dereferences are wasted to spell out `"pple"`.

### The Radix / Patricia Invariant
A **Radix Tree** (or Patricia Trie — *Practical Algorithm to Retrieve Information Coded in Alphanumeric*) compresses every non-branching chain into a single edge labeled with the entire substring:

```
( root )
   |
  "a"
   |
 ( a )
   | \
   |  "rt" --> ( art )*
  "pp"
   |
 ( app )*
   |
  "le"
   |
 ( apple )*
```

### Key Invariant
Every internal node in a Radix Tree (except possibly the root) has at least **two children** (or is a terminal key).
- Consequently, for $N$ keys, a Radix Tree contains at most $2N - 1$ total nodes!
- Memory is strictly linear in the number of stored keys: $O(N)$, completely immune to path-length bloat.

---

## 19.4 The 20-Step Problem Breakdown: Compressed Bitwise Radix Trie with Longest Prefix Match (`TRIE-0001`)

We now examine a foundational systems algorithm implemented at the core of network routers (BGP / OSPF / Linux Kernel FIB table): **Longest Prefix Match (LPM)** on 32-bit IPv4 routing subnets using a compressed bitwise radix trie.

### Step 1: Real-World Motivation & Context
In core internet routers, packets arrive at rates exceeding 100 million packets per second on 100 GbE fiber links. Each incoming packet has a 32-bit destination IP address. The router must determine the next-hop interface by finding the **longest matching subnet mask** (e.g., matching `192.168.1.0/24` over the fallback `192.168.0.0/16`). A linear scan over 1,000,000 routing rules is impossible. A compressed bitwise radix trie performs this classification in at most 32 bit-tests.

### Step 2: Formal Problem Specification
- **Requirements**:
  Implement a Bitwise Routing Trie supporting:
  1. `insert_route(ip, prefix_len, next_hop)`: Insert an IPv4 subnet rule specified by a 32-bit integer `ip`, a mask length `prefix_len` ($0 \le \text{prefix\_len} \le 32$), and a routing target `next_hop`.
  2. `lookup_lpm(ip)`: Given a destination 32-bit IP, return the `next_hop` of the **longest matching prefix rule**. If no route matches, return a default sentinel (`-1`).
- **Constraints**:
  - $0 \le N \le 10^5$ routing rules.
  - Worst-case lookup time: At most $32$ bit inspections ($\Theta(1)$ relative to $N$).
  - Auxiliary Memory: Strictly bounded by $O(N)$ nodes.

### Step 3: Algorithmic Decision Framework (ADF) Formulation
1. *Key Type*: 32-bit unsigned binary integers.
2. *Query Type*: Longest Prefix Match (find the deepest terminal node along the bit path).
3. *Path Length*: Fixed at 32 bits maximum.
4. *Decision*: Bitwise Trie where edge transitions follow bits from Most Significant Bit (MSB, bit 31) down to Least Significant Bit (LSB).

### Step 4: Mathematical Invariant Definition
Let IP address $X$ have binary representation:
$$X = \sum_{k=0}^{31} b_k 2^{31 - k} \quad \text{where } b_k \in \{0, 1\}$$

A routing prefix $(P, L)$ matches $X$ if and only if the most significant $L$ bits of $P$ and $X$ are identical:
$$(X \gg (32 - L)) == (P \gg (32 - L))$$

During traversal of query $X$:
- At depth $d$, extract bit $b_d = (X \gg (31 - d)) \ \& \ 1$.
- Transition to child $b_d$.
- If child $b_d$ does not exist, traversal terminates.
- The **Longest Prefix Match** is the most recently visited node along the path that has a valid route payload.

```
IP: 192.168.1.100 (11000000.10101000.00000001.01100100)
Trie Navigation:
Depth 0: Bit 1 -> Child 1
Depth 1: Bit 1 -> Child 1
Depth 2: Bit 0 -> Child 0
...
Track `last_valid_next_hop` as we descend.
```

### Step 5: State Transitions and Route Overwrite
- When inserting $(P, L, \text{next\_hop})$:
  1. Start at root.
  2. For $d = 0$ to $L - 1$:
     - $b = (P \gg (31 - d)) \ \& \ 1$.
     - If `child[b]` is null, allocate new node.
     - Move to `child[b]`.
  3. At depth $L$, set `has_route = true` and `next_hop = target`.
  *Invariant*: Shorter overlapping prefixes reside at ancestors; longer prefixes reside deeper.

### Step 6: Loop Variant & Termination
The maximum depth of the trie is strictly bounded by $W = 32$.
Both insertion and lookup loops decrement the remaining bits $32 - d$ by $1$ at each step.
The loop terminates in at most 32 steps.
Time complexity is strictly $O(W) = O(1)$ per operation!

### Step 7: Proof of Correctness
- **Prefix Path Equivalence**: The sequence of bits along the unique path from root to a node at depth $d$ corresponds uniquely to the bit prefix of length $d$.
- **LPM Maximality**: Traversing the bits of query IP $X$ visits ancestors in strictly increasing order of prefix length ($0, 1, 2, \dots$). By updating the candidate answer whenever `has_route == true`, the recorded answer upon termination is the maximum prefix length that matches $X$. Any deeper match would require matching bits that do not exist or differ from $X$, which is impossible by trie construction. $\blacksquare$

### Step 8: Concrete Trace
Routing Table:
1. `0.0.0.0/0` (Default route) $\to \text{NextHop } 1$
2. `192.168.0.0/16` $\to \text{NextHop } 2$
3. `192.168.1.0/24` $\to \text{NextHop } 3$

Query IP: `192.168.1.55`
1. At root (depth 0): Matches `/0`. Candidate $\leftarrow 1$.
2. Traverse 16 bits matching `192.168`: Reaches depth 16 node. Matches `/16`. Candidate $\leftarrow 2$.
3. Traverse 8 more bits matching `.1`: Reaches depth 24 node. Matches `/24`. Candidate $\leftarrow 3$.
4. Traverse remaining bits: No deeper route node exists.
5. Return candidate: $3$. Correct!

### Step 9: Edge Cases & Guards
- **Default Route ($L = 0$)**: Stored directly at the root node.
- **Host Route ($L = 32$)**: Full 32-bit exact match at a leaf node.
- **No Route Matched**: Root has no route; returns $-1$.
- **Duplicate Prefix Insertion**: Overwrites previous `next_hop` with updated policy.

### Step 10: Standard ISO C++20 Implementation
```cpp
// solutions/cpp/TRIE-0001.cpp
#include <iostream>
#include <vector>
#include <memory>
#include <cstdint>
#include <cassert>

namespace trie_0001 {

struct TrieNode {
    int next_hop; // -1 if non-terminal
    std::unique_ptr<TrieNode> child[2];

    TrieNode() : next_hop(-1) {
        child[0] = nullptr;
        child[1] = nullptr;
    }
};

class RoutingTrie {
private:
    std::unique_ptr<TrieNode> root;

public:
    RoutingTrie() : root(std::make_unique<TrieNode>()) {}

    // Inserts a CIDR prefix route: ip/prefix_len -> next_hop
    void insert_route(uint32_t ip, int prefix_len, int next_hop) {
        assert(prefix_len >= 0 && prefix_len <= 32);
        TrieNode* curr = root.get();

        for (int i = 0; i < prefix_len; ++i) {
            int bit = (ip >> (31 - i)) & 1;
            if (!curr->child[bit]) {
                curr->child[bit] = std::make_unique<TrieNode>();
            }
            curr = curr->child[bit].get();
        }
        curr->next_hop = next_hop;
    }

    // Returns the next_hop of the longest matching prefix for the given destination IP
    int lookup_lpm(uint32_t ip) const {
        const TrieNode* curr = root.get();
        int best_next_hop = curr->next_hop;

        for (int i = 0; i < 32; ++i) {
            int bit = (ip >> (31 - i)) & 1;
            if (!curr->child[bit]) {
                break;
            }
            curr = curr->child[bit].get();
            if (curr->next_hop != -1) {
                best_next_hop = curr->next_hop;
            }
        }
        return best_next_hop;
    }
};

// Helper to convert dotted-decimal string to uint32_t
uint32_t ip_to_int(uint8_t a, uint8_t b, uint8_t c, uint8_t d) {
    return (static_cast<uint32_t>(a) << 24) |
           (static_cast<uint32_t>(b) << 16) |
           (static_cast<uint32_t>(c) << 8)  |
           static_cast<uint32_t>(d);
}

} // namespace trie_0001
```

### Step 11: Python 3.12+ Implementation
```python
# solutions/python/TRIE-0001.py
from typing import Optional, List

class TrieNode:
    def __init__(self):
        self.next_hop: int = -1
        self.child: List[Optional['TrieNode']] = [None, None]

class RoutingTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert_route(self, ip: int, prefix_len: int, next_hop: int) -> None:
        """Inserts an IPv4 routing prefix into the bitwise trie."""
        curr = self.root
        for i in range(prefix_len):
            bit = (ip >> (31 - i)) & 1
            if curr.child[bit] is None:
                curr.child[bit] = TrieNode()
            curr = curr.child[bit]
        curr.next_hop = next_hop

    def lookup_lpm(self, ip: int) -> int:
        """Performs Longest Prefix Match lookup for a 32-bit IP address."""
        curr = self.root
        best_next_hop = curr.next_hop

        for i in range(32):
            bit = (ip >> (31 - i)) & 1
            if curr.child[bit] is None:
                break
            curr = curr.child[bit]
            if curr.next_hop != -1:
                best_next_hop = curr.next_hop

        return best_next_hop

def ip_to_int(a: int, b: int, c: int, d: int) -> int:
    return (a << 24) | (b << 16) | (c << 8) | d
```

### Step 12: Asymptotic & Microarchitectural Complexity
- **Time Complexity**:
  - `insert_route`: Strictly $O(W)$ operations, where $W = 32$ bits. Max 32 pointer transitions.
  - `lookup_lpm`: Strictly $O(W)$ operations. At most 32 loop cycles.
  - Time is strictly $\Theta(1)$ with respect to the total number of rules $N$!
- **Space Complexity**: Each rule of length $L$ allocates at most $L \le 32$ nodes. Total space is bounded by $O(N \cdot W)$, which simplifies to $O(N)$ since $W = 32$ is a fixed constant.
- **Hardware Realization**: In silicon hardware (TCAM — Ternary Content-Addressable Memory), bitwise prefix matching is performed in parallel in a single clock cycle.

### Step 13: Failure Modes & Anti-Patterns
- **Bit Shift Order**: Shifting by $(31 - i)$ evaluates the MSB first. Shifting by $i$ evaluates LSB first, which destroys CIDR prefix semantics!
- **Premature Loop Termination**: Ending the search at the first matched terminal returns the *shortest* prefix instead of the *longest*. The search must continue down to the deepest matching node while maintaining `best_next_hop`.

### Step 14: Dual-Language Nuance & Idioms
- **C++20**: Utilizing `std::unique_ptr<TrieNode>` ensures complete recursive deallocation when the routing trie is destroyed, preventing memory leaks in dynamic route update engines.
- **Python 3.12**: Bitwise integers in Python handle unsigned 32-bit operations naturally without signed integer underflow issues.

### Step 15: Unit Tests & Verification Fixtures
Differential testing verifies:
1. Default route (`/0`) matches any arbitrary IP when no more specific route exists.
2. Specific subnet (`/24`) correctly overrides broader subnet (`/16`).
3. Host route (`/32`) takes highest priority.
4. Non-matching IP returns $-1$ when no default route exists.

### Step 16: Reader Engineering Challenges
1. **Multi-Bit Triebounds (2-Bit Stride)**: Modify the trie to process 2 bits per level ($|\Sigma| = 4$), halving tree depth from 32 to 16.
2. **Path-Compressed Patricia Trie**: Compress single-child paths by storing a skip-length integer in each node, reducing memory consumption by $50\%$.

---

## 19.5 Chapter Summary & Part VI Milestone

With Chapter 19 complete, **Part VI: Trees, Heaps, and Tries** is fully realized:
- **Chapter 16**: Established the graph-theoretic foundations of hierarchical trees and the BST invariant.
- **Chapter 17**: Solved adversarial BST degradation through AVL rotations and explored multiway B-trees for block storage.
- **Chapter 18**: Demonstrated how deliberate partial ordering in binary and Min-Max heaps enables $O(1)$ extrema access in contiguous arrays.
- **Chapter 19**: Deconstructed atomic keys into symbol transitions, enabling length-dependent $O(L)$ retrieval and hardware-speed routing classifications.

The curriculum now stands ready for **Part VII: Range Queries and Advanced Data Structures**, advancing into Disjoint Set Union, Fenwick Trees, Segment Trees, and Heavy-Light Decomposition.
