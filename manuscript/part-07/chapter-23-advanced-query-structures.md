# CHAPTER 23: ADVANCED QUERY STRUCTURES

> *"When updates are absent, idempotence allows two overlapping intervals to answer range queries in strictly $O(1)$ time via Sparse Tables. When queries can be reordered offline, Mo's algorithm and Square-Root Decomposition dance along Hilbert curves and block partitions to achieve subquadratic speedups. And when queries traverse paths on arbitrary trees, Heavy-Light Decomposition straightens branched hierarchies into contiguous linear intervals."*

---

## 23.1 The Idempotence Principle and Sparse Tables

A binary operator $\circ$ is **idempotent** if applying it to identical operands leaves the value unchanged:
$$x \circ x = x \quad \forall x \in S$$

Examples of idempotent operators:
- $\min(x, x) = x$
- $\max(x, x) = x$
- $\gcd(x, x) = x$
- $\text{bitwise\_OR}(x, x) = x$
- $\text{bitwise\_AND}(x, x) = x$

Notice that addition is **NOT** idempotent: $x + x = 2x \neq x$.

### The Overlapping Range Query Theorem
Because $\min$ is idempotent, the minimum of an arbitrary interval $[l, r]$ of length $L = r - l + 1$ can be evaluated by taking the minimum of **two overlapping intervals of length $2^k$**, where $2^k$ is the largest power of two $\le L$:
$$k = \lfloor \log_2(r - l + 1) \rfloor$$
$$\min_{i=l}^r A[i] = \min\left( \min_{i=l}^{l + 2^k - 1} A[i], \ \min_{i=r - 2^k + 1}^r A[i] \right)$$

```
Interval [l, r] of length L = 7:
Indices:      [ l   l+1  l+2  l+3  l+4  l+5   r ]
Range 1 (2^2): [===============>]                (l .. l+3)
Range 2 (2^2):             [==================>] (r-3 .. r)
Overlap:                 [======] (Overlapping is harmless due to idempotence!)
```

### Sparse Table Construction and Memory Layout
Let $\text{ST}[k][i]$ store the query aggregation for range $[i, i + 2^k - 1]$:
- **Base Case ($k = 0$)**: $\text{ST}[0][i] = A[i]$.
- **Dynamic Programming Recurrence**:
  $$\text{ST}[k][i] = \min(\text{ST}[k-1][i], \ \text{ST}[k-1][i + 2^{k-1}])$$

#### Complexity:
- **Preprocessing Time**: $\Theta(N \log N)$ (each of the $\log_2 N$ rows takes $O(N)$ steps).
- **Space**: $\Theta(N \log N)$ integers.
- **Query Time**: **Strictly $\Theta(1)$** single-instruction lookup!

---

## 23.2 Square-Root Decomposition: The Sqrt Trick

When an array undergoes dynamic updates and arbitrary range queries, and writing a full Segment Tree is too complex or costly, **Square-Root Decomposition** partitions the array into $\lceil N / B \rceil$ blocks of size $B = \lceil \sqrt{N} \rceil$:

```
Block 0: [ 0 .. B-1 ]     Summary: sum_0, min_0
Block 1: [ B .. 2B-1 ]    Summary: sum_1, min_1
...
Block k: [ kB .. (k+1)B-1] Summary: sum_k, min_k
```

### Query Execution
An arbitrary query $[l, r]$ spans:
1. **Left Fringe**: Elements from $l$ to the end of $l$'s block (at most $B$ elements).
2. **Intermediate Full Blocks**: Whole blocks fully enclosed in $[l, r]$ (at most $N/B$ blocks, inspected in $O(1)$ per block summary).
3. **Right Fringe**: Elements from the start of $r$'s block up to $r$ (at most $B$ elements).

$$\text{Query Cost} = O(B + N/B)$$
By the AM-GM inequality, $B + N/B$ is minimized when $B = \sqrt{N}$:
$$\text{Query Time} = O(\sqrt{N}), \quad \text{Update Time} = O(1) \text{ or } O(\sqrt{N})$$

---

## 23.3 Mo's Algorithm: Offline Query Optimization

Given $Q$ static range queries $[l_i, r_i]$ that do not require online answers, **Mo's Algorithm** reorders the queries to minimize the total Manhattan distance traversed by a two-pointer window $[L, R]$.

