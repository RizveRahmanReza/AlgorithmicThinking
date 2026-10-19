# CHAPTER 6: ASYMPTOTIC ANALYSIS AND COMPLEXITY CLASSES

> *"Asymptotic analysis does not measure the speed of your computer today; it measures how your algorithm survives the scaling of the universe tomorrow."*

---

## 6.1 The Formal Definitions: Big-$O$, $\Omega$, and $\Theta$

In popular programming culture, the term "Big-O" is frequently abused as a colloquial shorthand for "worst-case running time." In rigorous computer science, this is an unacceptable confusion of distinct mathematical concepts.

Asymptotic notation describes the **growth rate of functions** as their inputs approach infinity. It says nothing about worst-case, best-case, or average-case until you explicitly specify which cost function you are bounding:

```
+-----------------------------------------------------------------------------+
| Notation    | Mathematical Definition                                       | Plain English Meaning   |
+-----------------------------------------------------------------------------+
| f(n) = O(g(n)) | \exists c > 0, n_0 > 0 \text{ s.t. } 0 \le f(n) \le c \cdot g(n) \; \forall n \ge n_0 | Asymptotic Upper Bound  |
| f(n) = \Omega(g(n)) | \exists c > 0, n_0 > 0 \text{ s.t. } 0 \le c \cdot g(n) \le f(n) \; \forall n \ge n_0 | Asymptotic Lower Bound  |
| f(n) = \Theta(g(n)) | \exists c_1, c_2 > 0, n_0 > 0 \text{ s.t. } c_1 g(n) \le f(n) \le c_2 g(n) \;\forall n \ge n_0 | Asymptotically Tight Bound|
| f(n) = o(g(n)) | \lim_{n \to \infty} \frac{f(n)}{g(n)} = 0                   | Strict Upper Bound      |
| f(n) = \omega(g(n)) | \lim_{n \to \infty} \frac{f(n)}{g(n)} = \infty         | Strict Lower Bound      |
+-----------------------------------------------------------------------------+
```

### The Sandwich Theorem of Asymptotics
A function $f(n)$ is asymptotically tight ($\Theta(g(n))$) if and only if it is simultaneously upper-bounded ($O(g(n))$) and lower-bounded ($\Omega(g(n))$) by the same function:

$$f(n) = \Theta(g(n)) \iff \left( f(n) = \mathcal{O}(g(n)) \quad \text{and} \quad f(n) = \Omega(g(n)) \right)$$

### The Distinction Between Case and Bound
Never confuse the **input case** with the **asymptotic bound**:
- **QuickSort**:
  - Best-case time: $\Theta(n \log n)$
  - Average-case time: $\Theta(n \log n)$
  - Worst-case time: $\Theta(n^2)$
  - Global upper bound across all cases: $\mathcal{O}(n^2)$
- Saying "QuickSort is $O(n^2)$" is mathematically true, but saying "QuickSort is $\Theta(n^2)$" without qualifying it as the *worst case* is false.

---

## 6.2 Amortized Analysis: Aggregate, Accounting, and Potential Methods

When evaluating a data structure, analyzing operations in strict isolation can paint a misleadingly pessimistic picture. 

Consider a dynamic array (like `std::vector` in C++ or `list` in Python):
- Most insertions take $\mathcal{O}(1)$ time (writing a value into an unused preallocated slot).
- Occasionally, when capacity is exhausted, an insertion triggers a complete array reallocation, copying all $N$ elements to a new memory block, taking $\mathcal{O}(N)$ time.

If an engineer only looks at the worst-case single operation ($\mathcal{O}(N)$), they might falsely conclude that dynamic arrays are too slow for real-time applications. **Amortized analysis** provides the mathematical framework to prove that across any arbitrary sequence of $M$ operations, the average cost per operation is guaranteed to be small.

There are three foundational techniques for proving amortized bounds:

```
+-------------------------------------------------------------------------------+
| 1. The Aggregate Method                                                       |
| Compute total cost T(M) for an arbitrary sequence of M operations.            |
| Amortized cost per operation = T(M) / M.                                      |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| 2. The Accounting (Banker's) Method                                           |
| Assign an artificial charge (amortized cost) to each operation.               |
| Overcharged cheap operations accumulate "credit" in a bank.                   |
| Expensive operations consume banked credit so balance is never negative.      |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
| 3. The Potential (Physicist's) Method                                         |
| Define a potential function Phi(D) mapping data structure state to R >= 0.    |
| Amortized cost a_i = actual_cost c_i + Phi(D_i) - Phi(D_{i-1}).               |
| Total amortized cost >= Total actual cost if Phi(D_M) >= Phi(D_0).            |
+-------------------------------------------------------------------------------+
```

---

## 6.3 Lower Bounds and Information-Theoretic Limits

How do we know when an algorithm cannot possibly be improved? We establish a **Theoretical Lower Bound**.

### The Comparison Sort Lower Bound ($\Omega(N \log N)$)
Any deterministic comparison-based sorting algorithm can be modeled as a **Decision Tree**:
1. Each internal node represents a comparison between two elements ($A[i] \le A[j]$).
2. Each branch represents the binary outcome (True or False).
3. Each leaf node represents a distinct permutation of the $n$ elements.

Since there are $n!$ possible permutations of $n$ distinct elements, the decision tree must contain at least $n!$ reachable leaf nodes:
$$\text{Leaves } L \ge n!$$

A binary tree of height $h$ has at most $2^h$ leaves. Therefore:
$$2^h \ge n! \implies h \ge \log_2(n!)$$

Using **Stirling's Approximation** ($\ln(n!) = n \ln n - n + \mathcal{O}(\log n)$):
$$h \ge \log_2(n!) = \sum_{k=1}^n \log_2(k) \ge \sum_{k=\lceil n/2 \rceil}^n \log_2(k) \ge \frac{n}{2} \log_2\left(\frac{n}{2}\right) = \Omega(n \log n)$$

Because the height of the decision tree represents the worst-case number of comparisons, **no comparison-based sorting algorithm can ever execute in faster than $\Omega(n \log n)$ comparisons.**

When an algorithm achieves a time complexity matching the theoretical lower bound, it is declared **asymptotically optimal**.

---

## 6.4 Worked Problem: MATH-0003 — Amortized Analysis of Dynamic Array Geometric Growth

We now formalize the exact mathematics of amortized growth by proving why geometric array expansion guarantees $\mathcal{O}(1)$ amortized time, whereas arithmetic expansion degrades catastrophically to $\mathcal{O}(N^2)$.

---

### Step 1: Real-World Motivation
Every modern programming language provides an auto-resizing contiguous sequence container (`std::vector` in C++, `list` in Python, `ArrayList` in Java, `Vec` in Rust). Systems engineers in database and networking engines must continuously append incoming telemetry records to dynamic buffers without knowing total volume upfront. 

If the reallocation growth strategy is chosen incorrectly (e.g., allocating a fixed extra 1,000 slots whenever full), the system's ingestion throughput collapses exponentially under load, inducing latency timeouts.

### Step 2: Problem Identification
Analyzing the total copy and allocation cost of appending $N$ items to a dynamically resizing contiguous array, contrasting **Geometric Growth** (factor $\alpha > 1$) against **Arithmetic Growth** (constant increment $+K$).

### Step 3: Formal Problem Statement
Let a dynamic array start with capacity $C_0 = 1$ and size $S_0 = 0$.
We execute an arbitrary sequence of $n$ `push_back(x)` operations.
An insertion costs:
- **1 unit of work** (to write the element) if $S_{i-1} < C_{i-1}$.
- **$S_{i-1} + 1$ units of work** (to allocate new memory, copy all $S_{i-1}$ elements, and write the new element) if $S_{i-1} == C_{i-1}$.

