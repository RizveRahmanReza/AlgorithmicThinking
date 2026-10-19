# PROBLEMS MASTER INDEX & CATALOG

This document indexes all verified and in-progress problems admitted into *The Art of Algorithmic Thinking*.

---

## Catalog Summary
- **Target Count**: 1,200+
- **Admitted Problems**: 26
- **Fully Implemented in C++20**: 26 (`SOLV-0001` through `DAG-0001`)
- **Fully Implemented in Python 3**: 26 (`SOLV-0001` through `DAG-0001`)
- **Verification Environment**: Host compilers offline (`UNVERIFIED_ENVIRONMENT`).

---

## Problem Ledger

### Problem Family: Problem Solving & Methodology (`SOLV`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`SOLV-0001`](../solutions/cpp/SOLV-0001.cpp) | **The Anomaly Subsegment Identification** | Level 1 (Foundation) | Prefix Invariant / Kadane Extension | Continuous sum tracking with non-negative lower bound reset | Implemented (C++20 & Py3.12) |
| [`SOLV-0002`](../solutions/cpp/SOLV-0002.cpp) | **Stable Resource Allocation Under Capacity Constraints** | Level 2 (Easy) | Sweep-Line / Capacity Invariant | Discretize continuous timeline into delta events; releases sort before allocations | Implemented (C++20 & Py3.12) |
| [`SOLV-0003`](../solutions/cpp/SOLV-0003.cpp) | **Maximum Subarray Sum: From $O(N^3)$ to $O(N)$** | Level 2 (Easy) | Kadane Invariant / Dynamic Programming | Local optimal suffix sum preserves global maximum; differential oracle validation | Implemented (C++20 & Py3.12) |

### Problem Family: Mathematics, Logic, and Proofs (`MATH`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`MATH-0001`](../solutions/cpp/MATH-0001.cpp) | **Strict Two-Sum Uniqueness and Invariant Verification** | Level 2 (Easy) | Two-Pointer Monotonic Search | Inward pointer stride preserves solution space; contradiction proof eliminates candidate rows/cols | Implemented (C++20 & Py3.12) |
| [`MATH-0002`](../solutions/cpp/MATH-0002.cpp) | **Inversion Counting via Divide-and-Conquer** | Level 3 (Intermediate) | MergeSort Invariant / Master Theorem | Count split inversions in bulk using sorted half-array boundaries | Implemented (C++20 & Py3.12) |
| [`MATH-0003`](../solutions/cpp/MATH-0003.cpp) | **Amortized Analysis of Dynamic Array Geometric Growth** | Level 2 (Easy) | Banker's Accounting / Potential Method | Geometric reallocation guarantees O(1) amortized cost vs O(N) arithmetic collapse | Implemented (C++20 & Py3.12) |

### Problem Family: Arrays & Contiguous Sequences (`ARR`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`ARR-0001`](../solutions/cpp/ARR-0001.cpp) | **In-Place Array Rotation and Cache Line Alignment** | Level 2 (Easy) | Three-Step Reversal / Cache Locality | Decompose cyclic permutation into prefix/suffix mirror inversions; O(1) auxiliary space | Implemented (C++20 & Py3.12) |

### Problem Family: Strings & Sequence Processing (`STR`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`STR-0001`](../solutions/cpp/STR-0001.cpp) | **Valid Palindrome Invariant with Dual-Pointer In-Place Filtering** | Level 1 (Foundation) | Dual-Pointer Inward Scan / Read-Write Filter | Stream-filter non-alphanumeric chars on the fly without intermediate heap buffers; O(1) space | Implemented (C++20 & Py3.12) |

### Problem Family: Pointer-Based & Linked Structures (`LIST`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`LIST-0001`](../solutions/cpp/LIST-0001.cpp) | **Floyd's Cycle Detection and In-Place List Inversion** | Level 2 (Easy) | Tortoise & Hare / Relative Velocity | Relative distance decreases by 1 in cycle; L1 = (k-1)C + (C-L2) entry proof; 3-pointer reversal | Implemented (C++20 & Py3.12) |

