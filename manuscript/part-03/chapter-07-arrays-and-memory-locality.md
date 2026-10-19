# CHAPTER 7: CONTIGUOUS MEMORY, DYNAMIC ARRAYS, AND MEMORY LOCALITY

> *"To the mathematician, an array is an indexed sequence in $\mathbb{R}^n$. To the CPU, an array is a linear sequence of physical bytes striding across cache lines."*

---

## 7.1 The Physics of Memory: Why Contiguity Dominates Modern Computing

In theoretical computer science, the classical **Random Access Machine (RAM) model** posits that accessing any memory address requires uniform $\mathcal{O}(1)$ time. 

On physical hardware, this assumption is an illusion.

Modern microprocessors do not operate directly on main memory (DRAM). Accessing main memory takes approximately $50$ to $100$ nanoseconds ($\approx 200$ to $300$ clock cycles), during which an out-of-order execution CPU core stalls helplessly. To hide this vast latency disparity, hardware architects place a multi-tiered hierarchy of high-speed silicon caches between the CPU execution registers and main memory:

```
+---------------------------------------------------------------------------------+
| Level          | Typical Capacity | Access Latency  | Relative Clock Cycle Cost |
+---------------------------------------------------------------------------------+
| CPU Registers  | ~1 - 2 KB        | ~0.5 ns         | 1 cycle                   |
| L1 Data Cache  | ~32 - 64 KB      | ~1.0 - 1.5 ns   | 4 - 5 cycles              |
| L2 Cache       | ~512 KB - 1 MB   | ~3.0 - 5.0 ns   | 12 - 15 cycles            |
| L3 Shared Cache| ~16 - 64 MB      | ~10 - 20 ns     | 40 - 60 cycles            |
| Main DRAM      | ~16 - 128 GB     | ~60 - 100 ns    | 200 - 300 cycles (STALL!) |
+---------------------------------------------------------------------------------+
```

### The Cache Line and Hardware Prefetchers
Memory is not transferred between DRAM and CPU caches in individual bytes; it is fetched in atomic blocks called **Cache Lines** (typically **64 bytes** in modern x86-64 and ARM64 architectures).

When your code accesses a single 64-bit integer (`int64_t`, 8 bytes) at address $P$:
1. The hardware does not load merely 8 bytes; it loads the entire 64-byte aligned chunk containing $P$ into the L1 cache.
2. The next 7 integers adjacent to $P$ ($P+1$ through $P+7$) are now residing directly in the L1 cache for free!
3. Furthermore, the CPU's hardware **Stream Prefetcher** detects your sequential access stride ($\Delta = +8$ bytes) and proactively fetches subsequent cache lines into L2 and L1 *before your instruction even executes*.

This phenomenon is **Spatial Locality**. An algorithm that traverses contiguous memory with unit stride achieves near-zero memory stall cycles. Conversely, an algorithm that chases pointers scattered randomly across the heap (such as a standard linked list or pointer-heavy binary tree) incurs an L1/L2/L3 cache miss on nearly every access—running **10 to 50 times slower** in practice despite having identical asymptotic Big-$O$ complexity!

---

## 7.2 Static vs. Dynamic Arrays: Memory Layout and Geometric Resizing

### Memory Layout Comparison

| Feature | Static Array (`std::array`, C-style `T[N]`) | Dynamic Array (`std::vector`, Python `list`) |
| :--- | :--- | :--- |
| **Storage Location** | Stack or Static Data Segment | Control metadata on Stack; contiguous elements on Heap |
| **Size Fixed at Compile-Time?** | Yes | No (resizes dynamically at runtime) |
| **Pointer Indirection** | None (direct indexed offset) | Single pointer indirection to heap buffer |
| **Memory Overhead** | 0 bytes auxiliary overhead | 24 bytes (Pointer, Size, Capacity on 64-bit platforms) |

### The Mechanics of Geometric Capacity Doubling
As mathematically proven in Chapter 6 (Problem `MATH-0003`), dynamic arrays maintain $\mathcal{O}(1)$ amortized insertion cost by expanding capacity geometrically ($\times 2$ or $\times 1.5$) whenever `size == capacity`:

```
Initial Capacity = 4:
Heap: [ E0 | E1 | E2 | E3 ] (Full)

Append E4 triggers reallocation:
1. Allocate new buffer of size 8 on Heap.
2. Copy / Move elements E0...E3 to new buffer.
3. Deallocate old buffer of size 4.
4. Insert E4 into new buffer.

New Buffer (Capacity = 8, Size = 5):
Heap: [ E0 | E1 | E2 | E3 | E4 | Unused | Unused | Unused ]
```

---

## 7.3 In-Place Transformations: Space Invariants and Cyclic Decomposition

When working with contiguous arrays under strict systems constraints (e.g., embedded devices, kernel drivers, high-throughput GPU memory buffers), allocating an auxiliary temporary array of size $N$ is strictly prohibited ($\mathcal{O}(1)$ auxiliary space budget).

To transform, reorder, or rotate an array in place, algorithmic thinkers use two foundational techniques:
1. **The Reversal Algorithm (Mirror Inversion)**: Decomposing a permutation into a sequence of symmetric subarray reversals.
2. **Cyclic Decomposition (Juggling / Orbit Algorithm)**: Decomposing the permutation into disjoint cycles and shifting elements around each cycle using a single temporary register.

---

## 7.4 Worked Problem: ARR-0001 — In-Place Array Rotation and Cache Line Alignment

We now execute the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify in-place array rotation across both C++20 and Python 3.12.

---

### Step 1: Real-World Motivation
In high-performance circular logging buffers, audio digital signal processing (DSP) rings, and display framebuffer scrolling engines, data sequences must be rotated cyclically by $k$ positions. 

In a low-latency network interface card (NIC) driver, allocating dynamic heap memory during a packet buffer shift would trigger memory fragmentation and introduce non-deterministic allocator latency spikes. The buffer must be rotated **strictly in place** using $\mathcal{O}(1)$ auxiliary memory while maintaining high memory cache throughput.

### Step 2: Problem Identification
Given an array of $n$ elements, rotate the array cyclically to the right by $k$ positions such that each element at index $i$ moves to index $(i + k) \pmod n$.

### Step 3: Formal Problem Statement
Let $A = [a_0, a_1, \dots, a_{n-1}]$ be an array of $n$ elements.
Given an integer shift amount $k \in \mathbb{Z}_{\ge 0}$:
Transform $A$ in place such that for all $0 \le i < n$:
$$A'[(i + k) \pmod n] = A[i]$$

#### Constraints:
- Array length: $0 \le n \le 10^7$
- Shift amount: $0 \le k \le 10^{15}$
- Elements: 64-bit integers (`int64_t` in C++, arbitrary integers in Python)
- Time budget: Strictly $\mathcal{O}(n)$
- Auxiliary space budget: Strictly $\mathcal{O}(1)$ (Zero dynamic heap allocations)

### Step 4: Thinking Before Coding
1. **What if $k \ge n$?**
   Rotating an array of length $n$ by $n$ positions returns the array to its original state. 
   Therefore, any shift amount $k$ is mathematically equivalent to:
   $$k_{\text{eff}} = k \pmod n$$
   If $n = 0$ or $k_{\text{eff}} = 0$, the operation is an immediate no-op.
2. **Can we allocate a temporary buffer?**
   No. The constraint states $n \le 10^7$ under an $\mathcal{O}(1)$ auxiliary space budget. Allocating a temporary vector of $10^7$ elements would require $80 \text{ MB}$ of memory, violating our embedded/driver memory envelope.

### Step 5: First-Principles Reasoning & The Reversal Invariant
Let us view the array $A$ as divided into two contiguous segments:
- Segment $X = A[0 \dots n - k - 1]$ (the first $n - k$ elements, which must move to the back).
- Segment $Y = A[n - k \dots n - 1]$ (the last $k$ elements, which must move to the front).

The array can be represented as the concatenation:
$$A = X Y$$
The desired rotated array is:
$$A' = Y X$$

