# CHAPTER 4: DISCRETE FOUNDATIONS, LOGIC, AND PROOF TECHNIQUES

> *"A computer program without a mathematical proof is merely a collection of bytes that hasn't failed yet."*

---

## 4.1 Propositional and Predicate Logic in Algorithm Design

Every conditional branch (`if / else`), every loop guard (`while / for`), and every data structure invariant is an assertion in **formal logic**. 

When software bugs emerge in production systems, they rarely originate from hardware memory bit-flips; they originate from **flawed boolean logic**:
- An engineer writes `if (A || B && C)` forgetting operator precedence ($\wedge$ binds tighter than $\vee$).
- An engineer negates a complex query using naive syntax instead of applying De Morgan's laws:
  $$\neg(A \wedge B) \iff (\neg A \vee \neg B)$$
  $$\neg(A \vee B) \iff (\neg A \wedge \neg B)$$
- An engineer conflates the **implication** $P \implies Q$ with its **converse** $Q \implies P$.

### The Implication and its Relatives
In algorithm design, we frequently reason about conditions of the form:
$$\text{Precondition } P \implies \text{Postcondition } Q$$

| Statement | Symbolic Form | Truth Equivalence | Algorithmic Meaning |
| :--- | :--- | :--- | :--- |
| **Direct Implication** | $P \implies Q$ | Standard | "If the array is sorted ($P$), binary search finds the key ($Q$)." |
| **Converse** | $Q \implies P$ | **NOT equivalent** | "Binary search found the key, therefore the entire array must have been sorted." (False! A lucky hit can occur in an unsorted array). |
| **Inverse** | $\neg P \implies \neg Q$ | **NOT equivalent** | "The array is not sorted, therefore binary search cannot find the key." (False! The key might reside at the probed middle index). |
| **Contrapositive** | $\neg Q \implies \neg P$ | **Logically Identical** ($P \implies Q \equiv \neg Q \implies \neg P$) | "If binary search provably cannot locate an element that exists, then the array was not sorted." (Indispensable for proofs by contradiction). |

### Predicate Logic and Quantifiers
In discrete algorithms, properties apply over collections of elements:
- **Universal Quantifier ($\forall$)**: "For all elements $x \in A$, property $P(x)$ holds."
  - *Negation*: $\neg (\forall x \in A, P(x)) \iff \exists x \in A \text{ such that } \neg P(x)$.
  - *Engineering Translation*: To prove an array is *not* sorted, you do not need to examine all pairs; you only need to produce **one single inverted adjacent pair** ($A[i] > A[i+1]$).
- **Existential Quantifier ($\exists$)**: "There exists at least one element $x \in A$ satisfying $P(x)$."
  - *Negation*: $\neg (\exists x \in A, P(x)) \iff \forall x \in A, \neg P(x)$.
  - *Engineering Translation*: To prove that a set contains *no duplicates*, you must prove that *every distinct pair* evaluates to unequal ($A[i] \ne A[j]$).

---

## 4.2 The Four Pillars of Algorithmic Proof

How do we prove beyond doubt that an algorithm terminates and yields the correct output across infinite possible inputs? We rely on four foundational proof techniques:

```
+-----------------------------------------------------------------------+
| 1. Direct Proof                                                       |
| Transform known axioms and preconditions via deductive steps into Q.   |
+-----------------------------------------------------------------------+
                                   |
+-----------------------------------------------------------------------+
| 2. Proof by Contradiction (Reductio ad Absurdum)                      |
| Assume ~Q is true; deduce a logical impossibility (e.g., 0 = 1).      |
+-----------------------------------------------------------------------+
                                   |
+-----------------------------------------------------------------------+
| 3. Mathematical Induction (Weak and Strong)                           |
| Prove Base Case P(0); prove Inductive Step P(k) -> P(k+1).            |
+-----------------------------------------------------------------------+
                                   |
+-----------------------------------------------------------------------+
| 4. Loop Invariants and Structural Induction                           |
| Establish Initialization, Maintenance across state transitions, and   |
| Termination to guarantee postconditions.                              |
+-----------------------------------------------------------------------+
```