### Problem Family: Stacks, Queues, and Linear ADTs (`STACK`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`STACK-0001`](../solutions/cpp/STACK-0001.cpp) | **Valid Parentheses String Parsing and LIFO Invariants** | Level 1 (Foundation) | LIFO Delimiter Matching / CFG Grammar | Push expected closers; verify innermost scope termination; fast parity rejection | Implemented (C++20 & Py3.12) |
| [`STACK-0002`](../solutions/cpp/STACK-0002.cpp) | **Next Greater Element with Circular Invariant** | Level 2 (Easy) | Monotonic Decreasing Stack / Virtual Doubling | Maintain decreasing order; resolve smaller waiting indices in O(1) amortized time | Implemented (C++20 & Py3.12) |

### Problem Family: Hashing & Associative Structures (`HASH`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`HASH-0001`](../solutions/cpp/HASH-0001.cpp) | **Cache-Conscious Flat Hash Map with Linear Probing** | Level 3 (Intermediate) | Open Addressing / SplitMix64 / Tombstones | Power-of-two bitwise masking, contiguous flat layout, and tombstone search continuity | Implemented (C++20 & Py3.12) |

### Problem Family: Search Paradigms (`SRCH`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`SRCH-0001`](../solutions/cpp/SRCH-0001.cpp) | **Capacity Allocation via Binary Search on Answer Space** | Level 2 (Easy) | Binary Search on Answer Space / Range Monotonicity | Monotonic feasibility predicate converts combinatorial search into logarithmic greedy evaluations | Implemented (C++20 & Py3.12) |

### Problem Family: Sorting & Partitioning (`SORT`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`SORT-0001`](../solutions/cpp/SORT-0001.cpp) | **Dutch National Flag In-Place 3-Way Partitioning** | Level 2 (Easy) | Dijkstra 3-Way Partition / Loop Variant | Four-interval invariant isolates identical keys, collapsing QuickSort duplicate degradation to O(N) | Implemented (C++20 & Py3.12) |

### Problem Family: Fundamental Array Patterns (`PATT`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`PATT-0001`](../solutions/cpp/PATT-0001.cpp) | **Dynamic Sliding Window with Multi-Constraint Frequency Invariant** | Level 3 (Intermediate) | Dynamic Sliding Window / Deficit Counter | Monotonic two-pointer expansion/contraction guarantees O(N+M) minimum coverage subsegment | Implemented (C++20 & Py3.12) |

### Problem Family: Trees & Hierarchical Structures (`TREE`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`TREE-0001`](../solutions/cpp/TREE-0001.cpp) | **BST Validation and Invariant Reconstruction Under Serialization** | Level 2 (Easy) | Range-Bounded DFS / Monotonic Parser | Open interval ancestor bounds enforce global BST validity; single-pass pre-order reconstruction runs in O(N) | Implemented (C++20 & Py3.12) |
| [`TREE-0002`](../solutions/cpp/TREE-0002.cpp) | **AVL Tree Self-Balancing Invariants and Rotations** | Level 4 (Advanced) | Height-Balanced AVL / 4-Case Rotation | Strict \|BF\| <= 1 invariant bounds tree height to <= 1.44 log2 N, restoring O(log N) against sorted streams | Implemented (C++20 & Py3.12) |

### Problem Family: Heaps & Priority Queues (`HEAP`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`HEAP-0001`](../solutions/cpp/HEAP-0001.cpp) | **Min-Max Heap and Real-Time Sliding Priority Window** | Level 4 (Advanced) | Min-Max Heap / Alternating Levels | Alternating min/max levels grant O(1) double-ended min and max access in a single contiguous array | Implemented (C++20 & Py3.12) |

### Problem Family: Tries & Prefix Structures (`TRIE`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`TRIE-0001`](../solutions/cpp/TRIE-0001.cpp) | **Compressed Bitwise Radix Trie with Routing Prefix Match** | Level 3 (Intermediate) | Bitwise Trie / Longest Prefix Match | Binary prefix decomposition yields guaranteed 32-step routing lookup independent of rule set size | Implemented (C++20 & Py3.12) |

