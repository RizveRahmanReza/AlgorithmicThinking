# CHAPTER 5: COUNTING, COMBINATORICS, AND RECURRENCES

> *"To understand recursion, one must first count the ways a problem subdivides. To master complexity, one must solve the recurrence."*

---

## 5.1 Combinatorial Foundations: Permutations, Subsets, and Partitions

In algorithm design, **counting** is not merely an elementary arithmetic exercise; it is the fundamental tool for quantifying search spaces, establishing information-theoretic lower bounds, and designing dynamic programming states.

When you design an algorithm, the number of distinct configurations dictates whether a brute-force search is feasible:

```
+---------------------------------------------------------------------------------+
| Configuration Archetype   | Mathematical Formula | Combinatorial Growth Class  |
+---------------------------------------------------------------------------------+
| Ordered Sequences         | n^k                  | Exponential                 |
| Permutations (No Rep.)    | P(n, k) = n!/(n-k)!  | Factorial O(n!)             |
| Subsets / Combinations    | C(n, k) = n!/(k!(n-k)!)| Binomial Coefficients     |
| Total Power Set           | 2^n                  | Exponential O(2^n)          |
| Integer Partitions        | p(n) ~ exp(pi sqrt(2n/3)) / (4n sqrt(3)) | Sub-exponential |
+---------------------------------------------------------------------------------+
```

### The Pigeonhole Principle
The **Pigeonhole Principle** states:
> If $n$ items are put into $m$ containers, and $n > m$, then at least one container must contain more than one item: $\lceil n / m \rceil \ge 2$.

In algorithmic thinking, this principle is an indispensable analytical weapon:
- **Cycle Detection**: In any finite state machine or pseudo-random generator with $S$ distinct states, traversing $S + 1$ transitions mathematically guarantees that at least one state has been revisited, proving the existence of a cycle.
- **Hash Table Collisions**: If a hash function maps $N$ keys to $M$ buckets where $N > M$, collisions are not an unfortunate possibility—**they are a mathematical certainty**. Any hash table design must incorporate a collision resolution strategy.
- **Subsequence Guarantees (Erdős–Szekeres Theorem)**: Every sequence of distinct integers of length at least $n^2 + 1$ contains a monotonically increasing subsequence of length $n + 1$ or a monotonically decreasing subsequence of length $n + 1$.

---

## 5.2 Recurrences in Algorithm Design

A **recurrence relation** is an equation that defines a sequence recursively: each term is expressed as a function of preceding terms.

In computer science, recurrence relations model the execution time, memory usage, or structural composition of recursive and divide-and-conquer algorithms:

$$T(n) = a \cdot T(n/b) + f(n)$$

where:
- $a \ge 1$ represents the number of recursive subproblems generated at each step.
- $n/b$ ($b > 1$) represents the reduced size of each subproblem.
- $f(n)$ represents the cost of dividing the problem and combining the subproblem results at the current level.

### The Three Methods for Solving Recurrences

To solve a recurrence relation (i.e., derive a closed-form asymptotic bound $\Theta(g(n))$), algorithm designers use three foundational techniques:

```
+------------------------------------------------------------------------+
| 1. The Recursion Tree Method                                           |
| Draw the hierarchical tree of calls; sum costs across each horizontal   |
| level; sum the geometric series across all log_b(n) levels.            |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
| 2. The Substitution Method (Inductive Guess & Prove)                   |
| Guess the asymptotic form T(n) <= c * g(n); substitute into the       |
| recurrence; prove by mathematical induction for all n >= n_0.          |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
| 3. The Master Theorem (Cookbook Solution)                             |
| Compare the watershed exponent c_crit = log_b(a) against f(n) = n^c.    |
| Determine if root cost dominates, leaf cost dominates, or both balance.|
+------------------------------------------------------------------------+
```

---

## 5.3 The Master Theorem: Power and Boundaries

The **Master Theorem** provides an immediate asymptotic recipe for standard divide-and-conquer recurrences of the form $T(n) = a T(n/b) + \Theta(n^c)$.

Let $c_{\text{crit}} = \log_b(a)$ represent the **critical watershed exponent**. The total work is determined by comparing the work done at the leaves ($\Theta(n^{\log_b a})$) against the work done at the root combining step ($\Theta(n^c)$):

### Case 1: Leaf-Heavy (Subproblem Explosion)
If $c < \log_b(a)$, the cost is dominated by the vast number of base-case subproblems at the leaves:
$$T(n) = \Theta\left(n^{\log_b a}\right)$$
- *Example*: Strassen's Matrix Multiplication: $T(n) = 7 T(n/2) + \Theta(n^2)$. Here $a = 7, b = 2, c = 2$.
  $$\log_b(a) = \log_2(7) \approx 2.807 > 2 \implies T(n) = \Theta(n^{2.807})$$