How can we transform $X Y \to Y X$ using only the operation of reversing a subarray in place ($\text{rev}(S) = S^R$)?
Notice what happens when we reverse both components individually:
$$(X^R Y^R)$$
Now, what happens if we reverse the **entire combined array**?
$$(X^R Y^R)^R = (Y^R)^R (X^R)^R = Y X$$

**The Three-Step Reversal Theorem**:
1. Reverse the prefix $X$: $\text{Reverse}(A, 0, n - k - 1)$.
2. Reverse the suffix $Y$: $\text{Reverse}(A, n - k, n - 1)$.
3. Reverse the entire array $A$: $\text{Reverse}(A, 0, n - 1)$.

Each element is swapped exactly twice, resulting in an optimal in-place transformation!

### Step 6: Brute-Force Implementation (The Oracle)

```python
# Reference Baseline: Shifting 1 step at a time k times (O(n * k) Time, O(1) Space)
def rotate_right_brute(arr: list[int], k: int) -> None:
    n = len(arr)
    if n == 0:
        return
    k = k % n
    for _ in range(k):
        # Shift entire array right by 1
        last = arr[-1]
        for i in range(n - 1, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = last
```

### Step 7: Bottleneck Analysis
- The baseline shifts the array by 1 position $k$ times.
- Each 1-step shift requires moving all $n-1$ elements.
- Total operations: $\Theta(n \cdot (k \pmod n))$.
- For $n = 10^6$ and $k = 5 \times 10^5$, total operations $\approx 5 \times 10^{11}$, taking over 10 minutes.
- The defect is shifting elements through intermediate positions that are not their final destination.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Auxiliary Space | Cache Performance | Complexity / Fragility |
| :--- | :--- | :--- | :--- | :--- |
| **Repeated 1-step Shift** | $\mathcal{O}(n \cdot k)$ | $\mathcal{O}(1)$ | Unviable ($> 100 \text{ s}$) | Simple but unacceptably slow |
| **Auxiliary Copy Buffer** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Good | Violates $\mathcal{O}(1)$ memory constraint |
| **Cyclic Juggling (GCD Orbits)**| $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | Poor (strided cache misses) | Complex index math; poor locality |
| **Three-Step Reversal** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **Optimal (Sequential Strides)** | Highly readable; optimal cache prefetching |

### Step 9: Derivation of the Three-Step Reversal Algorithm
1. If $n \le 1$, return immediately.
2. Compute $k = k \pmod n$. If $k == 0$, return.
3. Reverse range $[0, n - k - 1]$.
4. Reverse range $[n - k, n - 1]$.
5. Reverse range $[0, n - 1]$.

### Step 10: Correctness Proof via Symmetric Mapping

#### Subarray Inversion Mapping:
The operation $\text{Reverse}(A, l, r)$ maps an element originally at index $l + \delta$ to $r - \delta$ for all $0 \le \delta \le r - l$.

Let $m = n - k$.
1. **First Reversal**: Elements in $X = A[0 \dots m - 1]$ move according to:
   $$\pi_1(i) = (m - 1) - i \quad \text{for } 0 \le i < m$$
2. **Second Reversal**: Elements in $Y = A[m \dots n - 1]$ move according to:
   $$\pi_2(i) = (n - 1) - (i - m) = n + m - 1 - i \quad \text{for } m \le i < n$$
3. **Third Reversal (Entire Array)**: Reversing the entire array from $0$ to $n-1$ maps any intermediate index $j$ to $(n - 1) - j$.

Evaluating the composite permutation $\pi_{\text{final}}(i) = (n - 1) - \pi(i)$:
- For $i \in X$ ($0 \le i < m$):
  $$\pi_{\text{final}}(i) = (n - 1) - ((m - 1) - i) = n - 1 - m + 1 + i = n - m + i$$
  Since $m = n - k$, $n - m = k$. Thus:
  $$\pi_{\text{final}}(i) = i + k$$
- For $i \in Y$ ($m \le i < n$):
  $$\pi_{\text{final}}(i) = (n - 1) - (n + m - 1 - i) = n - 1 - n - m + 1 + i = i - m$$
  Since $m = n - k$, $i - m = i - (n - k) = i + k - n \equiv (i + k) \pmod n$.

