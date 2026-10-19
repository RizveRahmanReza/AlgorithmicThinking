# CHAPTER 21: FENWICK TREES (BINARY INDEXED TREES)

> *"Prefix sums answer static range queries in $O(1)$ time, but choke on dynamic point updates with $O(N)$ rebuild costs. A Fenwick tree marries binary integer representation with partial prefix responsibilities, partitioning array prefixes into dyadic intervals determined by each index's least significant set bit (`i & -i`). Both point updates and prefix evaluations execute in $O(\log N)$ time with zero pointer overhead in a 1-indexed flat array."*

---

## 21.1 The Dynamic Prefix Sum Problem

Given an array $A$ of $N$ elements subject to intermixed queries:
1. `update(idx, delta)`: Add `delta` to $A[\text{idx}]$.
2. `query(idx)`: Compute prefix sum $\sum_{k=1}^{\text{idx}} A[k]$.
3. `range_query(l, r)`: Compute $\sum_{k=l}^r A[k] = \text{query}(r) - \text{query}(l - 1)$.

### The Engineering Dilemma
- **Raw Array**: Point update is $O(1)$, but range query is $O(N)$.
- **Static Prefix Sum Array**: Range query is $O(1)$, but point update is $O(N)$ (requires updating all subsequent prefix entries).
- **Segment Tree**: Both operations run in $O(\log N)$, but requires $4N$ memory, recursion overhead, or complex tree navigation.

Proposed by Boris Ryabko (1989) and popularized by Peter Fenwick (1994), the **Binary Indexed Tree (BIT)** or **Fenwick Tree** solves this with the absolute minimum footprint possible: **exactly $N$ integers in a flat array, zero pointer indirection, and simple bitwise index arithmetic.**

---

## 21.2 The Binary Structure of Indices and `lowbit`

Every positive integer $i$ can be uniquely expressed as a sum of powers of two:
$$i = 2^{k_1} + 2^{k_2} + \dots + 2^{k_m} \quad \text{where } k_1 > k_2 > \dots > k_m$$

The lowest power of two in this expansion is denoted as $\text{lowbit}(i)$:
$$\text{lowbit}(i) = i \ \& \ (-i)$$

### Two's Complement Bitwise Derivation
In two's complement arithmetic, the negative of an integer $-i$ is formed by inverting all bits and adding $1$:
$$-i = \sim i + 1$$
- Let $i$ in binary be $w\,1\,00\dots0$ (where $w$ is an arbitrary bit sequence).
- Then $\sim i$ is $(\sim w)\,0\,11\dots1$.
- Adding $1$ flips all the trailing 1s back to 0s and carries over into the lowest set bit position: $-i = (\sim w)\,1\,00\dots0$.
- Bitwise AND $i \ \& \ (-i)$ clears all bits in $w$, preserving **strictly the single least significant set bit**:
$$\text{lowbit}(12) = 12 \ \& \ (-12) = (01100_2) \ \& \ (10100_2) = 00100_2 = 4$$

---

## 21.3 Dyadic Interval Partitioning

In a Fenwick Tree array `tree` of size $N$ (using 1-based indexing):
Each index $i$ stores the cumulative sum of a half-open contiguous range ending at $i$ of length $\text{lowbit}(i)$:

$$\text{tree}[i] = \sum_{k = i - \text{lowbit}(i) + 1}^i A[k]$$

```
Index (binary)   lowbit(i)   Interval Covered by tree[i]
--------------------------------------------------------
1  (0001)        1           [1..1]
2  (0010)        2           [1..2]  (= A[1] + A[2])
3  (0011)        1           [3..3]
4  (0100)        4           [1..4]  (= A[1] + ... + A[4])
5  (0101)        1           [5..5]
6  (0110)        2           [5..6]
7  (0111)        1           [7..7]
8  (1000)        8           [1..8]  (= A[1] + ... + A[8])
```

```
Hierarchical Tree Responsibility Structure:
tree[8]: [================================================] (1..8)
tree[4]: [========================]                         (1..4)
tree[2]: [============]                                     (1..2)
tree[1]: [======]                                           (1..1)
tree[3]:               [======]                             (3..3)
tree[6]:                            [============]          (5..6)
tree[5]:                            [======]                (5..5)
tree[7]:                                           [======] (7..7)
```

---

## 21.4 The Traversal Invariants

### 1. Prefix Sum Query: Peeling Off Bits
To compute $\sum_{k=1}^i A[k]$:
- Add $\text{tree}[i]$, which covers $[i - \text{lowbit}(i) + 1, i]$.
- Jump backward to $i - \text{lowbit}(i)$.
- Repeat until $i == 0$.
- **Complexity**: Since each step clears the lowest set bit of $i$, the loop runs in at most $\text{popcount}(i) \le \log_2 N$ steps!

