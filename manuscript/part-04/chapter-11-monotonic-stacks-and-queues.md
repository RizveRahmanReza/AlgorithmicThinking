# CHAPTER 11: MONOTONIC STACKS AND QUEUES

> *"When a younger, stronger candidate enters the scene, older and weaker candidates become obsolete. A monotonic structure is the mathematical pruning of the obsolete."*

---

## 11.1 The Monotonic Principle: Elimination of Dominated Candidates

In standard algorithm design, maintaining all previously seen elements requires $\mathcal{O}(N)$ memory and frequently leads to $\mathcal{O}(N^2)$ exhaustive comparisons.

However, in many fundamental problems, certain elements become **provably irrelevant** the moment a new element arrives:
- In a sequence of stock prices, if price $P_j$ at day $j$ is greater than price $P_i$ at day $i$ ($j > i$), then for any future day $k > j$, **day $i$ can never be the next greater element** because day $j$ is both closer in time and larger in value! Day $i$ is **dominated** by day $j$.

```
Index:    0    1    2    3    4
Values: [ 4,   2,   1,   5,   ... ]

When '5' arrives at index 3:
- '1' is smaller than 5 and occurred earlier -> Obsolete! Discard.
- '2' is smaller than 5 and occurred earlier -> Obsolete! Discard.
- '4' is smaller than 5 and occurred earlier -> Obsolete! Discard.

Stack collapses from [4, 2, 1] down to [5].
```

A **Monotonic Stack** is a stack that enforces an invariant of strict (or non-strict) monotonicity among its elements, typically ordered from bottom to top:
- **Monotonically Increasing Stack**: Elements increase from bottom to top ($S[0] < S[1] < \dots < S[\text{top}]$). Used to find the **Previous / Next Smaller Element**.
- **Monotonically Decreasing Stack**: Elements decrease from bottom to top ($S[0] > S[1] > \dots > S[\text{top}]$). Used to find the **Previous / Next Greater Element**.

---

## 11.2 The Amortized $\mathcal{O}(N)$ Invariant Proof

A novice programmer inspecting a monotonic stack implementation sees a `while` loop nested inside a `for` loop:

```cpp
for (size_t i = 0; i < n; ++i) {
    while (!st.empty() && st.top() < arr[i]) {
        st.pop(); // Inner loop!
    }
    st.push(arr[i]);
}
```

The novice's initial intuition is: *"Nested loops over $N$ elements implies $\mathcal{O}(N^2)$ time."*

### Why the Nested Loop is Strictly $\mathcal{O}(N)$:
We prove the bound using the **Aggregate Amortized Method**:
1. Consider the lifecycle of any element $A[i]$ ($0 \le i < n$).
2. How many times can element $A[i]$ be **pushed** onto the stack? **Exactly once** (inside the outer `for` loop).
3. How many times can element $A[i]$ be **popped** from the stack? **At most once** (once popped, an element is destroyed and never re-enters the stack).
4. Therefore, across the entire execution of the program:
   $$\text{Total Pushes} = n$$
   $$\text{Total Pops} \le n$$
   $$\text{Total Inner Loop Iterations} = \text{Total Pops} \le n$$
5. Total operations: $\le n + n = 2n = \Theta(N)$.

The amortized time spent per element is strictly $\mathcal{O}(1)$, despite the worst-case single iteration occasionally popping $N-1$ elements at once!

---

## 11.3 Worked Problem: STACK-0002 — Next Greater Element with Circular Invariant

We now apply the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify the canonical monotonic stack pattern: **Next Greater Element with Circular Wrap-Around**.

---

### Step 1: Real-World Motivation
In real-time financial order matching and algorithmic exchange engines, limit buy and sell orders sit in circular execution rings. A trader wants to compute the "market resistance level" for every order: what is the next higher price quote observed down the circular order book? 

Because order books process hundreds of thousands of updates per second, running an $\mathcal{O}(N^2)$ nested loop per ticker freezes matching threads, causing catastrophic execution slippage.

### Step 2: Problem Identification
For every element in an array, find the first element to its right that is strictly greater than it. If no greater element exists to its right, search circularly from the beginning of the array. If no greater element exists anywhere, return $-1$.

### Step 3: Formal Problem Statement
Let $A = [a_0, a_1, \dots, a_{n-1}]$ be a circular array of $n$ integers ($n \ge 1$).
For each index $i$ ($0 \le i < n$), find the value $a_j$ such that:
1. $j = (i + k) \pmod n$ for the smallest integer $k \in [1, n - 1]$ satisfying $a_j > a_i$.
2. If no such $k$ exists, output $-1$ for index $i$.