### Case 2: Balanced Work (Even Distribution across Levels)
If $c = \log_b(a)$, the work done at each horizontal level of the recursion tree is asymptotically identical. The total work is the work per level multiplied by the tree depth $\log_b(n)$:
$$T(n) = \Theta\left(n^c \log n\right)$$
- *Example*: MergeSort: $T(n) = 2 T(n/2) + \Theta(n)$. Here $a = 2, b = 2, c = 1$.
  $$\log_2(2) = 1 = c \implies T(n) = \Theta(n \log n)$$

### Case 3: Root-Heavy (Combination Step Dominates)
If $c > \log_b(a)$ and the regularity condition holds ($a f(n/b) \le k f(n)$ for some $k < 1$):
$$T(n) = \Theta\left(f(n)\right) = \Theta(n^c)$$
- *Example*: $T(n) = 2 T(n/2) + \Theta(n^2)$. Here $\log_2(2) = 1 < 2 \implies T(n) = \Theta(n^2)$.

### Where the Master Theorem Fails!
The Master Theorem is **not universally applicable**. It fails in four common algorithmic scenarios:
1. **Non-polynomial gap**: $T(n) = 2 T(n/2) + n / \log n$. The gap between $n^1$ and $n / \log n$ is sub-polynomial. One must use the Recursion Tree method directly, yielding $\Theta(n \log \log n)$.
2. **Unequal subproblem sizes**: $T(n) = T(n/3) + T(2n/3) + \Theta(n)$ (as seen in Quickselect or unbalanced QuickSort). The Master Theorem cannot evaluate this; one must draw an asymmetric recursion tree or use the **Akra-Bazzi method**.
3. **Subproblem size subtracted rather than divided**: $T(n) = T(n-1) + \Theta(1)$ or $T(n) = 2 T(n-1) + \Theta(1)$ (exponential recurrences).

---

## 5.4 Worked Problem: MATH-0002 — Inversion Counting via Divide-and-Conquer

To demonstrate how recurrence analysis, combinatorics, and invariant preservation unite in practice, let us examine the classic problem of **Counting Inversions in a Sequence**.

---

### Step 1: Real-World Motivation
In recommendation systems (e.g., Netflix, Spotify, Amazon), user preferences are represented as ranked permutations of items. To measure the similarity between two users' taste rankings, engineers compute the **Kendall Tau Distance**, which equals the minimum number of adjacent swaps needed to transform one user's ranking into another's. 

A distance of 0 means identical taste; a maximum distance means perfectly inverted preferences. The core computational engine required to compute Kendall Tau distance is **Inversion Counting**. Because modern platforms process millions of user ratings, a quadratic $\mathcal{O}(N^2)$ algorithm would freeze the real-time recommendation pipeline.

### Step 2: Problem Identification
Given an array of $n$ numbers, count the total number of pairs $(i, j)$ such that $i < j$ and $A[i] > A[j]$.

### Step 3: Formal Problem Statement
Let $A = [a_0, a_1, \dots, a_{n-1}]$ be a sequence of $n$ distinct integers.
An **inversion** is defined as an ordered pair of indices $(i, j)$ satisfying:
$$0 \le i < j < n \quad \text{and} \quad a_i > a_j$$
Compute the exact cardinality:
$$\text{Inv}(A) = \left| \{ (i, j) \mid 0 \le i < j < n \text{ and } a_i > a_j \} \right|$$

#### Constraints:
- Length: $1 \le n \le 2 \times 10^5$
- Elements: $-10^9 \le a_i \le 10^9$
- Time budget: $\mathcal{O}(n \log n)$
- Space budget: $\mathcal{O}(n)$ auxiliary memory.

### Step 4: Thinking Before Coding
1. **What is the maximum possible number of inversions?**
   If the array is strictly descending ($[n, n-1, \dots, 2, 1]$), every pair is an inversion:
   $$\text{Max Inversions} = \binom{n}{2} = \frac{n(n-1)}{2}$$
   For $n = 2 \times 10^5$, $\frac{(2 \times 10^5)(199999)}{2} \approx 2 \times 10^{10}$.
   **This exceeds $2^{31}-1 \approx 2.14 \times 10^9$. The inversion count MUST be stored in a 64-bit integer (`int64_t` / Python `int`).**