Compare two growth policies:
1. **Geometric Growth Policy ($\alpha = 2$)**: When full, new capacity $C_{\text{new}} = 2 \times C_{\text{old}}$.
2. **Arithmetic Growth Policy ($+K$)**: When full, new capacity $C_{\text{new}} = C_{\text{old}} + K$ (for constant $K \ge 1$).

#### Objectives:
- Prove that under Geometric Growth, the total cost for $n$ appends is $\mathcal{O}(n)$, yielding $\mathcal{O}(1)$ amortized cost per append.
- Prove that under Arithmetic Growth, the total cost for $n$ appends is $\Omega(n^2)$, yielding $\Omega(n)$ amortized cost per append.
- Provide a dual-language simulator verifying exact operation cost counts across both policies.

### Step 4: Thinking Before Coding
1. **How many reallocations occur in Geometric Growth?**
   Capacity doubles at sizes $1, 2, 4, 8, \dots, 2^k$.
   The number of reallocations up to size $n$ is $\lfloor \log_2 n \rfloor$.
2. **How many reallocations occur in Arithmetic Growth?**
   Capacity expands at sizes $K, 2K, 3K, \dots, mK$.
   The number of reallocations up to size $n$ is $\approx n / K = \Theta(n)$.
3. **What is the sum of copy operations?**
   - Geometric: A convergent geometric series: $1 + 2 + 4 + \dots + 2^k < 2n$.
   - Arithmetic: An arithmetic progression: $K + 2K + 3K + \dots + n = \Theta(n^2)$.

### Step 5: First-Principles Proof of Amortized Bounds

#### 1. Proof via the Aggregate Method (Geometric Growth $\alpha = 2$):
Total work $W(n)$ across $n$ insertions equals the cost of inserting each element once, plus the total cost of copying elements during reallocations:

$$W(n) = \sum_{i=1}^n 1 + \sum_{j=0}^{\lfloor \log_2 n \rfloor} 2^j = n + (2^{\lfloor \log_2 n \rfloor + 1} - 1) < n + 2n = 3n$$

The amortized cost per operation is:
$$\hat{c} = \frac{W(n)}{n} < \frac{3n}{n} = 3 = \mathcal{O}(1)$$

#### 2. Proof via the Accounting (Banker's) Method:
- Charge each insertion an amortized cost of **\$3**.
- **\$1** pays for the immediate cost of writing the newly inserted element.
- **\$1** is stored as credit on the newly inserted element itself.
- **\$1** is stored as credit on a previously inserted older element that has already moved once.
- When the array doubles from size $N$ to $2N$, exactly $N$ elements were added since the last resize. Each of those $N$ elements holds \$2 in credit (\$2N total credit), which pays completely for copying all $2N$ elements into the new array! The bank balance never drops below zero. Thus, amortized cost is strictly $\le 3 = \mathcal{O}(1)$.

#### 3. Proof of Arithmetic Failure ($+K$):
Suppose capacity increases by a fixed constant $K$ whenever full.
The number of resizes is $m = \lfloor n / K \rfloor$.
The total number of elements copied during resizes is:
$$\sum_{j=1}^m j \cdot K = K \sum_{j=1}^m j = K \frac{m(m+1)}{2} \approx K \frac{(n/K)^2}{2} = \frac{n^2}{2K} = \Theta(n^2)$$
Dividing by $n$ yields an amortized cost of $\Theta(n)$ per append. **Arithmetic growth turns a linear sequence of appends into a disastrous quadratic bottleneck!**

### Step 6: Step-by-Step State Tracking Table ($N=8$, $\alpha=2$)