### Problem Family: Disjoint Set Union (`DSU`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`DSU-0001`](../solutions/cpp/DSU-0001.cpp) | **Dynamic Connectivity with Rollback and Size-Rank Invariants** | Level 3 (Intermediate) | Rollback DSU / Union by Size | Omitting path compression unlocks O(1) state rollbacks and transactional checkpoints in O(log N) query time | Implemented (C++20 & Py3.12) |

### Problem Family: Fenwick Trees (`FENW`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`FENW-0001`](../solutions/cpp/FENW-0001.cpp) | **Dynamic Prefix Inversions and Multidimensional BIT** | Level 2 (Easy) | Fenwick Tree / Coordinate Compression | Lowbit dyadic intervals partition dynamic prefix sums in O(log N) time with zero pointer memory overhead | Implemented (C++20 & Py3.12) |

### Problem Family: Segment Trees & Range Structures (`SEGT`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`SEGT-0001`](../solutions/cpp/SEGT-0001.cpp) | **Dynamic Range Affine Transformations and Lazy Invariant Propagation** | Level 4 (Advanced) | Segment Tree / Dual Lazy Composition | Non-commutative composition of affine tags (M2*M1, M2*A1 + A2) enables simultaneous range scale and add in O(log N) | Implemented (C++20 & Py3.12) |

### Problem Family: Advanced Query Structures (`QRY`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`QRY-0001`](../solutions/cpp/QRY-0001.cpp) | **Static Range Minimum Query via Sparse Table** | Level 3 (Intermediate) | Sparse Table / Idempotence | Two overlapping dyadic intervals of length 2^k yield strictly O(1) query time for idempotent operators | Implemented (C++20 & Py3.12) |

### Problem Family: Graph Foundations & Traversals (`GRPH`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`GRPH-0001`](../solutions/cpp/GRPH-0001.cpp) | **Bipartite Verification and 2-Coloring Invariant** | Level 2 (Easy) | BFS 2-Coloring / Kőnig's Invariant | Parity distance coloring isolates odd cycles and proves two-set partitionability in O(V + E) time | Implemented (C++20 & Py3.12) |

### Problem Family: Shortest Paths & Routing (`PATH`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`PATH-0001`](../solutions/cpp/PATH-0001.cpp) | **Dijkstra with Strict Non-Negative Invariant and State-Space Distances** | Level 3 (Intermediate) | State-Space Dijkstra / Priority Queue | Expanding vertices into (u, k) resource states guarantees optimal routing with bounded discount allowances | Implemented (C++20 & Py3.12) |

### Problem Family: Directed Acyclic Graphs (`DAG`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`DAG-0001`](../solutions/cpp/DAG-0001.cpp) | **Course Prerequisite Cycle Isolation and Lexicographical TopoSort** | Level 2 (Easy) | Kahn's Algorithm / Min-Heap Priority Queue | Zero in-degree elimination with min-heap guarantees deterministic lexicographical scheduling and deadlock cycle isolation | Implemented (C++20 & Py3.12) |

### Problem Family: Minimum Spanning Trees (`MST`)

| Problem ID | Title | Difficulty | Primary Pattern | Invariant / Key Idea | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`MST-0001`](../solutions/cpp/MST-0001.cpp) | **Minimax Path and Dynamic Kruskal MST under Bottleneck Edge Weights** | Level 4 (Advanced) | Kruskal MST + Binary Lifting LCA | Every MST is an MBST; maximum tree-edge on LCA path strictly equals global minimax path bottleneck | Implemented (C++20 & Py3.12) |

---

## Machine-Readable Catalog Specification
All entries are synchronized in [`problems/catalog.jsonl`](catalog.jsonl). Each line contains a complete JSON record with:
`problem_id`, `title`, `chapter`, `family`, `difficulty`, `prerequisites`, `pattern`, `cpp_path`, `python_path`, `test_path`, `verification_status`.