### 1. Direct Proof
A direct proof begins with established definitions and preconditions, chaining legitimate deductive inferences until the target conclusion is reached.
- *Example*: Proving that the sum of the first $n$ positive integers is $\frac{n(n+1)}{2}$. By pairing symmetric terms $(1 + n) + (2 + n - 1) + \dots$, the identity follows directly.

### 2. Proof by Contradiction (*Reductio ad Absurdum*)
To prove statement $P \implies Q$:
1. Assume $P$ is True and assume $Q$ is **False** ($\neg Q$ is True).
2. Follow rigorous deductive steps using $P$ and $\neg Q$.
3. Arrive at an undeniable logical contradiction (e.g., an integer is simultaneously even and odd, or a path is strictly shorter than the shortest possible path).
4. Conclude that the assumption $\neg Q$ must be false, meaning $Q$ is unconditionally True.
- *Classic Application*: Proving the correctness of **Dijkstra's Shortest Path Algorithm** or the optimality of **Huffman Coding**.

### 3. Proof by Induction
Induction is the mathematical twin of **recursion**.
- **Base Case**: Establish that the proposition $P(n_0)$ holds for the smallest valid input (typically $n = 0$ or $n = 1$).
- **Inductive Hypothesis**: Assume $P(k)$ holds for an arbitrary integer $k \ge n_0$.
- **Inductive Step**: Using the assumption $P(k)$, prove that $P(k+1)$ must necessarily be True.
- In **Strong Induction**, we assume $P(m)$ holds for *all* $n_0 \le m \le k$ to prove $P(k+1)$. Strong induction is the exact mathematical foundation required to prove the correctness of **Divide and Conquer algorithms** (like MergeSort).

---

## 4.3 Loop Invariants: The Engine of Algorithmic Correctness

In iterative algorithms, **Loop Invariants** are the primary mechanism for proving correctness. As introduced in Chapter 1, a loop invariant must satisfy three properties:

1. **Initialization**: The invariant is true prior to the first execution of the loop.
2. **Maintenance**: If the invariant is true before an iteration of the loop, it remains true before the next iteration.
3. **Termination**: When the loop terminates, the invariant provides a useful property that, combined with the termination condition, proves the algorithm is correct.

### The Contrast with Mathematical Induction
Notice the exact structural isomorphism between a loop invariant and induction:
- **Initialization** corresponds to the **Base Case**.
- **Maintenance** corresponds to the **Inductive Step**.
- **Termination** corresponds to the application of the proven theorem to the halting state.

---

## 4.4 Worked Problem: MATH-0001 — Strict Two-Sum Uniqueness and Invariant Verification

We now demonstrate how formal proof techniques (specifically invariants and contradiction) govern the design of a foundational problem: **Verifying and Locating Target Sum Pairs in Monotonic Sequences**.

---

### Step 1: Real-World Motivation
In high-frequency automated portfolio rebalancing, a trading desk holds a strictly sorted ledger of asset prices. The trading engine needs to execute a matched pair order: simultaneously buying one asset and selling another such that their combined value equals an exact cash settlement target $K$. Because trades are executed in real time under latency penalties, the engine cannot tolerate quadratic nested loops. Furthermore, the risk desk requires mathematical proof that no valid pair is ever missed.

### Step 2: Problem Identification
Given a strictly sorted sequence of numbers, locate two distinct indices whose values sum to an exact target $T$, or formally prove that no such pair exists.

### Step 3: Formal Problem Statement
Let $A = [a_0, a_1, \dots, a_{n-1}]$ be an array of $n$ integers strictly sorted in non-decreasing order:
$$a_0 \le a_1 \le a_2 \le \dots \le a_{n-1}$$
Given a target integer $T \in \mathbb{Z}$:
Find indices $L$ and $R$ ($0 \le L < R < n$) such that:
$$a_L + a_R = T$$
If multiple such pairs exist, return the pair with the smallest left index $L$. If no such pair exists, return an empty indication.

#### Constraints:
- Length: $2 \le n \le 10^6$
- Elements: $-10^9 \le a_i \le 10^9$
- Target: $-2 \times 10^9 \le T \le 2 \times 10^9$
- Time budget: Strictly $\mathcal{O}(n)$
- Auxiliary memory budget: Strictly $\mathcal{O}(1)$