| Append Step $i$ | Pre-Capacity | Pre-Size | Resize Triggered? | Elements Copied | Raw Cost $c_i$ | New Capacity | Cumulative Cost |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 1 | 0 | No | 0 | 1 | 1 | 1 |
| 2 | 1 | 1 | **Yes** (to 2) | 1 | $1+1 = 2$ | 2 | 3 |
| 3 | 2 | 2 | **Yes** (to 4) | 2 | $2+1 = 3$ | 4 | 6 |
| 4 | 4 | 3 | No | 0 | 1 | 4 | 7 |
| 5 | 4 | 4 | **Yes** (to 8) | 4 | $4+1 = 5$ | 8 | 12 |
| 6 | 8 | 5 | No | 0 | 1 | 8 | 13 |
| 7 | 8 | 6 | No | 0 | 1 | 8 | 14 |
| 8 | 8 | 7 | No | 0 | 1 | 8 | 15 |

**Final Check**: At $N = 8$, total operations $= 15 < 3 \times 8 = 24$. Average cost per insertion $= 15 / 8 = 1.875 < 3$.

### Step 7: Full C++20 Implementation

```cpp
// solutions/cpp/MATH-0003.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <cassert>

struct SimulationMetrics {
    int64_t total_operations;
    int64_t total_copies;
    double amortized_cost_per_op;
};

/**
 * Simulates dynamic array append workload under Geometric Growth (factor 2).
 * Conforms to ISO C++20 standard.
 */
SimulationMetrics simulate_geometric_appends(size_t n) {
    if (n == 0) return {0, 0, 0.0};

    size_t capacity = 1;
    size_t size = 0;
    int64_t total_ops = 0;
    int64_t total_copies = 0;

    for (size_t i = 0; i < n; ++i) {
        if (size == capacity) {
            // Resize triggered
            total_copies += size;
            total_ops += size; // Copy cost
            capacity *= 2;
        }
        // Insert operation
        total_ops += 1;
        size += 1;
    }

    return SimulationMetrics{
        .total_operations = total_ops,
        .total_copies = total_copies,
        .amortized_cost_per_op = static_cast<double>(total_ops) / static_cast<double>(n)
    };
}

/**
 * Simulates dynamic array append workload under Arithmetic Growth (+K).
 */
SimulationMetrics simulate_arithmetic_appends(size_t n, size_t k) {
    if (n == 0 || k == 0) return {0, 0, 0.0};

    size_t capacity = k;
    size_t size = 0;
    int64_t total_ops = 0;
    int64_t total_copies = 0;

    for (size_t i = 0; i < n; ++i) {
        if (size == capacity) {
            total_copies += size;
            total_ops += size;
            capacity += k;
        }
        total_ops += 1;
        size += 1;
    }

    return SimulationMetrics{
        .total_operations = total_ops,
        .total_copies = total_copies,
        .amortized_cost_per_op = static_cast<double>(total_ops) / static_cast<double>(n)
    };
}

int main() {
    const size_t N = 100000;

    // Geometric growth should exhibit O(1) amortized cost (< 3.0)
    auto geom = simulate_geometric_appends(N);
    assert(geom.amortized_cost_per_op < 3.0);
    assert(geom.total_operations < 3 * static_cast<int64_t>(N));

    // Arithmetic growth (+100) should exhibit O(N) amortized cost (>> 100)
    auto arith = simulate_arithmetic_appends(N, 100);
    assert(arith.amortized_cost_per_op > 100.0);

    std::cout << "All C++20 assertions for MATH-0003 passed.\n"
              << "Geometric Amortized Cost: " << geom.amortized_cost_per_op << " ops/insert\n"
              << "Arithmetic (+100) Amortized Cost: " << arith.amortized_cost_per_op << " ops/insert" << std::endl;
    return 0;
}
```

### Step 8: Full Python Implementation