### The Sorting Order
Sort all queries $(l_i, r_i)$ primarily by $l_i$'s block index $\lfloor l_i / B \rfloor$, and secondarily by $r_i$:
- If $\lfloor l_1 / B \rfloor \neq \lfloor l_2 / B \rfloor$: sort by $\lfloor l_1 / B \rfloor < \lfloor l_2 / B \rfloor$.
- If in the same block: sort by $r_1 < r_2$ (or alternate $r$ direction on odd blocks—**Hilbert curve optimization**).

### Complexity Proof: $O((N + Q) \sqrt{N})$
Choose block size $B = \frac{N}{\sqrt{Q}}$:
1. **Right Pointer Movement**: For queries in the same block, $r$ moves monotonically from $0$ to $N$. Across all $N/B$ blocks, total $R$ moves are:
   $$\frac{N}{B} \cdot N = \frac{N^2}{B} = N \sqrt{Q}$$
2. **Left Pointer Movement**: For each query, $l$ wanders at most $B$ steps within its block:
   $$Q \cdot B = Q \cdot \frac{N}{\sqrt{Q}} = N \sqrt{Q}$$
Total pointer shifts: $\Theta((N + Q) \sqrt{N})$.
If adding/removing an element from the window state costs $O(1)$, the entire batch of $Q$ queries executes in $O((N + Q) \sqrt{N})$ time!

---

## 23.4 Heavy-Light Decomposition (HLD) on Trees

How do we answer range queries on the simple path between two arbitrary nodes $u$ and $v$ in an unrooted tree?

### The Heavy/Light Edge Classification
For every node $u$ with children:
- **Heavy Child**: The child $v$ whose subtree has the maximum size:
  $$\text{size}[v] = \max_{c \in \text{children}(u)} \text{size}[c]$$
- **Heavy Edge**: Edge $(u, v)$ connecting $u$ to its heavy child.
- **Light Edge**: All other outgoing edges to children.

```
                  ( root )
                 //      \
              ( Heavy )   ( Light )
              //     \
           ( Heavy )  ( Light )
```

### The Path Decomposition Theorem
Chaining heavy edges together decomposes the tree into a set of disjoint **Heavy Paths**.
- **Crucial Invariant**: When moving upward from any node $u$ to the root, a light edge can be crossed at most $\lfloor \log_2 N \rfloor$ times because each light step at least doubles the subtree size!
- Assigning in-order DFS arrival timestamps to heavy paths maps every heavy path to a **contiguous segment in an array**!
- Any path query between $u$ and $v$ is decomposed into at most $O(\log N)$ contiguous array intervals, answered via a Segment Tree in:
$$\text{Path Query Cost} = O(\log^2 N)$$

---

## 23.5 The 20-Step Problem Breakdown: Static Range Minimum Query via Sparse Table (`QRY-0001`)

We now construct the optimal $O(1)$ query static RMQ structure: the **Sparse Table with Fast Bitwise Logarithm Lookup**.

### Step 1: Real-World Motivation & Context
In Lowest Common Ancestor (LCA) algorithms on trees (via Euler Tour reductions), string processing (Longest Common Extensions via LCP arrays), and real-time audio sample peak analysis, millions of range minimum queries must be answered over static telemetry. An $O(\log N)$ segment tree incurs excessive CPU branch penalties. A Sparse Table delivers pure $O(1)$ single-cycle memory reads.

### Step 2: Formal Problem Specification
- **Requirements**:
  Implement a `SparseTable` supporting:
  1. `build(arr)`: Precompute range extrema in $O(N \log N)$ time.
  2. `query_min(l, r)`: Return $\min_{i=l}^r A[i]$ in strictly $\Theta(1)$ time.
  3. `query_min_index(l, r)`: Return the index of the minimum element in strictly $\Theta(1)$ time.
- **Constraints**:
  - $1 \le N \le 5 \times 10^5$.
  - $1 \le Q \le 10^7$ queries.
  - Elements: $-10^9 \le A[i] \le 10^9$.
  - Precomputation time: $O(N \log N)$.
  - Query time: $\Theta(1)$ strictly.
  - Memory: $O(N \log N)$.

### Step 3: Algorithmic Decision Framework (ADF) Formulation
1. *Static vs Dynamic*: Static dataset $\to$ No mutations.
2. *Operator Idempotence*: $\min(x, x) = x \to$ Idempotent.
3. *Query Throughput Budget*: $10^7$ queries requires sub-nanosecond $O(1)$ response without tree branches.
4. *Decision*: Dyadic Sparse Table with precomputed $\lfloor \log_2 \rfloor$ lookup table.