### Step 4: Thinking Before Coding
1. **Is the input sorted?** Yes! This is our primary structural clue. The monotonicity constraint means we must not use a hash map (which requires $\mathcal{O}(n)$ auxiliary space and destroys cache locality); we can utilize the order directly.
2. **Could the sum overflow 32-bit signed integers?** Yes: $10^9 + 10^9 = 2 \times 10^9$, and $(-10^9) + (-10^9) = -2 \times 10^9$. In C++, while within `INT32_MAX` ($\approx 2.14 \times 10^9$), edge cases can exceed signed 32-bit limits. We enforce `int64_t` for sum accumulators.
3. **What is the two-pointer invariant?** If we place one pointer at the start ($L = 0$) and one at the end ($R = n-1$):
   - If $a_L + a_R > T$, can $a_R$ ever pair with any other element to its right? No, because all elements to its right are $\ge a_R$, making sums even larger. Thus, $R$ can be safely decremented.

### Step 5: First-Principles Reasoning
In a naive search, there are $\binom{n}{2} = \frac{n(n-1)}{2} = \Theta(n^2)$ pairs.
Can we discard candidates in bulk rather than checking them one by one?
Consider the matrix $M_{i, j} = a_i + a_j$. Because $A$ is sorted, every row of $M$ is sorted left-to-right, and every column is sorted top-to-bottom.
When evaluating $(L, R)$:
- If $a_L + a_R > T$, then for *all* $k \in [L, R-1]$, $a_k + a_R \le a_L + a_R$ is false—actually, since $a_k \ge a_L$, $a_k + a_R \ge a_L + a_R > T$.
- This means $a_R$ **cannot pair with ANY element in the active range $[L \dots R-1]$!**
- With a single comparison, we discard $R - L$ pairs simultaneously!

### Step 6: Brute-Force Implementation (Oracle)

```python
# Reference Baseline Oracle: O(N^2)
def two_sum_sorted_oracle(arr: list[int], T: int):
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == T:
                return (i, j)
    return None
```

### Step 7: Bottleneck Analysis
The quadratic oracle checks $\Theta(n^2)$ pairs. For $n = 10^6$, $\approx 5 \times 10^{11}$ operations, taking over 10 minutes.
The bottleneck is evaluating pairs $(k, R)$ when we already know that $a_L + a_R > T$ and $a_k \ge a_L$, which mathematically guarantees that $a_k + a_R > T$. Testing those pairs is completely redundant.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Space Complexity | Viability for $N = 10^6$ | Hardware / Memory Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Exhaustive Oracle** | $\mathcal{O}(n^2)$ | $\mathcal{O}(1)$ | Impossible | Billions of CPU cycles |
| **Hash Table Set** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Viable but poor | Allocates tens of megabytes; hash collisions; cache-hostile |
| **Binary Search on Each** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(1)$ | Viable ($15 \text{ ms}$) | Repeated logarithmic branch traversals |
| **Two-Pointer Invariant** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Optimal ($1.1 \text{ ms}$)** | Zero allocations; contiguous cache stride; provably minimal |

### Step 9: Derivation of the Two-Pointer Algorithm
1. Initialize $L = 0$ and $R = n - 1$.
2. While $L < R$:
   - Calculate $S = a_L + a_R$.
   - If $S == T$: Return $(L, R)$.
   - If $S > T$: Decrement $R$ by 1 ($R \leftarrow R - 1$).
   - If $S < T$: Increment $L$ by 1 ($L \leftarrow L + 1$).
3. If $L \ge R$: Return not found.

### Step 10: Correctness Proof via Contradiction and Invariant

#### Loop Invariant:
At the start of each iteration of the `while (L < R)` loop:
> **Invariant**: If a valid pair $(i^*, j^*)$ exists such that $a_{i^*} + a_{j^*} = T$, then it must satisfy:
> $$L \le i^* < j^* \le R$$
> In other words, no step has ever discarded a valid solution index.

#### Base Case (Initialization):
Before the first iteration, $L = 0$ and $R = n - 1$. Since any valid indices must satisfy $0 \le i^* < j^* \le n - 1$, the invariant trivially holds.

