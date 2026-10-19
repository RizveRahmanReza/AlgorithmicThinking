# CHAPTER 13: SEARCH PARADIGMS AND BINARY SEARCH ON ANSWER SPACE

> *"Binary search is not an array lookup algorithm; it is the universal reduction of a monotonic boolean predicate across an ordered domain."*

---

## 13.1 Deconstructing Binary Search: Beyond Sorted Arrays

In introductory programming courses, binary search is almost universally introduced as a search over a sorted array: *"Given a sorted list of numbers, find index $i$ such that $A[i] == T$."*

This pedagogical framing is tragically narrow. It leads engineers to miss the true power of the technique.

### The Universal Predicate Formulation
Let $\mathcal{D}$ be an ordered search domain (which can be a discrete range of integers $[L, R]$, an array of elements, or a continuous interval of real numbers $[a, b]$).
Let $P: \mathcal{D} \to \{0, 1\}$ be a **Boolean Predicate Function** evaluated on candidate values in the domain.

Binary search is mathematically applicable **if and only if the predicate $P$ is Monotonic across $\mathcal{D}$**:

$$\forall x, y \in \mathcal{D}, \quad x \le y \implies P(x) \le P(y) \quad (\text{or } P(x) \ge P(y))$$

When monotonicity holds, the entire domain $\mathcal{D}$ partitions cleanly into two contiguous regimes:

```
Search Domain:  [ L,  L+1,  L+2,  ...,  M-1,  |  M,  M+1,  ...,  R ]
Predicate P(x):   0     0     0    ...    0    |  1    1   ...   1
                                               ^
                                    Boundary Threshold x*
```

The objective of Binary Search is **never merely to find an element**; it is to locate the **Phase Transition Boundary ($x^*$)** where $P(x)$ transitions from False ($0$) to True ($1$)!

Because each evaluation of $P(m)$ at the midpoint $m = \lfloor (L + R) / 2 \rfloor$ determines whether the threshold lies to the left or right, the search space halves at every step:
$$|\mathcal{D}_{k+1}| = \frac{|\mathcal{D}_k|}{2}$$
The algorithm terminates in exactly $\lceil \log_2 |\mathcal{D}| \rceil$ predicate evaluations.

---

## 13.2 The Anatomy of Boundary Invariants: Lower and Upper Bounds

The primary source of bugs in binary search (infinite loops, off-by-one errors) is ambiguous boundary definitions.
An algorithmic thinker operates with **strict boundary invariants**:

```
+---------------------------------------------------------------------------------+
| Variant          | Objective                                  | Invariant       |
+---------------------------------------------------------------------------------+
| Exact Match      | Find i such that A[i] == target            | Range [L, R]    |
| Lower Bound      | Find smallest i such that A[i] >= target   | A[R] is always 1|
| Upper Bound      | Find smallest i such that A[i] > target    | A[R] is always 1|
| Max True Search  | Find largest x such that P(x) == True      | P(L) is always 1|
| Min True Search  | Find smallest x such that P(x) == True     | P(R) is always 1|
+---------------------------------------------------------------------------------+
```

### The Safe Midpoint Formula
In 32-bit systems, the textbook formula `mid = (L + R) / 2` causes integer overflow when $L + R > 2^{31} - 1$, producing a negative index and crashing with a segmentation fault.
We strictly enforce the overflow-safe midpoint:
$$\text{mid} = L + \left\lfloor \frac{R - L}{2} \right\rfloor$$

---

## 13.3 The "Binary Search on Answer" Paradigm

When faced with an optimization problem of the form:
$$\text{Find } \min (\text{Cost}) \quad \text{or} \quad \max (\text{Capacity})$$
the direct optimization path is often difficult or mathematically intractable.

However, the **decision problem** is frequently trivial:
> *"Given a fixed candidate cost $C$, is it possible to achieve the task without exceeding cost $C$?"*