```cpp
long long query(int i) {
    long long sum = 0;
    for (; i > 0; i -= (i & -i)) {
        sum += tree[i];
    }
    return sum;
}
```

### 2. Point Update: Ascending Ancestors
When $A[i]$ increases by `delta`, which entries $\text{tree}[j]$ contain $A[i]$ in their coverage interval?
- Start at index $i$: add `delta` to $\text{tree}[i]$.
- Jump forward to the immediate parent covering $i$: $i + \text{lowbit}(i)$.
- Repeat while $i \le N$.
- **Complexity**: Each addition increases $i$'s lowest power of two, bounded by $\log_2 N$ iterations.

```cpp
void update(int i, long long delta) {
    for (; i <= n; i += (i & -i)) {
        tree[i] += delta;
    }
}
```

---

## 21.5 Linear-Time Initialization: $O(N)$ Construction

While calling `update` $N$ times builds a Fenwick Tree in $O(N \log N)$ time, the tree can be constructed in strictly $\Theta(N)$ time by propagating each node's value directly to its immediate parent:

```cpp
void build(const std::vector<long long>& arr) {
    for (int i = 1; i <= n; ++i) {
        tree[i] += arr[i - 1];
        int parent = i + (i & -i);
        if (parent <= n) {
            tree[parent] += tree[i];
        }
    }
}
```
Every entry is pushed to its parent in a single forward pass—strictly $N$ operations.

---

## 21.6 2D Multidimensional Fenwick Trees

The dyadic interval decomposition extends naturally to multiple dimensions. In 2D, $\text{tree}[i][j]$ stores the sum of the subgrid of width $\text{lowbit}(i)$ and height $\text{lowbit}(j)$:

$$\text{tree}[i][j] = \sum_{r = i - \text{lowbit}(i) + 1}^i \sum_{c = j - \text{lowbit}(j) + 1}^j M[r][c]$$

- Point Update $(r, c, \Delta)$ runs in $O(\log R \cdot \log C)$.
- Subgrid Query $(1, 1)$ to $(r, c)$ runs in $O(\log R \cdot \log C)$.
- Memory: Flat array of size $R \times C$. Zero pointer overhead.

---

## 21.7 The 20-Step Problem Breakdown: Dynamic Inversion Counting and Multidimensional BIT (`FENW-0001`)

We now apply the Fenwick Tree to solve a cornerstone problem in streaming algorithms: **Counting Inversions Dynamically Under Coordinate Compression**.