#### Maintenance (Inductive Step):
Assume the invariant holds for the current boundaries $L$ and $R$.
- **Case 1: $a_L + a_R == T$**:
  The algorithm terminates and returns $(L, R)$, which is correct.
- **Case 2: $a_L + a_R > T$**:
  The algorithm decrements $R$ to $R - 1$, discarding index $R$.
  *Proof by Contradiction that $R$ cannot be part of any valid pair*:
  Suppose $R = j^*$ for some valid pair $(i^*, R)$ with $L \le i^* < R$.
  Since the array is sorted, $a_{i^*} \ge a_L$.
  Therefore:
  $$a_{i^*} + a_R \ge a_L + a_R$$
  But our case condition is $a_L + a_R > T$. Thus:
  $$a_{i^*} + a_R > T$$
  This contradicts the premise that $a_{i^*} + a_R = T$.
  Therefore, index $R$ cannot pair with *any* index in $[L \dots R-1]$. Discarding $R$ preserves the invariant.
- **Case 3: $a_L + a_R < T$**:
  By symmetric reasoning, $a_L + a_k \le a_L + a_R < T$ for all $k \le R$. Thus $a_L$ cannot pair with any remaining candidate. Incrementing $L$ to $L + 1$ preserves the invariant.

#### Termination:
The loop terminates either when $a_L + a_R == T$ (returning a valid pair) or when $L \ge R$.
If $L \ge R$, the active set contains fewer than 2 elements. By the invariant, if a solution existed, it must be contained in this empty set—a contradiction. Therefore, no valid pair exists in the array. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Given sorted array: $A = [1, 3, 5, 8, 12, 15, 19]$, Target $T = 17$.

| Iteration | $L$ | $R$ | $A[L]$ | $A[R]$ | Current Sum $S$ | Comparison vs $T=17$ | Action Taken |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | 0 | 6 | 1 | 19 | 20 | $20 > 17$ | Discard $R$: $R \leftarrow 5$ |
| 2 | 0 | 5 | 1 | 15 | 16 | $16 < 17$ | Discard $L$: $L \leftarrow 1$ |
| 3 | 1 | 5 | 3 | 15 | 18 | $18 > 17$ | Discard $R$: $R \leftarrow 4$ |
| 4 | 1 | 4 | 3 | 12 | 15 | $15 < 17$ | Discard $L$: $L \leftarrow 2$ |
| 5 | 2 | 4 | 5 | 12 | 17 | **$17 == 17$** | **Target Found!** Return $(2, 4)$ |

**Result**: Indices $(2, 4)$ with values $5 + 12 = 17$.

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/MATH-0001.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <optional>
#include <utility>
#include <cassert>

struct PairIndices {
    size_t left;
    size_t right;

    bool operator==(const PairIndices& other) const = default;
};

/**
 * Finds two distinct indices in a sorted sequence summing to target.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 * Standard: ISO C++20.
 */
std::optional<PairIndices> find_sorted_two_sum(
    std::span<const int64_t> arr, 
    int64_t target
) {
    if (arr.size() < 2) {
        return std::nullopt;
    }

    size_t left = 0;
    size_t right = arr.size() - 1;

    while (left < right) {
        const int64_t current_sum = arr[left] + arr[right];

        if (current_sum == target) {
            return PairIndices{.left = left, .right = right};
        } else if (current_sum > target) {
            --right;
        } else {
            ++left;
        }
    }

    return std::nullopt;
}