If answering this yes/no feasibility question is monotonic (i.e., if it is feasible with cost $C$, it is obviously feasible with any cost $C' > C$), we can **Binary Search on the Answer Space itself**!

This paradigm converts complex optimization problems into simple greedy feasibility checks executed in $\mathcal{O}(\text{Feasibility}(N) \times \log(\text{Range}))$.

---

## 13.4 Worked Problem: SRCH-0001 — Capacity Allocation via Binary Search on Answer Space

We now apply the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify: **The Minimal Conveyor Ship Capacity Problem**.

---

### Step 1: Real-World Motivation
In automated logistics fulfillment hubs (Amazon robotics, container shipping ports), packages of varying weights arrive sequentially on a continuous conveyor belt. A fleet of cargo ships (or daily delivery trucks) is available to transport the packages. The shipping schedule dictates that all packages must be shipped within a strict deadline of $D$ days. 

Due to conveyor layout, packages must be loaded in the **exact sequential order** in which they arrive. The port authority must determine the **minimum daily weight capacity $C$** of the ships such that all packages are transported within $D$ days. Setting $C$ too high burns unnecessary fuel; setting $C$ too low violates delivery SLAs.

### Step 2: Problem Identification
Given an array of package weights and a maximum allowed days $D$, find the minimum integer capacity $C$ such that a greedy sequential partition of the array into contiguous subarrays each summing to at most $C$ requires at most $D$ partitions.

### Step 3: Formal Problem Statement
Let $W = [w_0, w_1, \dots, w_{n-1}]$ be an array of $n$ positive integer weights ($w_i \in \mathbb{Z}_{> 0}$).
Given an integer deadline $D \ge 1$:
Find the minimal integer $C \in \mathbb{Z}_{> 0}$ such that there exists a partition of $W$ into $k \le D$ contiguous subarrays $S_1, S_2, \dots, S_k$ satisfying:
$$\forall j \in [1, k], \quad \sum_{w \in S_j} w \le C$$

#### Constraints:
- Array length: $1 \le n \le 10^6$
- Days: $1 \le D \le n$
- Individual weights: $1 \le w_i \le 10^9$
- Total weight sum: $\sum w_i \le 10^{15}$
- Time budget: $\mathcal{O}(n \log(\sum w_i))$
- Auxiliary space budget: $\mathcal{O}(1)$

### Step 4: Thinking Before Coding
1. **What is the absolute minimum possible capacity ($L$)?**
   No package can be split. Therefore, the ship must be able to carry the single heaviest package!
   $$L = \max_{0 \le i < n} w_i$$
2. **What is the absolute maximum possible capacity ($R$)?**
   If $D = 1$, a single ship must carry every single package in one day!
   $$R = \sum_{i=0}^{n-1} w_i \le 10^{15}$$
   *Notice the scale*: $10^{15}$ exceeds 32-bit signed integers. **All capacity variables and sums must be 64-bit integers (`int64_t`).**
3. **Is the feasibility predicate monotonic?**
   Let $P(C)$ be the boolean predicate: *"Can all packages be shipped within $D$ days with capacity $C$?"*
   - If a ship of capacity $C$ can ship all packages within $D$ days, then a larger ship of capacity $C' > C$ can obviously do so as well (it has strictly more room per day).
   - If capacity $C$ cannot ship within $D$ days, no smaller capacity $C'' < C$ can possibly do so.
   - Therefore, $P(C)$ is **strictly monotonic** ($0, 0, \dots, 0, 1, 1, \dots, 1$). Binary search is guaranteed to succeed!

### Step 5: First-Principles Reasoning (The Greedy Feasibility Predicate)
Given a candidate capacity $C$:
How do we determine the minimum number of days needed?
To minimize days, each day should pack as much weight as physically possible without exceeding $C$!
We iterate through $W$ sequentially:
- Accumulate `current_day_weight += w_i`.
- If `current_day_weight + w_i > C`: we must start a new day (`days_used++`, `current_day_weight = w_i`).
- If `days_used > D`: return `False` immediately.
- If all packages are packed with `days_used <= D`: return `True`.

This greedy simulation takes exactly $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ space!

### Step 6: Brute-Force Implementation (The Linear Search Oracle)

```python
# Reference Baseline: Linear Search testing C = max(w) upwards (O(n * Range))
def ship_within_days_oracle(weights: list[int], D: int) -> int:
    def can_ship(capacity: int) -> bool:
        days = 1
        current = 0
        for w in weights:
            if current + w > capacity:
                days += 1
                current = w
            else:
                current += w
        return days <= D

    C = max(weights)
    while not can_ship(C):
        C += 1
    return C
```

### Step 7: Bottleneck Analysis
- The baseline linear search increments $C$ by 1 until feasibility is met.
- The search range is $R - L = \sum w_i - \max(w_i) \approx 10^{15}$.
- Testing each $C$ requires $\Theta(n)$ operations.
- Total operations for linear search: $\Theta(n \times 10^{15}) \approx 10^{21}$ operations $\implies$ **Hundreds of years!**
- Binary search evaluates $\lceil \log_2(10^{15}) \rceil \approx 50$ midpoints.
- Total operations for binary search: $50 \times n \approx 50 \times 10^6 \approx 5 \times 10^7$ operations $\implies$ **$0.02$ seconds!**

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Auxiliary Space | Feasibility for $\sum W = 10^{15}$ |
| :--- | :--- | :--- | :--- |
| **Linear Search Oracle** | $\mathcal{O}(n \cdot \sum W)$ | $\mathcal{O}(1)$ | Impossible ($10^{21}$ ops) |
| **Dynamic Programming** | $\mathcal{O}(n^2 \cdot D)$ | $\mathcal{O}(n \cdot D)$ | Impossible ($10^{12}$ ops; OOM) |
| **Binary Search on Answer** | $\mathcal{O}(n \log(\sum W))$ | $\mathcal{O}(1)$ | **Optimal ($15 \text{ ms}$)** |

### Step 9: Derivation of the Binary Search Invariant
We maintain the invariant on search range $[L, R]$:
- $L$: The current known lower bound where capacity might or might not be feasible.
- $R$: A known **feasible capacity** ($P(R) == \text{True}$).

```
Loop while L < R:
    mid = L + (R - L) / 2
    If can_ship(mid) == True:
        R = mid      // mid is feasible; optimal answer is <= mid
    Else:
        L = mid + 1  // mid is infeasible; optimal answer must be >= mid + 1

Termination:
When L == R, L is the exact minimum feasible capacity!
```

### Step 10: Correctness Proof

#### Invariant:
At the start of each iteration:
1. The optimal minimal capacity $C^*$ lies within the closed interval $[L, R]$.
2. $R$ is provably feasible ($P(R) = \text{True}$).
3. All values strictly smaller than $L$ are provably infeasible ($P(x) = \text{False}$ for all $x < L$).

#### Base Case:
- $L = \max(w_i)$: Any capacity $< \max(w_i)$ cannot even load the largest single package; thus all $x < L$ are infeasible.
- $R = \sum w_i$: Can ship everything in 1 day $\le D$, so $P(R) = \text{True}$.
The invariant holds.

#### Maintenance:
At each iteration with $L < R$:
- `mid` is chosen in $[L, R-1]$.
- If `can_ship(mid) == True`: By monotonicity, all $x \ge \text{mid}$ are feasible. The minimal feasible answer could be `mid` or smaller. Setting $R = \text{mid}$ preserves $C^* \in [L, R]$ and keeps $P(R) = \text{True}$.
- If `can_ship(mid) == False`: By monotonicity, all $x \le \text{mid}$ are infeasible. Thus $C^* \ge \text{mid} + 1$. Setting $L = \text{mid} + 1$ preserves the invariant.
- In both cases, the search space $R - L$ strictly decreases, guaranteeing termination.

#### Termination:
When $L == R$, the interval has collapsed to a single integer. By the invariant, $C^*$ is in $[L, R]$, so $C^* = L = R$. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Input: $W = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]$, $D = 5$.
$L = \max(W) = 10$, $R = \sum W = 55$.