Both partitions map identically to $(i + k) \pmod n$. The algorithm is unconditionally correct. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Given: $A = [1, 2, 3, 4, 5, 6, 7]$, $n = 7, k = 3$.
Here $n - k = 7 - 3 = 4$.
Partition: $X = [1, 2, 3, 4]$ (indices $0 \dots 3$), $Y = [5, 6, 7]$ (indices $4 \dots 6$).

1. **Step 1: Reverse $X$ ($[0 \dots 3]$)**:
   Swaps: $(1 \leftrightarrow 4), (2 \leftrightarrow 3)$.
   Array becomes: `[4, 3, 2, 1, 5, 6, 7]`
2. **Step 2: Reverse $Y$ ($[4 \dots 6]$)**:
   Swaps: $(5 \leftrightarrow 7)$.
   Array becomes: `[4, 3, 2, 1, 7, 6, 5]`
3. **Step 3: Reverse Entire Array ($[0 \dots 6]$)**:
   Swaps: $(4 \leftrightarrow 5), (3 \leftrightarrow 6), (2 \leftrightarrow 7), 1 \text{ stays at center}$.
   Array becomes: `[5, 6, 7, 1, 2, 3, 4]`

**Result**: Array correctly rotated by 3 to the right: `[5, 6, 7, 1, 2, 3, 4]`.

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/ARR-0001.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <utility>
#include <cassert>