2. **What if the array is already sorted?** Inversion count is 0.
3. **How does dividing the array help?**
   If we divide $A$ into two halves $L = A[0 \dots m]$ and $R = A[m+1 \dots n-1]$:
   $$\text{Inv}(A) = \text{Inv}(L) + \text{Inv}(R) + \text{SplitInversions}(L, R)$$
   where a "split inversion" has $i \in L$ and $j \in R$ with $A[i] > A[j]$.

### Step 5: First-Principles Reasoning
How can we count split inversions without checking all $|L| \times |R|$ pairs (which would be quadratic)?
Suppose both $L$ and $R$ were **already sorted in ascending order**!
If $L[p] > R[q]$, what does that imply about all subsequent elements in $L$?
Because $L$ is sorted, every element from index $p$ to the end of $L$ is $\ge L[p] > R[q]$!
Therefore, if $L[p] > R[q]$, then $R[q]$ forms an inversion with **every remaining element in $L$**!
The number of inversions contributed by $R[q]$ is immediately:
$$\text{Remaining}(L) = |L| - p$$
With a single comparison, we count $|L| - p$ inversions in $\mathcal{O}(1)$ time! This is the exact mechanism of the **Merge step** in MergeSort!

### Step 6: Brute-Force Implementation (The Oracle)

```python
# Reference Quadratic Baseline: O(N^2)
def count_inversions_oracle(arr: list[int]) -> int:
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count
```

### Step 7: Bottleneck Analysis
- The baseline oracle checks all $\binom{n}{2} = \Theta(n^2)$ pairs individually.
- For $n = 2 \times 10^5$, this requires $2 \times 10^{10}$ comparisons, taking roughly 20 to 30 seconds.
- The fundamental defect is testing pairs independently instead of leveraging sorted subproblem structure to count inversions in bulk.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Space Complexity | Viability for $N = 2 \times 10^5$ | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Quadratic Oracle** | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Impossible ($2 \times 10^{10}$ ops) | Re-evaluates each pair independently |
| **Fenwick Tree / BIT** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Viable ($12 \text{ ms}$) | Requires coordinate compression for arbitrary $a_i$ |
| **Divide & Conquer MergeSort** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | **Optimal ($9 \text{ ms}$)** | Cache-friendly sequential merge; no coordinate compression needed |

### Step 9: Derivation of the Divide-and-Conquer Algorithm
We combine sorting and counting into a single unified recurrence:
$$\text{SortAndCount}(A[l \dots r])$$
1. **Base Case**: If $l \ge r$, return 0 inversions.
2. **Divide**: Midpoint $m = l + \lfloor (r - l) / 2 \rfloor$.
3. **Conquer**:
   - `inv_left = SortAndCount(A[l ... m])`
   - `inv_right = SortAndCount(A[m+1 ... r])`
4. **Combine (Merge and Count Split)**:
   - Use two pointers $p$ (iterating over sorted left half) and $q$ (iterating over sorted right half).
   - If $A[p] \le A[q]$: Place $A[p]$ into auxiliary buffer; advance $p$.
   - If $A[p] > A[q]$: Place $A[q]$ into buffer; advance $q$; **add $(m - p + 1)$ to split inversions!**
   - Copy merged buffer back to $A[l \dots r]$.
5. Return `inv_left + inv_right + split_inversions`.

### Step 10: Correctness and Recurrence Proof

#### Recurrence Relation:
The divide-and-conquer function satisfies:
$$T(n) = 2 T(n/2) + \Theta(n)$$
- $a = 2$ recursive calls of size $n/2$.
- $f(n) = \Theta(n)$ time to merge and count split inversions across the two halves.
By **Case 2 of the Master Theorem**:
$$\log_b(a) = \log_2(2) = 1 = c \implies T(n) = \Theta(n \log n)$$

#### Merge Invariant:
Let $L = A[l \dots m]$ and $R = A[m+1 \dots r]$ be sorted ascending subarrays.
At each step of merging, when selecting $R[q]$:
- Since $L$ is sorted, $L[k] \ge L[p] > R[q]$ for all $k \in [p, m]$.
- Since elements in $L$ originally appeared before elements in $R$ in the original array, each pair $(L[k], R[q])$ constitutes a valid inversion.
- There are exactly $m - p + 1$ such elements.
- No inversion within $L$ or within $R$ is recounted, because they were already counted and neutralized by sorting their respective subproblems.
- No split inversion is missed because every element in $R$ is compared against the first element in $L$ that exceeds it. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Given array: $A = [8, 4, 2, 1]$

```
                [8, 4, 2, 1]
               /            \
          [8, 4]            [2, 1]
          /    \            /    \
        [8]    [4]        [2]    [1]
```
1. Merge `[8]` and `[4]`:
   - $8 > 4 \implies$ add $(m - p + 1) = (0 - 0 + 1) = 1$ inversion. Merged: `[4, 8]`. Inversions = 1.