| Iteration | $L$ | $R$ | `mid` | Days Needed for `mid` | Feasible ($\le 5$)? | New Range |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 10 | 55 | 32 | $[1..7]=28, [8..10]=27 \implies 2 \text{ days}$ | True ($\le 5$) | $R \leftarrow 32$ |
| 2 | 10 | 32 | 21 | $[1..5]=15, [6..7]=13, [8..9]=17, [10] \implies 4 \text{ days}$ | True ($\le 5$) | $R \leftarrow 21$ |
| 3 | 10 | 21 | 15 | $[1..5]=15, [6..7]=13, [8], [9], [10] \implies 5 \text{ days}$ | **True ($\le 5$)** | $R \leftarrow 15$ |
| 4 | 10 | 15 | 12 | $[1..4]=10, [5..6]=11, [7], [8], [9], [10] \implies 6 \text{ days}$ | False ($6 > 5$) | $L \leftarrow 13$ |
| 5 | 13 | 15 | 14 | $[1..4]=10, [5..6]=11, [7], [8], [9], [10] \implies 6 \text{ days}$ | False ($6 > 5$) | $L \leftarrow 15$ |
| 6 | 15 | 15 | — | **$L == R \implies$ Terminate!** | — | **Answer = 15** |

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/SRCH-0001.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <numeric>
#include <algorithm>
#include <span>
#include <cassert>