### Step 4: Mathematical Invariant Definition
Let $K = \lfloor \log_2 N \rfloor + 1$.
$\text{st}[k][i]$ denotes the index of the minimum element in subarray $A[i \dots i + 2^k - 1]$.
$$\text{st}[0][i] = i \quad \forall i \in [0, N-1]$$
$$\text{st}[k][i] = \text{argmin}(A[\text{st}[k-1][i]], \ A[\text{st}[k-1][i + 2^{k-1}]]) \quad \forall k \ge 1$$

For any query $[l, r]$ with length $\text{len} = r - l + 1$:
$$k = \lfloor \log_2(\text{len}) \rfloor$$
$$\text{idx}_1 = \text{st}[k][l]$$
$$\text{idx}_2 = \text{st}[k][r - 2^k + 1]$$
$$\text{ans\_index} = \text{argmin}(A[\text{idx}_1], A[\text{idx}_2])$$

### Step 5: Fast Logarithm Computation
To achieve strictly $O(1)$ query time without calling floating-point `std::log2()`:
- In C++20: Use `std::__lg(len)` or `std::countl_zero` bit-instructions (`BSR` / `LZCNT` on x86).
- Or precompute an array `log_table` of size $N + 1$:
$$\text{log\_table}[1] = 0, \quad \text{log\_table}[i] = \text{log\_table}[i / 2] + 1$$

### Step 6: Complexity & Invariant Proof
- **Table Dimensions**: The table has $K = \lfloor \log_2 N \rfloor + 1$ rows and $N$ columns.
- **Preprocessing**: Populating cell $(k, i)$ takes $O(1)$ comparisons. Total time: $\Theta(N \log N)$.
- **Query**: Computing $k$, indexing twice, and performing one comparison takes exactly 3 memory reads and 1 branch $\implies \Theta(1)$ strictly. $\blacksquare$

### Step 7: Concrete Trace
$A = [31, 41, 59, 26, 53, 58, 97]$.
Query: $[1, 5]$ ($A[1..5] = [41, 59, 26, 53, 58]$), length = 5.
1. $k = \lfloor \log_2 5 \rfloor = 2$ ($2^2 = 4$).
2. Range 1: $[1, 1 + 4 - 1] = [1, 4] \implies \min(41, 59, 26, 53) = 26$ at index 3.
3. Range 2: $[5 - 4 + 1, 5] = [2, 5] \implies \min(59, 26, 53, 58) = 26$ at index 3.
4. Combined: $\min(A[3], A[3]) = 26$ at index 3. Correct in $O(1)$!

### Step 8: Edge Cases & Guards
- **$l == r$**: Length is 1, $k = 0$, checks $A[l]$ with $A[l]$, returns $l$.
- **Entire Array ($l = 0, r = N-1$)**: Handled without overflow.
- **Duplicate Minimums**: Returns the earlier index consistently.

### Step 9: Standard ISO C++20 Implementation
```cpp
// solutions/cpp/QRY-0001.cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cassert>

namespace qry_0001 {

class SparseTable {
private:
    int n;
    int max_log;
    std::vector<int> log_table;
    std::vector<std::vector<int>> st; // Stores indices of minimums
    const std::vector<int>* raw_data;

    int min_index(int idx1, int idx2) const {
        return ((*raw_data)[idx1] <= (*raw_data)[idx2]) ? idx1 : idx2;
    }

public:
    explicit SparseTable(const std::vector<int>& arr)
        : n(static_cast<int>(arr.size())),
          raw_data(&arr) {
        if (n == 0) return;

        // 1. Precompute log table
        log_table.resize(n + 1, 0);
        for (int i = 2; i <= n; ++i) {
            log_table[i] = log_table[i / 2] + 1;
        }
        max_log = log_table[n] + 1;

        // 2. Precompute Sparse Table
        st.assign(max_log, std::vector<int>(n));
        for (int i = 0; i < n; ++i) {
            st[0][i] = i;
        }

        for (int k = 1; k < max_log; ++k) {
            int len = 1 << (k - 1);
            for (int i = 0; i + (1 << k) <= n; ++i) {
                st[k][i] = min_index(st[k - 1][i], st[k - 1][i + len]);
            }
        }
    }

    // O(1) query returning index of minimum element in [l, r]
    int query_min_index(int l, int r) const {
        assert(l <= r && l >= 0 && r < n);
        int len = r - l + 1;
        int k = log_table[len];
        return min_index(st[k][l], st[k][r - (1 << k) + 1]);
    }

    // O(1) query returning minimum value in [l, r]
    int query_min(int l, int r) const {
        return (*raw_data)[query_min_index(l, r)];
    }
};

} // namespace qry_0001
```