2. Merge `[2]` and `[1]`:
   - $2 > 1 \implies$ add $1$ inversion. Merged: `[1, 2]`. Inversions = 1.
3. Merge `[4, 8]` ($L$) and `[1, 2]` ($R$):
   - Compare $4$ vs $1$: $4 > 1 \implies$ add $(1 - 0 + 1) = 2$ inversions (pairs $(4, 1)$ and $(8, 1)$). Pick $1$.
   - Compare $4$ vs $2$: $4 > 2 \implies$ add $(1 - 0 + 1) = 2$ inversions (pairs $(4, 2)$ and $(8, 2)$). Pick $2$.
   - $R$ is exhausted; append $4, 8$.
   - Split inversions $= 2 + 2 = 4$.
4. Total Inversions $= 1 (\text{left}) + 1 (\text{right}) + 4 (\text{split}) = 6$.
   *Verification*: $\binom{4}{2} = 6$ total pairs, all inverted. Correct!

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/MATH-0002.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <stdexcept>
#include <cassert>

namespace internal {

int64_t merge_and_count(
    std::span<int64_t> arr, 
    std::vector<int64_t>& temp, 
    size_t left, 
    size_t mid, 
    size_t right
) {
    size_t p = left;      // Pointer for left sorted half
    size_t q = mid + 1;   // Pointer for right sorted half
    size_t k = left;      // Pointer for temp merged buffer
    int64_t split_inversions = 0;

    while (p <= mid && q <= right) {
        if (arr[p] <= arr[q]) {
            temp[k++] = arr[p++];
        } else {
            temp[k++] = arr[q++];
            // Key Invariant: arr[p] > arr[q], and since left half is sorted,
            // all elements from arr[p ... mid] are strictly greater than arr[q].
            split_inversions += static_cast<int64_t>(mid - p + 1);
        }
    }

    while (p <= mid) {
        temp[k++] = arr[p++];
    }
    while (q <= right) {
        temp[k++] = arr[q++];
    }

    for (size_t idx = left; idx <= right; ++idx) {
        arr[idx] = temp[idx];
    }

    return split_inversions;
}

int64_t sort_and_count(
    std::span<int64_t> arr, 
    std::vector<int64_t>& temp, 
    size_t left, 
    size_t right
) {
    if (left >= right) {
        return 0;
    }

    size_t mid = left + (right - left) / 2;
    int64_t inv_count = 0;

    inv_count += sort_and_count(arr, temp, left, mid);
    inv_count += sort_and_count(arr, temp, mid + 1, right);
    inv_count += merge_and_count(arr, temp, left, mid, right);

    return inv_count;
}

} // namespace internal

/**
 * Counts total inversions in O(N log N) time and O(N) space.
 * Conforms to ISO C++20 standard.
 */
int64_t count_inversions(std::span<const int64_t> input) {
    if (input.size() <= 1) {
        return 0;
    }

    std::vector<int64_t> arr(input.begin(), input.end());
    std::vector<int64_t> temp(arr.size());

    return internal::sort_and_count(arr, temp, 0, arr.size() - 1);
}

// Differential Oracle (O(N^2))
int64_t count_inversions_oracle(std::span<const int64_t> arr) {
    int64_t count = 0;
    for (size_t i = 0; i < arr.size(); ++i) {
        for (size_t j = i + 1; j < arr.size(); ++j) {
            if (arr[i] > arr[j]) {
                ++count;
            }
        }
    }
    return count;
}