```python
# solutions/python/MATH-0003.py
from typing import NamedTuple


class SimulationMetrics(NamedTuple):
    total_operations: int
    total_copies: int
    amortized_cost_per_op: float


def simulate_geometric_appends(n: int) -> SimulationMetrics:
    """
    Simulates append cost under Geometric Growth (x2).
    Target: Python 3.12+ (O(N) total time, O(1) space).
    """
    if n <= 0:
        return SimulationMetrics(0, 0, 0.0)

    capacity = 1
    size = 0
    total_ops = 0
    total_copies = 0

    for _ in range(n):
        if size == capacity:
            total_copies += size
            total_ops += size
            capacity *= 2
        total_ops += 1
        size += 1

    return SimulationMetrics(
        total_operations=total_ops,
        total_copies=total_copies,
        amortized_cost_per_op=total_ops / n
    )


def simulate_arithmetic_appends(n: int, k: int) -> SimulationMetrics:
    """Simulates append cost under Arithmetic Growth (+K)."""
    if n <= 0 or k <= 0:
        return SimulationMetrics(0, 0, 0.0)

    capacity = k
    size = 0
    total_ops = 0
    total_copies = 0

    for _ in range(n):
        if size == capacity:
            total_copies += size
            total_ops += size
            capacity += k
        total_ops += 1
        size += 1

    return SimulationMetrics(
        total_operations=total_ops,
        total_copies=total_copies,
        amortized_cost_per_op=total_ops / n
    )


if __name__ == "__main__":
    N = 100000
    geom = simulate_geometric_appends(N)
    assert geom.amortized_cost_per_op < 3.0, f"Geometric failed: {geom}"

    arith = simulate_arithmetic_appends(N, 100)
    assert arith.amortized_cost_per_op > 100.0, f"Arithmetic failed: {arith}"

    print(f"All Python 3 self-tests for MATH-0003 passed.\n"
          f"Geometric Amortized Cost: {geom.amortized_cost_per_op:.4f} ops/insert\n"
          f"Arithmetic (+100) Amortized Cost: {arith.amortized_cost_per_op:.4f} ops/insert")
```

### Step 9: Complexity Analysis
- **Geometric Policy**:
  - Total Time: $\Theta(N)$
  - Amortized Time per append: $\Theta(1)$
  - Peak Space Overhead: $\le 2N$ (at most 50% unused capacity).
- **Arithmetic Policy**:
  - Total Time: $\Theta(N^2 / K)$
  - Amortized Time per append: $\Theta(N / K)$
  - Unusable for large $N$.

### Step 10: Real-World Systems Insights (Why $\alpha = 1.5$ vs $\alpha = 2.0$?)
In standard C++ implementations:
- **GCC `libstdc++` and Clang `libc++`** use a growth factor of **$\alpha = 2.0$**.
- **Microsoft MSVC STL and Facebook Folly (`fbvector`)** use a growth factor of **$\alpha = 1.5$**.
*Why 1.5 instead of 2.0?*
With $\alpha = 2.0$, every newly allocated memory block is strictly larger than the sum of all previously freed blocks:
$$\sum_{j=0}^{k-1} 2^j = 2^k - 1 < 2^k$$
This prevents the memory allocator from ever reusing the contiguous chunk of previously freed memory blocks, increasing memory fragmentation. With $\alpha = 1.5$, older contiguous blocks can eventually be recycled, improving memory locality and cache reuse in long-running servers!

---

## 6.5 Synthesis of Part II: Mathematics, Logic, and Complexity

With the completion of Chapter 6, we bring **Part II: Mathematics, Logic, and Complexity** to a triumphant conclusion.

Across Chapters 4, 5, and 6, we have mastered:
1. **Formal Logic & Proof Techniques**: Using invariants, contradiction, and induction to guarantee algorithmic correctness.
2. **Counting, Combinatorics & Recurrences**: Solving divide-and-conquer recurrences via recursion trees and the Master Theorem.
3. **Asymptotic Analysis & Amortization**: Distinguishing upper/lower bounds ($\mathcal{O}, \Omega, \Theta$), understanding information-theoretic sorting limits ($\Omega(N \log N)$), and proving $\mathcal{O}(1)$ amortized guarantees.

We are now equipped with the complete mathematical and analytical toolkit. 

In **Part III: Arrays, Strings, and Linked Lists**, we transition from pure mathematical theory into physical hardware realities: contiguous cache lines, dynamic array internals, UTF-8 strings, and pointer-based linked structures.