namespace alg {

/**
 * Reverses a contiguous subsegment [left, right] in place.
 * Exhibits optimal spatial locality with symmetric inward strides.
 */
void reverse_range(std::span<int64_t> arr, size_t left, size_t right) {
    while (left < right) {
        std::swap(arr[left], arr[right]);
        ++left;
        --right;
    }
}

/**
 * Rotates an array in-place cyclically to the right by k positions.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
void rotate_right_in_place(std::span<int64_t> arr, uint64_t k) {
    const size_t n = arr.size();
    if (n <= 1) {
        return;
    }

    const size_t effective_k = static_cast<size_t>(k % n);
    if (effective_k == 0) {
        return;
    }

    const size_t split_point = n - effective_k;

    // Step 1: Reverse prefix [0 ... split_point - 1]
    reverse_range(arr, 0, split_point - 1);

    // Step 2: Reverse suffix [split_point ... n - 1]
    reverse_range(arr, split_point, n - 1);

    // Step 3: Reverse entire array [0 ... n - 1]
    reverse_range(arr, 0, n - 1);
}

} // namespace alg

// Differential Quadratic Baseline Oracle
void rotate_right_oracle(std::vector<int64_t>& arr, uint64_t k) {
    if (arr.size() <= 1) return;
    size_t n = arr.size();
    size_t eff_k = static_cast<size_t>(k % n);
    for (size_t s = 0; s < eff_k; ++s) {
        int64_t last = arr.back();
        for (size_t i = n - 1; i > 0; --i) {
            arr[i] = arr[i - 1];
        }
        arr[0] = last;
    }
}

int main() {
    std::vector<int64_t> test_arr{1, 2, 3, 4, 5, 6, 7};
    std::vector<int64_t> oracle_arr = test_arr;

    alg::rotate_right_in_place(test_arr, 3);
    rotate_right_oracle(oracle_arr, 3);

    assert(test_arr == oracle_arr);
    std::vector<int64_t> expected{5, 6, 7, 1, 2, 3, 4};
    assert(test_arr == expected);

    // Edge Case: k > n
    std::vector<int64_t> arr2{10, 20, 30, 40};
    alg::rotate_right_in_place(arr2, 10); // 10 % 4 = 2
    std::vector<int64_t> expected2{30, 40, 10, 20};
    assert(arr2 == expected2);

    std::cout << "All C++20 assertions for ARR-0001 passed successfully." << std::endl;
    return 0;
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/ARR-0001.py
from typing import MutableSequence


def reverse_range(arr: MutableSequence[int], left: int, right: int) -> None:
    """Reverses elements in arr between indices left and right in-place."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def rotate_right_in_place(arr: MutableSequence[int], k: int) -> None:
    """
    Rotates arr in place cyclically to the right by k positions.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    n = len(arr)
    if n <= 1:
        return

    effective_k = k % n
    if effective_k == 0:
        return

    split_point = n - effective_k

    # Step 1: Reverse prefix
    reverse_range(arr, 0, split_point - 1)
    # Step 2: Reverse suffix
    reverse_range(arr, split_point, n - 1)
    # Step 3: Reverse entire array
    reverse_range(arr, 0, n - 1)


def rotate_right_oracle(arr: MutableSequence[int], k: int) -> None:
    """Quadratic oracle for differential testing (O(N * k))."""
    n = len(arr)
    if n <= 1:
        return
    eff_k = k % n
    for _ in range(eff_k):
        last = arr[-1]
        for i in range(n - 1, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = last


if __name__ == "__main__":
    t1 = [1, 2, 3, 4, 5, 6, 7]
    o1 = list(t1)
    rotate_right_in_place(t1, 3)
    rotate_right_oracle(o1, 3)
    assert t1 == o1 == [5, 6, 7, 1, 2, 3, 4], f"Failed: {t1}"

    t2 = [10, 20, 30, 40]
    rotate_right_in_place(t2, 10)
    assert t2 == [30, 40, 10, 20]

    print("All Python 3 self-tests for ARR-0001 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(n)$
  - Reversing prefix of size $n - k$ performs $\lfloor (n - k) / 2 \rfloor$ swaps.
  - Reversing suffix of size $k$ performs $\lfloor k / 2 \rfloor$ swaps.
  - Reversing entire array of size $n$ performs $\lfloor n / 2 \rfloor$ swaps.
  - Total swaps: $\approx \frac{n-k}{2} + \frac{k}{2} + \frac{n}{2} = n$ swaps.
  - Each element is read and written exactly twice. Strictly $2n$ memory accesses $\implies \Theta(n)$.
- **Space Complexity**: $\Theta(1)$ auxiliary memory. Only three scalar pointer indices are maintained.
- **Hardware Cache Analysis**:
  - Reversal accesses memory symmetrically from both ends inwards.
  - This preserves strong spatial locality within 64-byte cache lines, making the Three-Step Reversal significantly faster than cyclic juggling algorithms that jump across memory strides of size $k$.

### Step 15: Edge Cases and Failure Modes
- $n = 0$ or $n = 1$: Guard clause exits cleanly.
- $k = 0$ or $k = c \cdot n$: Handled by `k % n == 0`.
- Large $k$ ($k \ge 10^{15}$): Modulo arithmetic prevents integer overflow.

### Step 16: Test Cases & Differential Validation
- Standard array, prime-sized array ($n = 7$), single-element array, array where $k > n$, and differential equivalence against the quadratic oracle.

### Step 17: Real-World Engineering Application
- Circular audio streaming buffers in digital sound synthesis.
- Horizontal pixel buffer scrolling in embedded display controllers.
- Thread work-stealing deque rebalancing in multicore runtimes.

### Step 18: Further Optimization
- In 64-bit architectures with AVX-512 support, contiguous byte reversals can be vectorized using byte-shuffle registers (`_mm512_shuffle_epi8`).

### Step 19: Related Patterns
- **String Word Reversal**: Reversing all words in a sentence in place ("the sky is blue" $\to$ "blue is sky the").
- **Block-Swapping Algorithms**: Gries-Mills algorithms using GCD decomposition.

### Step 20: Reader Challenges
1. **Challenge 7.1 (Cyclic Juggling Algorithm)**: Implement in-place rotation using GCD orbits and prove why the number of disjoint cycles is exactly $\gcd(n, k)$.
2. **Challenge 7.2 (Left Rotation)**: Formulate the left-rotation variant ($A'[(i - k) \pmod n] = A[i]$) using reversal steps and prove its correctness.

---

## 7.5 Chapter Synthesis
Arrays are the bedrock of systems programming because they mirror the physical layout of hardware memory. Understanding cache line alignment, spatial locality, and in-place invariants transforms you from an abstract coder into a true systems-aware engineer.

In **Chapter 8**, we expand into **Strings, Encodings, and In-Place Sequence Manipulation**, analyzing UTF-8 variable-length encodings, sliding character buffers, and palindrome invariants.