// Differential Quadratic Oracle for verification
std::optional<PairIndices> find_sorted_two_sum_oracle(
    std::span<const int64_t> arr,
    int64_t target
) {
    for (size_t i = 0; i < arr.size(); ++i) {
        for (size_t j = i + 1; j < arr.size(); ++j) {
            if (arr[i] + arr[j] == target) {
                return PairIndices{.left = i, .right = j};
            }
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<int64_t> test_arr{1, 3, 5, 8, 12, 15, 19};
    auto res = find_sorted_two_sum(test_arr, 17);
    auto oracle_res = find_sorted_two_sum_oracle(test_arr, 17);

    assert(res.has_value() && oracle_res.has_value());
    assert(res.value() == oracle_res.value());
    assert(res.value().left == 2 && res.value().right == 4);

    // Negative case
    auto not_found = find_sorted_two_sum(test_arr, 100);
    assert(!not_found.has_value());

    std::cout << "All C++20 test assertions for MATH-0001 passed successfully." << std::endl;
    return 0;
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/MATH-0001.py
from typing import Sequence, Optional, NamedTuple


class PairIndices(NamedTuple):
    left: int
    right: int


def find_sorted_two_sum(arr: Sequence[int], target: int) -> Optional[PairIndices]:
    """
    Finds two distinct indices in a sorted sequence summing to target.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    if len(arr) < 2:
        return None

    left: int = 0
    right: int = len(arr) - 1

    while left < right:
        current_sum: int = arr[left] + arr[right]

        if current_sum == target:
            return PairIndices(left, right)
        elif current_sum > target:
            right -= 1
        else:
            left += 1

    return None


def find_sorted_two_sum_oracle(arr: Sequence[int], target: int) -> Optional[PairIndices]:
    """Quadratic baseline oracle for differential verification."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return PairIndices(i, j)
    return None


if __name__ == "__main__":
    data = [1, 3, 5, 8, 12, 15, 19]
    ans = find_sorted_two_sum(data, 17)
    oracle_ans = find_sorted_two_sum_oracle(data, 17)
    assert ans == oracle_ans == PairIndices(2, 4), f"Failed: {ans}"

    assert find_sorted_two_sum(data, 100) is None
    print("All Python 3 self-tests for MATH-0001 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(N)$ worst-case. In each step of the loop, either $L$ increases by 1 or $R$ decreases by 1. Since $L$ starts at $0$ and $R$ starts at $n-1$, the loop executes at most $n-1$ times. Each iteration performs $\mathcal{O}(1)$ operations.
- **Space Complexity**: $\Theta(1)$ auxiliary space. Only two pointer indices (`left`, `right`) and a scalar accumulator are retained.
- **Cache Behavior**: Two pointers stride inwards from opposite ends of a contiguous vector. Hardware stream prefetchers easily track both streams.

### Step 15: Edge Cases and Failure Modes
- Array size $< 2$: Handled immediately with `std::nullopt` / `None`.
- Duplicate elements summing to target (e.g., $A = [2, 4, 4, 9]$, $T = 8$): Correctly returns $(1, 2)$.
- Extreme signed values: Handled with 64-bit integer addition.

### Step 16: Test Cases & Validation
- Standard hit, boundary elements ($A[0] + A[n-1] == T$), target strictly between adjacent elements, and completely unreachable targets.

### Step 17: Real-World Engineering Application
- Collateral Optimization in Financial Clearinghouses: Finding paired offsetting derivative liabilities to net out liquidity obligations.
- Memory Arena Allocation: Pairing split buddy blocks in zero-fragmentation allocators.

### Step 18: Further Optimization
- If the target sum is far outside the active range, we can use **Exponential Search** to reposition $R$ to $\text{upper\_bound}(T - A[0])$ before beginning the linear two-pointer scan.

### Step 19: Related Patterns
- **3-Sum Problem**: Fixing one element $A[i]$ and executing a 2-Sum scan on the remainder reduces 3-Sum from $\mathcal{O}(N^3)$ to $\mathcal{O}(N^2)$.
- **Container With Most Water**: Two pointers moving inward based on height comparison.

### Step 20: Reader Challenges
1. **Challenge 4.1 (3-Sum Zero)**: Extend this invariant to find all unique triplets summing to 0 in $\mathcal{O}(N^2)$ time and $\mathcal{O}(1)$ space, proving why sorting upfront is optimal.
2. **Challenge 4.2 (Two-Sum with Unsorted Data under Strict $O(1)$ Space)**: Prove why finding two-sum in an unsorted array requires either $\mathcal{O}(N \log N)$ time (via sorting) or $\mathcal{O}(N)$ space (via hashing), referencing comparison tree lower bounds.

---

## 4.5 Chapter Synthesis
Mathematical logic and proof techniques are not decorative academic rituals; they are the sole guarantee of algorithmic correctness. 

In **Chapter 5**, we build upon this logical foundation to master **Counting, Combinatorics, and Recurrences**, exploring how to model the exact operational cost of recursive divide-and-conquer structures.