namespace alg {

/**
 * Evaluates whether packages can be shipped within max_days using given capacity.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 */
bool can_ship_within_days(
    std::span<const int64_t> weights, 
    int64_t max_days, 
    int64_t capacity
) noexcept {
    int64_t days_used = 1;
    int64_t current_day_load = 0;

    for (int64_t w : weights) {
        if (current_day_load + w > capacity) {
            ++days_used;
            current_day_load = w;
            if (days_used > max_days) {
                return false;
            }
        } else {
            current_day_load += w;
        }
    }

    return true;
}

/**
 * Finds minimum ship capacity using Binary Search on Answer Space.
 * Complexity: O(N * log(Sum(W))) Time, O(1) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
int64_t ship_within_days(std::span<const int64_t> weights, int64_t max_days) {
    if (weights.empty() || max_days <= 0) {
        throw std::invalid_argument("Invalid weights or deadline.");
    }

    int64_t left = *std::max_element(weights.begin(), weights.end());
    int64_t right = std::accumulate(weights.begin(), weights.end(), int64_t{0});

    while (left < right) {
        int64_t mid = left + (right - left) / 2;

        if (can_ship_within_days(weights, max_days, mid)) {
            right = mid;      // mid is feasible, try smaller
        } else {
            left = mid + 1;   // mid is infeasible, must increase
        }
    }

    return left;
}

} // namespace alg

// Differential Linear Search Baseline Oracle
int64_t ship_within_days_oracle(std::span<const int64_t> weights, int64_t max_days) {
    int64_t cap = *std::max_element(weights.begin(), weights.end());
    while (!alg::can_ship_within_days(weights, max_days, cap)) {
        ++cap;
    }
    return cap;
}

int main() {
    std::vector<int64_t> t1{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto r1 = alg::ship_within_days(t1, 5);
    auto o1 = ship_within_days_oracle(t1, 5);
    assert(r1 == o1 && r1 == 15);

    std::vector<int64_t> t2{3, 2, 2, 4, 1, 4};
    auto r2 = alg::ship_within_days(t2, 3);
    auto o2 = ship_within_days_oracle(t2, 3);
    assert(r2 == o2 && r2 == 6);

    std::vector<int64_t> t3{1, 2, 3, 1, 1};
    auto r3 = alg::ship_within_days(t3, 4);
    assert(r3 == 3);

    std::cout << "All C++20 assertions for SRCH-0001 passed successfully." << std::endl;
    return 0;
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/SRCH-0001.py
from typing import Sequence


def can_ship_within_days(weights: Sequence[int], max_days: int, capacity: int) -> bool:
    """Evaluates feasibility of capacity under greedy allocation."""
    days_used = 1
    current_load = 0

    for w in weights:
        if current_load + w > capacity:
            days_used += 1
            current_load = w
            if days_used > max_days:
                return False
        else:
            current_load += w

    return True


def ship_within_days(weights: Sequence[int], max_days: int) -> int:
    """
    Finds minimum capacity using Binary Search on Answer Space.
    Target: Python 3.12+ (O(N * log(Sum(W))) Time, O(1) Auxiliary Space).
    """
    if not weights or max_days <= 0:
        raise ValueError("Invalid weights or max_days.")

    left = max(weights)
    right = sum(weights)

    while left < right:
        mid = left + (right - left) // 2

        if can_ship_within_days(weights, max_days, mid):
            right = mid
        else:
            left = mid + 1

    return left


def ship_within_days_oracle(weights: Sequence[int], max_days: int) -> int:
    """Linear search baseline oracle for differential testing."""
    cap = max(weights)
    while not can_ship_within_days(weights, max_days, cap):
        cap += 1
    return cap


if __name__ == "__main__":
    t1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    r1 = ship_within_days(t1, 5)
    o1 = ship_within_days_oracle(t1, 5)
    assert r1 == o1 == 15, f"Failed: {r1}"

    t2 = [3, 2, 2, 4, 1, 4]
    r2 = ship_within_days(t2, 3)
    o2 = ship_within_days_oracle(t2, 3)
    assert r2 == o2 == 6, f"Failed: {r2}"

    print("All Python 3 self-tests for SRCH-0001 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(N \cdot \log(\sum w_i - \max(w_i)))$
  - The search domain has size $U = \sum w_i$.
  - Binary search executes exactly $\lceil \log_2 U \rceil$ iterations.
  - In each iteration, `can_ship_within_days` iterates through all $N$ elements once ($\Theta(N)$ time).
  - For $N = 10^6$ and $\sum w_i = 10^{15}$, $\log_2(10^{15}) \approx 50$ iterations.
  - Total operations $\approx 50 \times 10^6 \approx 5 \times 10^7$ ops, easily finishing in $< 0.05$ seconds.
- **Space Complexity**: $\Theta(1)$ auxiliary memory. Only scalar 64-bit bounds (`left`, `right`, `mid`) are tracked.

### Step 15: Edge Cases and Failure Modes
- $D = 1$: Output is $\sum w_i$.
- $D = n$: Output is $\max(w_i)$.
- 64-bit overflow prevented by safe midpoint formula $L + (R - L) / 2$.

### Step 16: Test Cases & Validation Suite
- Standard distribution arrays.
- Minimum possible days ($D = 1$) and maximum days ($D = n$).
- Uniform weights (`[5, 5, 5, 5, 5]`).

### Step 17: Real-World Engineering Application
- Container shipping and freight optimization (FedEx, Maersk).
- Distributed batch job scheduling on compute clusters (Hadoop, Ray, Slurm).
- Memory partition sizing in video streaming transcoders.

### Step 18: Related Patterns
- **Koko Eating Bananas**: Binary search on eating speed ($K$).
- **Split Array Largest Sum**: Mathematically isomorphic problem on subarray sums.
- **Aggressive Cows / Painter's Partition**: Binary search on minimum distance / time.

### Step 19: Reader Challenges
1. **Challenge 13.1 (Continuous Real Binary Search)**: Solve the square root $\sqrt{x}$ or square division on continuous real numbers $\mathbb{R}$ to within $10^{-9}$ precision, proving the absolute epsilon termination condition $|R - L| < \epsilon$.
2. **Challenge 13.2 (Search in Rotated Sorted Array)**: Find an element in a sorted array that has been rotated by an unknown pivot in $\mathcal{O}(\log N)$ time, establishing the half-array monotonicity invariant.

---

## 13.5 Chapter Synthesis
Binary search is one of the most versatile weapons in algorithmic design. By generalizing from arrays to arbitrary monotonic boolean predicates, you can solve complex combinatorial optimization problems in logarithmic iterations.

In **Chapter 14**, we explore **Comparison Sorting and Linear-Time Sorting**, investigating QuickSort, MergeSort, HeapSort, Counting Sort, Radix Sort, and the information-theoretic sorting lower bounds.