### Step 1: Real-World Motivation & Context
In recommendation systems, ranking engines (Kendall's tau distance), and real-time anomaly detection, algorithms measure the degree of disorder (inversions) in a sequence of user preferences or price vectors as items arrive dynamically. Because values can be arbitrarily large (e.g. 64-bit floating point numbers) and updates stream continuously, counting how many previously seen elements exceed the current item must execute in $O(\log N)$ time.

### Step 2: Formal Problem Specification
- **Requirements**:
  Given an arbitrary stream of $N$ integers $A = \langle a_1, a_2, \dots, a_N \rangle$:
  1. Coordinate-compress the universe into ranks $[1..U]$ where $U \le N$.
  2. For each element $a_i$, compute the number of previous elements $a_j$ ($j < i$) such that $a_j > a_i$.
  3. Return the total number of inversions in $A$.
  4. Support dynamic point insertions into the active multiset.
- **Constraints**:
  - $1 \le N \le 2 \times 10^5$.
  - Elements: $-10^9 \le a_i \le 10^9$.
  - Total inversion count can reach $\approx \frac{N(N-1)}{2} \approx 2 \times 10^{10}$ (requires 64-bit integers).
  - Time complexity: Strictly $O(N \log N)$.
  - Auxiliary space: Strictly $O(N)$ memory.

### Step 3: Algorithmic Decision Framework (ADF) Formulation
1. *Streaming Frequency Query*: For each incoming rank $r$, we need the count of elements in range $[r+1, U]$.
2. *Range Complement Invariant*: $\text{count}(> r) = \text{total\_seen} - \text{prefix\_sum}(r)$.
3. *Data Structure Selection*: Fenwick Tree maintains frequencies of compressed ranks in $O(\log U)$ time per element.

### Step 4: Mathematical Invariant Definition
Let $C(x)$ be the 1-based compressed rank of value $x \in A$, where $1 \le C(x) \le U \le N$.
Maintain a Fenwick Tree of size $U$, initially all zeros.
When processing $a_i$ with rank $r = C(a_i)$:
$$\text{inversions}(a_i) = i - 1 - \text{query}(r)$$
Where:
- $i - 1$ is the total count of elements processed so far.
- $\text{query}(r) = \sum_{k=1}^r \text{tree}[k]$ is the count of elements with rank $\le r$.
- The difference represents strictly elements $a_j > a_i$ for $j < i$.
After recording, execute $\text{update}(r, +1)$ to insert $a_i$ into the frequency tree.

### Step 5: Coordinate Compression Mechanics
1. Copy input array $A$ to temporary array $S$.
2. Sort $S$ in ascending order: $O(N \log N)$.
3. Deduplicate $S$ using `std::unique`: $U = |S| \le N$.
4. Map any value $x$ to its 1-based rank via binary search (`std::lower_bound`):
   $$\text{rank}(x) = (\text{binary\_search}(S, x) - S.\text{begin}()) + 1$$

### Step 6: Loop Variant & Complexity
The main loop processes $i$ from $0$ to $N - 1$.
At each iteration:
- Rank lookup costs $O(\log U)$.
- Fenwick query costs $O(\log U)$.
- Fenwick update costs $O(\log U)$.
Total iterations: $N$.
Total runtime: $O(N \log N)$ strictly.

### Step 7: Proof of Correctness
- **Strict Ordering**: Because elements are processed in chronological order $i = 1, \dots, N$, the Fenwick tree at step $i$ contains frequencies strictly of the prefix $a_1, \dots, a_{i-1}$.
- **Exhaustive Partition**: By definition, every element previously inserted has rank either $\le r$ or $> r$. Subtracting the count of elements with rank $\le r$ from total elements seen yields exactly the count of elements greater than $a_i$. Summing over all $i$ produces the total inversion count. $\blacksquare$

### Step 8: Concrete Trace
$A = [8, 4, 2, 1]$.
Sorted unique: $S = [1, 2, 4, 8]$. Ranks: $8 \to 4, 4 \to 3, 2 \to 2, 1 \to 1$.
1. $a_0 = 8$ (rank 4): seen 0, $\text{query}(4) = 0 \implies \text{inv} = 0 - 0 = 0$. Update rank 4 (+1).
2. $a_1 = 4$ (rank 3): seen 1, $\text{query}(3) = 0 \implies \text{inv} = 1 - 0 = 1$. Update rank 3 (+1).
3. $a_2 = 2$ (rank 2): seen 2, $\text{query}(2) = 0 \implies \text{inv} = 2 - 0 = 2$. Update rank 2 (+1).
4. $a_3 = 1$ (rank 1): seen 3, $\text{query}(1) = 0 \implies \text{inv} = 3 - 0 = 3$. Update rank 1 (+1).
Total Inversions: $0 + 1 + 2 + 3 = 6$. Matches $\binom{4}{2} = 6$ for reverse-sorted array!

### Step 9: Edge Cases & Guards
- **Empty Array ($N = 0$)**: 0 inversions.
- **Already Sorted Array**: Every element has $\text{query}(r) == \text{total\_seen}$, producing 0 inversions.
- **All Identical Elements**: Duplicate ranks return $0$ inversions because $\text{query}(r)$ includes identical values.
- **64-bit Overflow**: Return variable must be `long long` / 64-bit int.

### Step 10: Standard ISO C++20 Implementation
```cpp
// solutions/cpp/FENW-0001.cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cassert>

namespace fenw_0001 {

class FenwickTree {
private:
    int n;
    std::vector<int64_t> tree;

public:
    explicit FenwickTree(int size) : n(size), tree(size + 1, 0) {}

    // Adds delta to 1-based index i: O(log N)
    void update(int i, int64_t delta) {
        for (; i <= n; i += (i & -i)) {
            tree[i] += delta;
        }
    }

    // Computes prefix sum [1..i]: O(log N)
    int64_t query(int i) const {
        int64_t sum = 0;
        for (; i > 0; i -= (i & -i)) {
            sum += tree[i];
        }
        return sum;
    }

    // Computes range sum [l..r]: O(log N)
    int64_t query_range(int l, int r) const {
        if (l > r) return 0;
        return query(r) - query(l - 1);
    }
};

// Computes total inversions in an arbitrary sequence using coordinate compression and Fenwick Tree
int64_t count_inversions(const std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    if (n <= 1) return 0;

    // 1. Coordinate compression
    std::vector<int> sorted_unique = arr;
    std::sort(sorted_unique.begin(), sorted_unique.end());
    sorted_unique.erase(std::unique(sorted_unique.begin(), sorted_unique.end()), sorted_unique.end());

    int u = static_cast<int>(sorted_unique.size());
    FenwickTree bit(u);

    int64_t total_inversions = 0;

    // 2. Process stream
    for (int i = 0; i < n; ++i) {
        // Find 1-based rank
        auto it = std::lower_bound(sorted_unique.begin(), sorted_unique.end(), arr[i]);
        int rank = static_cast<int>(std::distance(sorted_unique.begin(), it)) + 1;

        // Elements seen so far: i
        // Elements <= arr[i]: query(rank)
        // Inversions contributed by arr[i]: elements > arr[i] seen earlier
        int64_t greater_count = i - bit.query(rank);
        total_inversions += greater_count;

        // Insert current element into BIT
        bit.update(rank, 1);
    }

    return total_inversions;
}

// Differential quadratic oracle for verification
int64_t reference_count_inversions(const std::vector<int>& arr) {
    int64_t inv = 0;
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] > arr[j]) {
                inv++;
            }
        }
    }
    return inv;
}

} // namespace fenw_0001
```

### Step 11: Python 3.12+ Implementation
```python
# solutions/python/FENW-0001.py
from typing import List
import bisect

class FenwickTree:
    def __init__(self, size: int):
        self.n = size
        self.tree: List[int] = [0] * (size + 1)

    def update(self, i: int, delta: int) -> None:
        """Adds delta to 1-based index i: O(log N)."""
        while i <= self.n:
            self.tree[i] += delta
            i += (i & -i)

    def query(self, i: int) -> int:
        """Computes prefix sum [1..i]: O(log N)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= (i & -i)
        return s

    def query_range(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)

def count_inversions(arr: List[int]) -> int:
    """
    Computes total inversions in arr via coordinate compression and Fenwick Tree.
    Runs in strictly O(N log N) time and O(N) space.
    """
    n = len(arr)
    if n <= 1:
        return 0

    sorted_unique = sorted(set(arr))
    u = len(sorted_unique)
    bit = FenwickTree(u)

    total_inversions = 0

    for i, val in enumerate(arr):
        # 1-based rank via binary search
        rank = bisect.bisect_left(sorted_unique, val) + 1
        greater_count = i - bit.query(rank)
        total_inversions += greater_count
        bit.update(rank, 1)

    return total_inversions

def reference_count_inversions(arr: List[int]) -> int:
    """Quadratic oracle for testing."""
    inv = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv += 1
    return inv
```

### Step 12: Asymptotic & Microarchitectural Complexity
- **Time Complexity**:
  - Sorting and Deduplication: $\Theta(N \log N)$.
  - Streaming Phase: $N$ iterations, each doing binary search ($O(\log U)$) and BIT query/update ($O(\log U)$).
  - Total Time: $\Theta(N \log N)$.
- **Space Complexity**: Strictly $\Theta(N)$ auxiliary memory for the flat BIT buffer and unique rank array. Zero node pointers!
- **Microarchitectural Behavior**: Flat array accesses with power-of-two strides exhibit exceptional cache behavior, making Fenwick Trees up to $4\times$ faster than pointer-based Segment Trees in practice.

### Step 13: Failure Modes & Anti-Patterns
- **0-Index Bitwise Trap**: If an index is $0$, `0 & -0` evaluates to $0$. Executing `i -= (i & -i)` from $0$ results in an infinite loop! Fenwick Trees must always operate on **1-based indices** ($1 \le i \le N$).
- **Signed 32-bit Inversion Overflow**: For $N = 2 \times 10^5$, maximum inversions can reach $2 \times 10^{10}$, overflowing 32-bit signed integers (`INT_MAX` $\approx 2.14 \times 10^9$). Inversion counters must be 64-bit integers.

### Step 14: Dual-Language Nuance & Idioms
- **C++20**: Utilizing `std::unique` with `erase` compresses ranges in-place with zero reallocation, while `int64_t` avoids arithmetic overflow.
- **Python 3.12**: `sorted(set(arr))` creates a sorted unique lookup list in one concise C-accelerated call, and Python handles arbitrary-precision integers automatically.

### Step 15: Unit Tests & Verification Fixtures
Differential testing verifies:
1. Reverse sorted arrays return exactly $\frac{N(N-1)}{2}$.
2. Sorted arrays return 0.
3. Arrays with heavy duplicate values handle equality correctly (no false inversions).
4. Randomized differential fuzz testing against the quadratic oracle verifies equivalence over 50 randomized arrays.

### Step 16: Reader Engineering Challenges
1. **Range-Update Point-Query BIT**: Combine a difference array with a Fenwick Tree to support range updates `update_range(l, r, delta)` and point queries `query_point(i)` in $O(\log N)$ time.
2. **Range-Update Range-Query BIT**: Use two Fenwick Trees to support both range additions and range sum queries simultaneously in $O(\log N)$ time.

---

## 21.8 Chapter Summary & Dyadic Mental Model

The Fenwick Tree is a triumph of arithmetic minimalism:
- By decomposing integers into powers of two via `i & -i`, it assigns responsibility for dyadic intervals to flat array cells.
- It solves the dynamic prefix sum dilemma in $O(\log N)$ time with **zero pointer overhead**, outperforming Segment Trees in raw wall-clock latency for prefix-dominated workloads.