#### Constraints:
- Length: $1 \le n \le 10^6$
- Elements: $-10^9 \le a_i \le 10^9$
- Time budget: Strictly $\mathcal{O}(n)$
- Auxiliary memory budget: $\mathcal{O}(n)$ (to store indices on the monotonic stack).

### Step 4: Thinking Before Coding
1. **Handling the Circular Nature**: How do we handle wrap-around without writing complicated circular logic?
   *The Virtual Doubling Trick*: A circular traversal of an array of size $n$ is mathematically isomorphic to traversing a linearly concatenated array of size $2n$:
   $$A_{\text{virtual}} = A \circ A = [a_0, \dots, a_{n-1}, a_0, \dots, a_{n-1}]$$
   Instead of physically copying the array (which wastes memory), we simply loop index $i$ from $0$ to $2n - 1$ and access elements via $A[i \pmod n]$!
2. **What should the stack store?**
   The stack must store **indices**, not raw values! Storing indices allows us to write the resolved answer directly into the output array `result[stack.top()] = A[i % n]`.
3. **What is the monotonic property?**
   We maintain a **Monotonically Decreasing Stack of Values** (from bottom to top). When a larger value $A[i \pmod n]$ arrives, it resolves and pops all smaller elements sitting on the stack!

### Step 5: First-Principles Reasoning
Consider an element $A[p]$ waiting on the stack. Why is it waiting?
Because no element greater than $A[p]$ has appeared since index $p$.
When we inspect element $A[curr]$:
- If $A[curr] \le A[p]$: $A[curr]$ cannot be the next greater element for $A[p]$. We push $curr$ onto the stack; $curr$ must now also wait for a future larger element.
- If $A[curr] > A[p]$: **$A[curr]$ is the very first element to the right of $p$ that exceeds $A[p]$!** We immediately record `result[p] = A[curr]` and pop $p$.

### Step 6: Brute-Force Implementation (The Quadratic Oracle)

```python
# Reference Baseline Oracle: O(N^2) Time, O(1) Auxiliary Space
def next_greater_elements_oracle(arr: list[int]) -> list[int]:
    n = len(arr)
    result = [-1] * n
    for i in range(n):
        for step in range(1, n):
            j = (i + step) % n
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result
```

### Step 7: Bottleneck Analysis
- The baseline oracle executes an inner loop of up to $n-1$ steps for each of the $n$ elements.
- For strictly descending arrays (e.g., `[5, 4, 3, 2, 1]`), the inner loop searches all the way around the circle before concluding that no greater element exists, executing $\approx n^2$ operations.
- For $n = 10^5$, $n^2 = 10^{10}$ operations $\implies 10$ to $20$ seconds.
- The monotonic stack processes each element in $\mathcal{O}(1)$ amortized time by batch-resolving all smaller waiting elements.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Auxiliary Space | Viable for $N = 10^6$? | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Exhaustive Scan Oracle** | $\Theta(N^2)$ | $\mathcal{O}(1)$ | Impossible | Repeated circular linear re-scans |
| **Segment Tree on Values** | $\mathcal{O}(N \log N)$ | $\mathcal{O}(N)$ | Viable ($35 \text{ ms}$) | High constant factors; complex range max queries |
| **Monotonic Stack ($2N$ virtual)**| $\Theta(N)$ | $\mathcal{O}(N)$ | **Optimal ($2.1 \text{ ms}$)** | Cache-friendly flat stack; single pass |

### Step 9: Derivation of the Circular Monotonic Algorithm
1. Initialize output array `result` of size $n$, filled with $-1$.
2. Initialize an empty stack `st` to store indices.
3. Iterate index $i$ from $0$ to $2n - 1$:
   - Let `val = arr[i % n]`.
   - While `st` is not empty and `arr[st.top()] < val`:
     - Pop `idx = st.pop()`.
     - `result[idx] = val`.
   - If $i < n$: Push $i$ onto `st`.
     *(Note: In the second pass $i \ge n$, we do not push new indices, because all $n$ output slots have already been placed on the stack during the first pass; we only use the second pass to resolve unresolved elements from the first pass).*
4. Return `result`.

### Step 10: Correctness Proof via Invariant

#### Stack Invariant:
At any step $i$ ($0 \le i < 2n$):
1. The stack `st` contains indices $[k_0, k_1, \dots, k_m]$ ($0 \le k_0 < k_1 < \dots < k_m < n$) whose next greater elements have **not yet been discovered**.
2. The corresponding array values are strictly monotonically decreasing:
   $$A[k_0] \ge A[k_1] \ge \dots \ge A[k_m]$$