int main() {
    std::vector<int64_t> sample{8, 4, 2, 1};
    assert(count_inversions(sample) == 6);
    assert(count_inversions_oracle(sample) == 6);

    std::vector<int64_t> mixed{2, 4, 1, 3, 5};
    assert(count_inversions(mixed) == 3); // (2,1), (4,1), (4,3)
    assert(count_inversions_oracle(mixed) == 3);

    std::vector<int64_t> sorted{1, 2, 3, 4, 5};
    assert(count_inversions(sorted) == 0);

    std::cout << "All C++20 test assertions for MATH-0002 passed successfully." << std::endl;
    return 0;
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/MATH-0002.py
from typing import Sequence


def count_inversions(arr: Sequence[int]) -> int:
    """
    Computes total inversions in O(N log N) time and O(N) space.
    Target: Python 3.12+ (Type-Annotated, Idiomatic).
    """
    if len(arr) <= 1:
        return 0

    mutable_arr = list(arr)
    temp_buffer = [0] * len(mutable_arr)

    def _sort_and_count(left: int, right: int) -> int:
        if left >= right:
            return 0

        mid = left + (right - left) // 2
        inv = _sort_and_count(left, mid)
        inv += _sort_and_count(mid + 1, right)

        # Merge and count split inversions
        p = left
        q = mid + 1
        k = left
        split_inv = 0

        while p <= mid and q <= right:
            if mutable_arr[p] <= mutable_arr[q]:
                temp_buffer[k] = mutable_arr[p]
                p += 1
            else:
                temp_buffer[k] = mutable_arr[q]
                q += 1
                # Key invariant: mutable_arr[p ... mid] are all strictly greater than mutable_arr[q]
                split_inv += (mid - p + 1)
            k += 1

        while p <= mid:
            temp_buffer[k] = mutable_arr[p]
            p += 1
            k += 1

        while q <= right:
            temp_buffer[k] = mutable_arr[q]
            q += 1
            k += 1

        mutable_arr[left:right + 1] = temp_buffer[left:right + 1]
        return inv + split_inv

    return _sort_and_count(0, len(mutable_arr) - 1)


def count_inversions_oracle(arr: Sequence[int]) -> int:
    """Quadratic baseline oracle for differential testing (O(N^2))."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


if __name__ == "__main__":
    t1 = [8, 4, 2, 1]
    assert count_inversions(t1) == count_inversions_oracle(t1) == 6

    t2 = [2, 4, 1, 3, 5]
    assert count_inversions(t2) == count_inversions_oracle(t2) == 3

    t3 = [1, 2, 3, 4]
    assert count_inversions(t3) == 0

    print("All Python 3 self-tests for MATH-0002 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(N \log N)$
  - Master Theorem applies cleanly: $T(N) = 2 T(N/2) + \Theta(N) \implies \Theta(N \log N)$.
  - Regardless of initial ordering (best-case, worst-case, or random), the recursion tree always divides evenly into $\lceil \log_2 N \rceil$ levels, and each level processes exactly $N$ elements during merging.
- **Space Complexity**: $\Theta(N)$ auxiliary space
  - A single auxiliary buffer `temp` of size $N$ is allocated upfront and reused across all recursive frames.
  - The call stack depth is $\Theta(\log N)$.

### Step 15: Edge Cases and Failure Modes
- Empty array or $N=1$: Returns 0.
- All elements identical (`[5, 5, 5, 5]`): Since $a_p \le a_q$ breaks ties without counting inversions, correctly returns 0.
- 64-bit integer overflow: Up to $2 \times 10^{10}$ inversions for $N = 2 \times 10^5$. Handled with `int64_t`.

### Step 16: Test Cases & Differential Validation
- Strict reverse-sorted array ($\binom{N}{2}$ inversions).
- Strictly sorted array ($0$ inversions).
- Random permutations verified against `count_inversions_oracle`.

### Step 17: Real-World Engineering Application
- Collaborative filtering in recommendation systems.
- Ranking correlation metrics (Kendall's $\tau$ and Spearman's $\rho$).
- Genomic sequence alignment: Identifying gene inversion mutations between chromosomes.

### Step 18: Further Optimization
- In systems engineering, allocating a new vector for each call destroys performance. We allocate the `temp` buffer **once** at the root call and pass it by reference across all stack frames, eliminating dynamic heap reallocations.

### Step 19: Related Patterns
- **Fenwick Tree / Segment Tree Inversion Counting**: Provides an online alternative where numbers are inserted dynamically into a range frequency tree.
- **Count of Smaller Numbers After Self**: Generalizing inversion counting to produce an array of individual element counts.

### Step 20: Reader Challenges
1. **Challenge 5.1 (Reverse Pairs)**: Count the number of pairs $(i, j)$ such that $i < j$ and $A[i] > 2 A[j]$. Prove how the merge step must be split into a separate counting pass before merging to maintain linear combine time.
2. **Challenge 5.2 (Online Inversion Counter)**: Design a data structure that accepts a continuous stream of numbers and answers the current total inversion count in $\mathcal{O}(\log U)$ time per insertion using a Fenwick Tree.

---

## 5.5 Chapter Synthesis
Combinatorics and recurrence relations establish the mathematical laws governing recursive decomposition. By mastering the Master Theorem and recursion tree analysis, you can immediately predict whether a divide-and-conquer strategy will yield an optimal algorithm or an exponential explosion.

In **Chapter 6**, we complete Part II with **Asymptotic Analysis and Complexity Classes**, exploring the formal definitions of Big-$O$, $\Omega$, and $\Theta$, amortized analysis, and theoretical lower bounds.