### Step 10: Python 3.12+ Implementation
```python
# solutions/python/QRY-0001.py
from typing import List

class SparseTable:
    def __init__(self, arr: List[int]):
        self.raw_data = arr
        self.n = len(arr)
        if self.n == 0:
            return

        # 1. Precompute log table
        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.max_log = self.log_table[self.n] + 1

        # 2. Build Sparse Table storing indices of minimums
        self.st: List[List[int]] = [[0] * self.n for _ in range(self.max_log)]
        for i in range(self.n):
            self.st[0][i] = i

        for k in range(1, self.max_log):
            half = 1 << (k - 1)
            full = 1 << k
            for i in range(self.n - full + 1):
                idx1 = self.st[k - 1][i]
                idx2 = self.st[k - 1][i + half]
                self.st[k][i] = idx1 if self.raw_data[idx1] <= self.raw_data[idx2] else idx2

    def query_min_index(self, l: int, r: int) -> int:
        """Returns the index of the minimum element in arr[l..r] in strictly O(1) time."""
        length = r - l + 1
        k = self.log_table[length]
        idx1 = self.st[k][l]
        idx2 = self.st[k][r - (1 << k) + 1]
        return idx1 if self.raw_data[idx1] <= self.raw_data[idx2] else idx2

    def query_min(self, l: int, r: int) -> int:
        """Returns the minimum value in arr[l..r] in strictly O(1) time."""
        return self.raw_data[self.query_min_index(l, r)]
```

### Step 11: Asymptotic & Microarchitectural Complexity
- **Time Complexity**:
  - Precomputation: $\Theta(N \log N)$ strictly.
  - Query: Strictly $\Theta(1)$ operations (zero loops, zero recursion).
- **Space Complexity**: $\Theta(N \log N)$ integers.
- **Microarchitectural Behavior**: Query touches at most two memory addresses in array `st[k]`, achieving maximum L1/L2 cache hit rate with zero branch mispredictions.

### Step 12: Failure Modes & Anti-Patterns
- **Applying Sparse Table to Sums**: Attempting to answer Range Sum Queries with a standard 2-interval Sparse Table double-counts the overlapping elements ($x + x = 2x$), producing incorrect answers. Sparse Tables strictly require **idempotence** for $O(1)$ overlap queries.
- **Log Table Off-by-One**: Querying `log_table[0]` accesses undefined memory. Length is always $\ge 1$.

### Step 13: Dual-Language Nuance & Idioms
- **C++20**: Storing indices instead of values allows the same Sparse Table to locate extrema locations for LCA Euler tour reductions without duplicating memory.
- **Python 3.12**: Precomputing integer logarithm table avoids expensive Python `math.log2()` floating-point roundoff errors.

### Step 14: Unit Tests & Verification Fixtures
Differential testing verifies:
1. Every subsegment $[l, r]$ matches Python's built-in `min(arr[l:r+1])`.
2. Adversarial arrays (sorted, reverse sorted, identical elements, alternating signs) produce identical answers.
3. 500 randomized subsegment queries verify $100\%$ differential oracle parity.

### Step 15: Reader Engineering Challenges
1. **Disjoint Sparse Table**: How can you achieve $O(1)$ range queries for **arbitrary non-idempotent monoids** (such as range multiplication or matrices) using a Disjoint Sparse Table?
2. **Fisher-Heun RMQ**: Combine Cartesian Trees, Four Russians speedup, and Sparse Tables to achieve $O(N)$ preprocessing and strictly $O(1)$ query time!

---

## 23.6 Chapter Summary & Part VII Milestone

With Chapter 23 complete, **Part VII: Range Queries and Advanced Data Structures** is fully achieved:
- **Chapter 20 (DSU)**: Mastered equivalence partitioning, proving the $O(\alpha(N))$ Inverse Ackermann bound and creating reversible transaction structures.
- **Chapter 21 (Fenwick Trees)**: Leveraged binary index representations (`lowbit`) to achieve $O(\log N)$ dynamic prefix sums with zero memory overhead.
- **Chapter 22 (Segment Trees)**: Universalized range queries across general monoids and deferred whole-interval updates via Lazy Propagation.
- **Chapter 23 (Advanced Query Structures)**: Exploited idempotence for $O(1)$ Sparse Table queries, square-root decomposition, and Heavy-Light Decomposition on trees.

With 23 chapters complete, the manuscript has established complete mastery of linear, hierarchical, and range query structures, and is ready to advance into **Part VIII: Graph Algorithms: Foundations** (BFS, DFS, Dijkstra, Bellman-Ford, DAGs, and Topological Sorting).