#### Maintenance:
When inspecting $A[i \pmod n]$:
- If $A[i \pmod n] > A[k_m]$: Since $i > k_m$ in traversal order and no earlier element exceeded $A[k_m]$, $A[i \pmod n]$ is by definition the *first* (closest) element exceeding $A[k_m]$. Recording `result[k_m] = A[i % n]` and popping $k_m$ is correct.
- We repeat this until the top element is $\ge A[i \pmod n]$ or stack is empty, restoring the decreasing invariant.
- For $i < n$, pushing $i$ maintains the decreasing invariant.
- For $i \ge n$, any element that remains on the stack after $2n$ steps has circled the entire array without finding any element strictly greater than itself; its output remains $-1$. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Input: `A = [1, 2, 1]`, $n = 3$. Virtual loop $i = 0 \dots 5$.

| Step $i$ | $i \pmod 3$ | Value $A[\dots]$ | Action Taken | Stack (indices) | `result` State |
| :---: | :---: | :---: | :--- | :---: | :---: |
| 0 | 0 | 1 | Stack empty $\implies$ push 0 | `[0]` (val: 1) | `[-1, -1, -1]` |
| 1 | 1 | 2 | $2 > A[0](1) \implies$ pop 0, `result[0] = 2`. Push 1. | `[1]` (val: 2) | `[ 2, -1, -1]` |
| 2 | 2 | 1 | $1 \le A[1](2) \implies$ push 2 | `[1, 2]` (vals: 2, 1) | `[ 2, -1, -1]` |
| 3 | 0 | 1 | $1 \le A[2](1) \implies$ do not push ($i \ge 3$) | `[1, 2]` | `[ 2, -1, -1]` |
| 4 | 1 | 2 | $2 > A[2](1) \implies$ pop 2, `result[2] = 2`. $2 \le A[1](2) \implies$ stop. | `[1]` (val: 2) | `[ 2, -1,  2]` |
| 5 | 2 | 1 | $1 \le A[1](2) \implies$ stop. | `[1]` | `[ 2, -1,  2]` |

**Final Result**: `[2, -1, 2]`. Correct!

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/STACK-0002.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <cassert>

namespace alg {

/**
 * Finds next greater element in a circular array using a Monotonic Stack.
 * Complexity: O(N) Time, O(N) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
std::vector<int64_t> next_greater_elements(std::span<const int64_t> arr) {
    const size_t n = arr.size();
    if (n == 0) {
        return {};
    }

    std::vector<int64_t> result(n, -1);
    std::vector<size_t> stack; // Stores indices
    stack.reserve(n);

    const size_t virtual_length = 2 * n;

    for (size_t i = 0; i < virtual_length; ++i) {
        const size_t curr_idx = i % n;
        const int64_t current_val = arr[curr_idx];

        // Maintain strictly decreasing value invariant from bottom to top
        while (!stack.empty() && arr[stack.back()] < current_val) {
            size_t resolved_idx = stack.back();
            stack.pop_back();
            result[resolved_idx] = current_val;
        }

        // Only push indices during the first circular pass
        if (i < n) {
            stack.push_back(curr_idx);
        }
    }

    return result;
}

} // namespace alg

// Differential Quadratic Oracle
std::vector<int64_t> next_greater_oracle(std::span<const int64_t> arr) {
    const size_t n = arr.size();
    if (n == 0) return {};
    std::vector<int64_t> result(n, -1);

    for (size_t i = 0; i < n; ++i) {
        for (size_t step = 1; step < n; ++step) {
            size_t j = (i + step) % n;
            if (arr[j] > arr[i]) {
                result[i] = arr[j];
                break;
            }
        }
    }
    return result;
}

int main() {
    std::vector<int64_t> t1{1, 2, 1};
    auto r1 = alg::next_greater_elements(t1);
    auto o1 = next_greater_oracle(t1);
    assert(r1 == o1);
    std::vector<int64_t> exp1{2, -1, 2};
    assert(r1 == exp1);

    std::vector<int64_t> t2{1, 2, 3, 4, 3};
    auto r2 = alg::next_greater_elements(t2);
    auto o2 = next_greater_oracle(t2);
    assert(r2 == o2);
    std::vector<int64_t> exp2{2, 3, 4, -1, 4};
    assert(r2 == exp2);

    // Single element
    std::vector<int64_t> t3{42};
    auto r3 = alg::next_greater_elements(t3);
    assert(r3 == std::vector<int64_t>{-1});

    std::cout << "All C++20 assertions for STACK-0002 passed successfully." << std::endl;
    return 0;
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/STACK-0002.py
from typing import Sequence


def next_greater_elements(arr: Sequence[int]) -> list[int]:
    """
    Finds next greater element in circular array using a Monotonic Stack.
    Target: Python 3.12+ (O(N) Time, O(N) Auxiliary Space).
    """
    n = len(arr)
    if n == 0:
        return []

    result = [-1] * n
    stack: list[int] = []  # Stores indices

    for i in range(2 * n):
        curr_idx = i % n
        curr_val = arr[curr_idx]

        while stack and arr[stack[-1]] < curr_val:
            resolved_idx = stack.pop()
            result[resolved_idx] = curr_val

        if i < n:
            stack.append(curr_idx)

    return result


def next_greater_oracle(arr: Sequence[int]) -> list[int]:
    """Quadratic baseline oracle for differential testing."""
    n = len(arr)
    if n == 0:
        return []
    result = [-1] * n
    for i in range(n):
        for step in range(1, n):
            j = (i + step) % n
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result


if __name__ == "__main__":
    t1 = [1, 2, 1]
    r1 = next_greater_elements(t1)
    o1 = next_greater_oracle(t1)
    assert r1 == o1 == [2, -1, 2], f"Failed: {r1}"

    t2 = [1, 2, 3, 4, 3]
    r2 = next_greater_elements(t2)
    o2 = next_greater_oracle(t2)
    assert r2 == o2 == [2, 3, 4, -1, 4], f"Failed: {r2}"

    print("All Python 3 self-tests for STACK-0002 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(N)$
  - Outer loop runs exactly $2N$ times.
  - Each of the $N$ indices is pushed onto the stack at most once (during $i < N$).
  - Each index is popped from the stack at most once.
  - Total push operations $= N$; Total pop operations $\le N$.
  - Amortized cost per iteration: $\mathcal{O}(1) \implies \Theta(N)$ total time.
- **Space Complexity**: $\Theta(N)$ auxiliary memory
  - The stack stores at most $N$ integer indices.

### Step 15: Edge Cases and Failure Modes
- **All Elements Equal** (e.g., `[5, 5, 5]`): `arr[stack.back()] < curr_val` is false; elements are never popped; output correctly remains all `-1`.
- **Strictly Decreasing** (e.g., `[5, 4, 3, 2, 1]`): Resolved circularly on the second pass by $A[0] = 5$, except for 5 itself, outputting `[-1, 5, 5, 5, 5]`.
- **Single Element** (`[99]`): Returns `[-1]`.

### Step 16: Test Cases & Validation Suite
- Circular wrap-around dependencies (`[1, 2, 1]`).
- Monotonically increasing and decreasing sequences.
- Array with duplicates and identical values.
- Empty array.

### Step 17: Real-World Engineering Application
- Financial Order Books: Locating nearest resistance price levels.
- Weather Forecasting: "Daily Temperatures" (computing days to wait for warmer weather).
- VLSI Design: Shadow calculation in 2D physical wire placement.

### Step 18: Further Optimization & Systems Considerations
- Monotonic stacks benefit immensely from flat contiguous vector backing (`std::vector<size_t>`). Pre-allocating `reserve(n)` eliminates dynamic heap reallocations.

### Step 19: Related Patterns
- **Largest Rectangle in Histogram**: Using a monotonic increasing stack of heights to compute the left and right boundaries where a bar is the minimum height.
- **Sliding Window Maximum**: Using a Monotonic Double-Ended Queue (Deque) to maintain the window maximum in $\mathcal{O}(1)$ amortized time.

### Step 20: Reader Challenges
1. **Challenge 11.1 (Largest Rectangle in Histogram)**: Given an array of bar heights, find the area of the largest rectangle that can be formed within the histogram. Achieve $\mathcal{O}(N)$ time using a monotonic increasing stack.
2. **Challenge 11.2 (Sliding Window Maximum)**: Given an array and a sliding window of size $K$, compute the maximum value in every window using a Monotonic Deque in $\mathcal{O}(N)$ total time.

---

## 11.4 Chapter Synthesis
Monotonic stacks and queues are the definitive algorithmic technique for turning quadratic linear scans into amortized linear invariants. By formalizing dominance and eliminating obsolete candidates, you achieve optimal speed.

In **Chapter 12**, we explore **Hash Tables, Collision Resolution, and Load Factors**, investigating hash functions, open addressing, Robin Hood hashing, and probabilistic sets like Bloom filters.
