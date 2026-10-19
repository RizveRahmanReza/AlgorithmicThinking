# CHAPTER 2: REQUIREMENTS ANALYSIS, CONSTRAINTS, AND INVARIANTS

> *"A problem well-stated is a problem half-solved. An unstated constraint is an ambush in production."*

---

## 2.1 Translating Real-World Requirements into Mathematical Formalisms

In commercial software development, competitive programming, and research, requirements rarely arrive in algebraic terms. They arrive as business logic, feature requests, or user complaints:
- *"Ensure no user starves for resources when the cluster experiences peak load."*
- *"Allow the analytics engine to query sliding windows without freezing the interface."*
- *"Schedule maintenance jobs such that machine reboot downtime does not overlap."*

Each of these statements is riddled with **informal semantics**. To an algorithm designer, the words "starves", "freezing", and "downtime" have no operational meaning until they are mapped into mathematical domains: sets, bounds, metrics, relations, and cost functions.

### The Formalization Funnel
The translation from an informal prompt to an executable algorithm requires four discrete formalization steps:

```
+-------------------------------------------------------------+
| 1. Disambiguation                                           |
| Identify implicit assumptions and eliminate ambiguous terms. |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 2. Domain & Codomain Binding                                |
| Cast entities into mathematical objects:                     |
| Elements -> Z, R; Timestamps -> Discrete T; Jobs -> Tuples   |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 3. Invariant & Objective Specification                      |
| Define the objective function f(x) and validity predicate P  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| 4. Complexity & Resource Budgets                            |
| Relate input cardinality N to physical CPU/memory envelopes |
+-------------------------------------------------------------+
```

### Case in Point: What Does "Fairness" Mean?
Consider the informal request: *"Allocate incoming network bandwidth fairly among connected sessions."*
- Does fairness mean **Equal Division**? Every session receives exactly $C / K$ bandwidth, regardless of whether a low-power IoT device needs only 10 KB/s, thereby wasting remaining capacity?
- Does it mean **Max-Min Fairness**? No session gets more than its demand, and no session with unsatisfied demand gets less than any other session?
- Does it mean **Proportional Fairness**? Bandwidth is allocated proportionally to a priority weight $w_i$?

Unless the software engineer formalizes this definition upfront, any algorithm implemented will be arbitrary, unverifiable, and brittle.

---

## 2.2 Finding Hidden Constraints: Time, Space, Monotonicity, and Invertibility

A constraint is not merely a restriction; **a constraint is an algorithmic clue**. 

Every constraint you discover narrows the permissible search space and rules out entire categories of inefficient algorithms. Experienced algorithmic thinkers actively hunt for four categories of hidden constraints:

### 1. The Monotonicity Constraint
If a property $P(k)$ has the characteristic that:
$$\forall k, \quad P(k) = \text{True} \implies P(k+1) = \text{True} \quad (\text{or } P(k+1) = \text{False})$$
then the solution space is **monotonic**. 
*Implication*: Monotonicity is the mathematical prerequisite for **Binary Search**. Instead of an exhaustive linear scan of size $M$ requiring $\mathcal{O}(M)$ time, monotonicity allows you to discard half the search space at each probe, reducing the cost to $\mathcal{O}(\log M)$.

### 2. The Invertibility Constraint
Can an operation be undone in $\mathcal{O}(1)$ time?
- **Addition** has an inverse (**Subtraction**). Therefore, range sums over a static array can be answered in $\mathcal{O}(1)$ time using a **Prefix Sum Array**: $\sum_{k=L}^R A[k] = P[R] - P[L-1]$.
- **Bitwise XOR** is its own inverse ($x \oplus x = 0$). Range XOR queries can likewise be answered in $\mathcal{O}(1)$ with a prefix XOR array.
- **Range Minimum Queries ($\min$)** and **Greatest Common Divisor ($\gcd$)** are *idempotent* ($x \circ x = x$) but *not invertible*. You cannot "subtract" an element from a minimum. Therefore, prefix sums cannot support range minimums; one must turn to **Sparse Tables** or **Segment Trees**.

### 3. The Conservation / Invariance Constraint
In physical, financial, and distributed systems, total quantities (energy, currency balance, total particle count) are often conserved:
$$\sum_{i=1}^n x_i^{(t)} = C \quad \forall t$$
Recognizing that a system state satisfies a conservation law allows you to compute the state of the $n$-th entity as $x_n = C - \sum_{i=1}^{n-1} x_i$ without additional queries, transforming an $n$-dimensional state into an $(n-1)$-dimensional state space.

### 4. Hardware and Computational Budgets
Every algorithm executes on physical silicon bound by hardware realities:
- Modern CPU cores execute approximately $10^8$ to $10^9$ basic operations per second.
- L1 Data Cache latency is $\approx 1$ ns; main memory (DRAM) latency is $\approx 50$ to $100$ ns.
- If $N = 10^5$, an algorithm requiring $\mathcal{O}(N^2) = 10^{10}$ operations will take roughly 10 to 30 seconds to finish—violating typical interactive response deadlines ($\le 1.0$ s). Only algorithms of complexity $\mathcal{O}(N \log N)$ or $\mathcal{O}(N)$ can survive this operational budget.

---

## 2.3 Designing Edge Cases and Adversarial Tests Before Writing Code

The amateur programmer writes code first and tests it on a single sunny-day example. The professional algorithm designer builds the **adversarial test suite** before typing the first line of the implementation.

### The Anatomy of Adversarial Testing
Adversarial inputs are instances specifically constructed to exploit boundary conditions, numerical limits, or structural degeneracies in naive algorithms:

1. **Extreme Cardinalities**:
   - $N = 0$ (empty collection — does the code crash with a segmentation fault or `IndexError`?)
   - $N = 1$ (single element — do loops execute zero times when they should execute once?)
   - $N = N_{\max}$ (maximum theoretical capacity — does memory consumption stay within budget?)
2. **Extreme Magnitudes**:
   - Elements at $0$, $\pm 1$, $\pm 10^9$, or $2^{31}-1$.
   - Quantities whose sums overflow 32-bit signed integers and require 64-bit (`int64_t`) arithmetic.
3. **Structural Degeneracies**:
   - **All Identical Elements**: Arrays where every element is the same (`[7, 7, 7, 7]`). Causes naive QuickSort implementations with bad pivot choices to degrade to $\mathcal{O}(N^2)$.
   - **Strictly Monotonic Inputs**: Already-sorted or reverse-sorted sequences.
   - **Alternating / Zig-Zag Sequences**: `[1, 10^9, 1, 10^9, 1]`.
   - **Disconnected or Path-Degenerate Graphs**: Trees that are long chains of single nodes (degenerating tree depth from $\mathcal{O}(\log N)$ to $\mathcal{O}(N)$ and blowing up the call stack).

---

## 2.4 The Technique of Counterexample Construction

When someone proposes an intuitive heuristic or greedy strategy, how do you verify whether it is universally correct? 
**You do not attempt to prove it true by listing examples where it works. You deliberately attempt to destroy it with a minimal counterexample.**

### The Counterexample Protocol
1. **Identify the Core Assumption**: What unproven assumption makes the greedy heuristic feel plausible? (e.g., *"Choosing the element with the largest immediate value will leave the most room for remaining elements."*)
2. **Isolate the Deception**: Construct an instance where the greedy choice provides an immediate small gain but blocks a substantially larger combined payoff immediately downstream.
3. **Minimize the Instance**: Shrink the counterexample to the smallest possible cardinality (often $N = 2, 3,$ or $4$). A 3-element counterexample is an airtight mathematical refutation that cannot be disputed.

---

## 2.5 Worked Problem: SOLV-0002 — Stable Resource Allocation Under Capacity Constraints

Let us now apply the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify a foundational problem in discrete resource management.

---

### Step 1: Real-World Motivation
In high-throughput cloud infrastructure (e.g., Kubernetes pod scheduling, AWS EC2 spot instance orchestration), customer workloads arrive with specific compute-capacity demands, start times, and execution durations. The cluster has a fixed total compute capacity $C$. 

If jobs are admitted blindly on a first-come, first-served basis, high-demand short jobs can monopolize the system, or jobs scheduled improperly can create capacity oversubscription, crashing the hypervisor node. The orchestration engine must determine the maximum number of requests that can be scheduled concurrently without at any point exceeding the cluster's physical resource ceiling.

### Step 2: Problem Identification
Formally, this problem maps to the **Interval Scheduling with Shared Discrete Capacity**. Given a collection of weighted time intervals and a constant capacity $C$, find a subset of intervals that maximizes utility (or in the foundational variant, verify whether a proposed allocation is feasible without violating the capacity invariant at any instant in time).

In this foundational chapter, we formalize the fundamental decision kernel: **Verifying and Identifying Resource Satiation across Dynamic Interval Allocations**.

### Step 3: Formal Problem Statement
Let $\mathcal{J} = \{J_1, J_2, \dots, J_n\}$ be a set of $n$ job requests.
Each job $J_k$ is represented as a triple:
$$J_k = (s_k, e_k, c_k)$$
where:
- $s_k \in \mathbb{Z}_{\ge 0}$ is the inclusive start timestamp.
- $e_k \in \mathbb{Z}_{\ge 0}$ is the exclusive end timestamp ($s_k < e_k$).
- $c_k \in \mathbb{Z}_{> 0}$ is the discrete capacity consumed continuously over the half-open interval $[s_k, e_k)$.

Given a global maximum capacity threshold $C \in \mathbb{Z}_{> 0}$:
1. Determine whether the scheduled allocation is **strictly feasible** (i.e., at all times $t \ge 0$, the sum of capacities of active jobs does not exceed $C$):
   $$\forall t \ge 0, \quad \sum_{k: s_k \le t < e_k} c_k \le C$$
2. Identify the **peak capacity utilization** $C_{\text{peak}} = \max_{t \ge 0} \sum_{k: s_k \le t < e_k} c_k$.
3. If $C_{\text{peak}} > C$, return the earliest timestamp $t_{\text{violation}}$ at which capacity was breached.

#### Constraints:
- Number of jobs: $1 \le n \le 2 \times 10^5$
- Timestamps: $0 \le s_k < e_k \le 10^9$
- Job capacities: $1 \le c_k \le 10^9$
- Global capacity: $1 \le C \le 10^{15}$
- Time limit: 1.0 second.
- Auxiliary space budget: $\mathcal{O}(n)$.

### Step 4: Thinking Before Coding
1. **Notice the scale of timestamps**: Timestamps reach $10^9$. A naive time-array simulation indexed by $t$ (`array[t] += c_k`) would require an array of size $10^9$, demanding multiple gigabytes of memory and taking billions of iterations. **Direct timeline simulation is impossible.**
2. **Notice the scale of capacity**: $C \le 10^{15}$, and each job capacity can be $10^9$. The sum can easily exceed $2^{31}-1$. **All capacity calculations must use 64-bit integers (`int64_t` in C++, arbitrary-precision `int` in Python).**
3. **What happens at the boundaries?** The interval is half-open $[s_k, e_k)$. If job $A$ ends at timestamp 5 ($e_A = 5$) and job $B$ starts at timestamp 5 ($s_B = 5$), their allocations **do not overlap**. Job $A$ releases its capacity *before* (or simultaneously with) job $B$ acquiring its capacity at $t = 5$.

### Step 5: First-Principles Reasoning
Does capacity change continuously at every real number $t$?
**No.** The active capacity remains strictly constant during any interval between successive job boundary events. 
Capacity *only changes* when:
- A job starts: Capacity increases by $+c_k$.
- A job finishes: Capacity decreases by $-c_k$.

Between discrete start and end events, nothing changes. Therefore, continuous time is irrelevant. We only need to examine the **finite sequence of discrete transition points** where jobs start or finish.

Since each of the $n$ jobs has exactly one start event and one end event, there are at most $2n$ critical event timestamps in total!

### Step 6: Brute-Force Implementation
A naive baseline would check every distinct job start timestamp $s_i$ and recompute the active capacity from all $n$ jobs:

```python
# Educational Reference Baseline: O(n^2)
def check_capacity_naive(jobs: list[tuple[int, int, int]], C: int):
    # Extract all distinct start times
    critical_times = sorted(set(job[0] for job in jobs))
    max_utilization = 0
    
    for t in critical_times:
        current_load = 0
        for s, e, c in jobs:
            if s <= t < e:
                current_load += c
        if current_load > max_utilization:
            max_utilization = current_load
        if current_load > C:
            return False, max_utilization, t
            
    return True, max_utilization, None
```

### Step 7: Bottleneck Analysis
Why is the baseline slow?
For each of the $\le n$ critical timepoints, it iterates over all $n$ jobs, producing $\mathcal{O}(n^2)$ total operations. For $n = 2 \times 10^5$, $n^2 = 4 \times 10^{10}$ operations, which requires over 40 seconds—violating our 1-second budget.

The redundancy is obvious: when moving from timestamp $t_a$ to the subsequent timestamp $t_b$, the vast majority of jobs have not changed state! Re-scanning every job from scratch throws away all previous knowledge.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Space Complexity | Viable for $N = 2 \times 10^5$? | Critical Assessment |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Timeline Simulation** | $\mathcal{O}(\max(e_k))$ | $\mathcal{O}(\max(e_k))$ | No | $10^9$ array indices; Out Of Memory |
| **All-Points Re-scan (Naive)** | $\mathcal{O}(n^2)$ | $\mathcal{O}(n)$ | No | $4 \times 10^{10}$ ops; exceeds latency budget |
| **Interval Tree / Segment Tree** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | Yes | Viable, but excessive code complexity |
| **Sweep-Line Event Processing** | $\mathcal{O}(n \log n)$ | $\mathcal{O}(n)$ | **Optimal** | Minimal code, cache-friendly flat array, clean invariants |

### Step 9: Derivation of the Improved Algorithm (Sweep-Line Paradigm)
Instead of querying intervals at arbitrary times, imagine an imaginary vertical line "sweeping" across the timeline from left to right ($t = -\infty \to +\infty$).

1. Decompose each job $J_k = (s_k, e_k, c_k)$ into two discrete **Events**:
   - `Event(time = s_k, delta = +c_k, type = START)`
   - `Event(time = e_k, delta = -c_k, type = END)`
2. Collect all $2n$ events into a single linear sequence.
3. **Sorting Invariant**:
   Sort all events in ascending order of timestamp.
   *What if an END event and a START event occur at the exact same timestamp $T$?*
   Because intervals are $[s_k, e_k)$, the job ending at $T$ frees its resources before the job starting at $T$ claims its resources. 
   **Crucial Rule**: In ties of identical timestamps, process `END` events before `START` events!
4. Traverse the sorted events sequentially. Maintain a running variable `current_capacity`.
   At each event: `current_capacity += event.delta`.
   Update `peak_capacity = max(peak_capacity, current_capacity)`.
   If `current_capacity > C`, record the violation immediately.

### Step 10: Correctness Proof

#### Invariant:
Let $E = [e_1, e_2, \dots, e_{2n}]$ be the sorted sequence of events.
Before processing event $e_m = (t_m, \Delta_m)$:
1. `current_capacity` is strictly equal to the exact active capacity consumed by all jobs currently active in the interval immediately preceding $t_m$.
2. `peak_capacity` is the maximum capacity attained across all points in time up to and including the most recently processed event group.

#### Base Case:
At $t = -\infty$ (before event $e_1$), no jobs are active. `current_capacity = 0`, `peak_capacity = 0`. The invariant holds.

#### Inductive Step:
Assume the invariant holds prior to processing the cluster of all events occurring at timestamp $T$.
- All jobs ending at $T$ have their delta $-c_k$ applied first. `current_capacity` accurately decreases by the exact freed capacity.
- All jobs starting at $T$ have their delta $+c_k$ applied next. `current_capacity` accurately increases by the newly allocated capacity.
- Since capacity is piecewise constant between event timestamps, the value of `current_capacity` after processing all events at timestamp $T$ equals $\sum_{k: s_k \le T < e_k} c_k$.
- The global maximum `peak_capacity` correctly updates to $\max(\text{peak\_capacity}, \text{current\_capacity})$.

#### Termination:
When all $2n$ events have been processed, every job that was started has also ended, returning `current_capacity` to 0. `peak_capacity` holds the true maximum of active capacity across the entire timeline $\mathbb{R}$. $\blacksquare$

### Step 11: Step-by-Step Dry Run

Consider $C = 15$ and 3 jobs:
- $J_1 = (1, 5, 10)$
- $J_2 = (2, 8, 4)$
- $J_3 = (5, 9, 3)$

Generated Events:
- $(1, +10)$ [Start $J_1$]
- $(5, -10)$ [End $J_1$]
- $(2, +4)$ [Start $J_2$]
- $(8, -4)$ [End $J_2$]
- $(5, +3)$ [Start $J_3$]
- $(9, -3)$ [End $J_3$]

Notice at $t = 5$, we have both an End event for $J_1$ and a Start event for $J_3$. By our tie-break rule, the End event MUST be processed first.

Sorted Event Stream:
1. $t=1$: Start $J_1$ ($\Delta = +10$)
2. $t=2$: Start $J_2$ ($\Delta = +4$)
3. $t=5$: End $J_1$ ($\Delta = -10$)
4. $t=5$: Start $J_3$ ($\Delta = +3$)
5. $t=8$: End $J_2$ ($\Delta = -4$)
6. $t=9$: End $J_3$ ($\Delta = -3$)

| Step | Timestamp $t$ | Event Type | Delta $\Delta$ | `current_capacity` | `peak_capacity` | Invariant Check $\le 15$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Init | — | — | — | 0 | 0 | True |
| 1 | 1 | Start $J_1$ | $+10$ | 10 | 10 | True ($10 \le 15$) |
| 2 | 2 | Start $J_2$ | $+4$ | 14 | **14** | True ($14 \le 15$) |
| 3 | 5 | End $J_1$ | $-10$ | 4 | 14 | True ($4 \le 15$) |
| 4 | 5 | Start $J_3$ | $+3$ | 7 | 14 | True ($7 \le 15$) |
| 5 | 8 | End $J_2$ | $-4$ | 3 | 14 | True ($3 \le 15$) |
| 6 | 9 | End $J_3$ | $-3$ | 0 | 14 | True ($0 \le 15$) |

**Final Output**: Allocation is feasible (`True`), Peak Capacity = 14, Violation Time = `None`.
*(Note: Had we processed Start $J_3$ before End $J_1$ at $t = 5$, `current_capacity` would have spuriously spiked to $14 + 3 = 17 > 15$, triggering a false violation! This confirms the necessity of our tie-breaking proof).*

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/SOLV-0002.cpp
#include <iostream>
#include <vector>
#include <cstdint>
#include <algorithm>
#include <span>
#include <optional>
#include <cassert>

struct JobRequest {
    int64_t start_time;
    int64_t end_time;
    int64_t capacity;
};

struct AllocationAudit {
    bool is_feasible;
    int64_t peak_capacity;
    std::optional<int64_t> first_violation_time;
};

// Event representation for Sweep-Line
struct ResourceEvent {
    int64_t timestamp;
    int64_t capacity_delta; // Negative for release, positive for acquisition

    // Tie-break invariant: if timestamps are identical, process negative deltas (releases) first
    bool operator<(const ResourceEvent& other) const noexcept {
        if (timestamp != other.timestamp) {
            return timestamp < other.timestamp;
        }
        return capacity_delta < other.capacity_delta;
    }
};

/**
 * Audits interval resource allocation using an O(N log N) sweep-line algorithm.
 * Conforms to ISO C++20 standard.
 */
AllocationAudit audit_resource_allocation(
    std::span<const JobRequest> jobs, 
    int64_t global_capacity
) {
    std::vector<ResourceEvent> events;
    events.reserve(jobs.size() * 2);

    for (const auto& job : jobs) {
        if (job.start_time >= job.end_time || job.capacity <= 0) {
            throw std::invalid_argument("Invalid job parameters: must have start < end and capacity > 0.");
        }
        events.push_back(ResourceEvent{job.start_time, job.capacity});
        events.push_back(ResourceEvent{job.end_time, -job.capacity});
    }

    std::sort(events.begin(), events.end());

    int64_t current_capacity = 0;
    int64_t peak_capacity = 0;
    std::optional<int64_t> violation_time = std::nullopt;

    for (const auto& ev : events) {
        current_capacity += ev.capacity_delta;

        if (current_capacity > peak_capacity) {
            peak_capacity = current_capacity;
        }

        if (current_capacity > global_capacity && !violation_time.has_value()) {
            violation_time = ev.timestamp;
        }
    }

    return AllocationAudit{
        .is_feasible = !violation_time.has_value(),
        .peak_capacity = peak_capacity,
        .first_violation_time = violation_time
    };
}
```

### Step 13: Full Python Implementation

```python
# solutions/python/SOLV-0002.py
from typing import Sequence, NamedTuple, Optional


class JobRequest(NamedTuple):
    start_time: int
    end_time: int
    capacity: int


class AllocationAudit(NamedTuple):
    is_feasible: bool
    peak_capacity: int
    first_violation_time: Optional[int]


def audit_resource_allocation(
    jobs: Sequence[JobRequest], 
    global_capacity: int
) -> AllocationAudit:
    """
    Evaluates dynamic capacity allocation feasibility using a Sweep-Line algorithm.
    Target: Python 3.12+ (O(N log N) time, O(N) auxiliary space).
    
    Invariant:
    Sorting ensures events at timestamp T with negative deltas (releases)
    are processed before events with positive deltas (allocations).
    """
    events: list[tuple[int, int]] = []
    for job in jobs:
        if job.start_time >= job.end_time or job.capacity <= 0:
            raise ValueError("Job must satisfy start_time < end_time and capacity > 0.")
        events.append((job.start_time, job.capacity))
        events.append((job.end_time, -job.capacity))

    # Sort key: primary = timestamp ASC, secondary = delta ASC
    # Negative delta sorts before positive delta for identical timestamps
    events.sort(key=lambda ev: (ev[0], ev[1]))

    current_capacity: int = 0
    peak_capacity: int = 0
    first_violation: Optional[int] = None

    for timestamp, delta in events:
        current_capacity += delta

        if current_capacity > peak_capacity:
            peak_capacity = current_capacity

        if current_capacity > global_capacity and first_violation is None:
            first_violation = timestamp

    return AllocationAudit(
        is_feasible=(first_violation is None),
        peak_capacity=peak_capacity,
        first_violation_time=first_violation
    )
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\Theta(n \log n)$
  - Generating events: $\Theta(n)$ time to create $2n$ event pairs.
  - Sorting events: $\Theta(n \log n)$ time using Introsort in C++ (`std::sort`) or Timsort in Python.
  - Linear scan: $\Theta(n)$ to iterate through $2n$ events with $\mathcal{O}(1)$ scalar arithmetic.
  - **Dominant term**: $\Theta(n \log n)$, perfectly fitting well within the 1.0 second envelope for $n = 2 \times 10^5$.
- **Space Complexity (Auxiliary)**: $\Theta(n)$
  - Storage for $2n$ event tuples in memory. 
  - For $n = 2 \times 10^5$, $4 \times 10^5$ events in C++ require $4 \times 10^5 \times 16 \text{ bytes} \approx 6.4 \text{ MB}$, trivially fitting within any embedded or server L3 cache/RAM budget.

### Step 15: Edge Cases and Failure Modes
1. **Zero-Duration Job**: If an input has $s_k = e_k$, the duration is 0. Our code rejects this in parameter validation, as instantaneous jobs with zero duration violate continuous operational semantics.
2. **Abutting Intervals**: Job $A$ ends at $t=10$, Job $B$ starts at $t=10$. Because `capacity_delta` is negative for releases, $-c_A$ sorts before $+c_B$. The capacity is cleanly returned before being claimed.
3. **Capacity Overflow**: Global capacity $C = 10^{15}$. In languages with 32-bit integers, this overflows into negative numbers. Explicit 64-bit integer types prevent undefined overflow behavior.
4. **All Intervals Completely Disjoint**: $n$ jobs spaced out with no temporal overlap. Complexity remains $\mathcal{O}(n \log n)$; peak capacity is correctly reported as $\max(c_k)$.

### Step 16: Test Cases & Validation Suite
- **T1 (Standard Feasible)**: $C = 15$; Jobs: `[(1, 5, 10), (2, 8, 4), (5, 9, 3)]` $\to$ Feasible: `True`, Peak: `14`, Violation: `None`.
- **T2 (Boundary Abutting No Overlap)**: $C = 10$; Jobs: `[(1, 5, 10), (5, 10, 10)]` $\to$ Feasible: `True`, Peak: `10`, Violation: `None`.
- **T3 (Capacity Breach)**: $C = 12$; Jobs: `[(1, 5, 10), (2, 6, 5)]` $\to$ Feasible: `False`, Peak: `15`, Violation: `2`.
- **T4 (Simultaneous Breaches)**: Multiple jobs starting at the exact same timestamp causing immediate breach.
- **T5 (Extreme Timestamps)**: $s_k = 0, e_k = 10^9$. Handled without memory dilation.

### Step 17: Real-World Engineering Application
This Sweep-Line technique is the foundational engine inside:
- **Cloud Hypervisors**: KVM and Xen schedulers tracking RAM and vCPU overcommit ratios.
- **Flight Reservation Systems**: Verifying seat inventory for multi-leg passenger journeys.
- **EDA & VLSI Chip Design**: Detecting electrical trace wire overlaps and capacitance hot-spots across physical layout coordinates.

### Step 18: Further Optimization
- If timestamps are already bounded in a small integer range $[0, U]$ where $U \le 10^6$, one can use a **Difference Array** and a prefix sum pass to achieve true $\mathcal{O}(n + U)$ linear time, bypassing the $\mathcal{O}(n \log n)$ comparison sort.
- For dynamic workloads where jobs are continuously added and cancelled online, a **Segment Tree with Lazy Propagation** allows updates and range capacity queries in $\mathcal{O}(\log U)$ time per operation.

### Step 19: Related Patterns
- **Sweep-Line Geometry**: Closely connected to finding the area of intersecting rectangles in 2D plane geometry.
- **Meeting Rooms & Interval Coloring**: Minimum rooms required to hold all meetings equals $C_{\text{peak}}$ when each job requires capacity $c_k = 1$.

### Step 20: Reader Challenges
1. **Challenge 2.1 (Maximum Non-Overlapping Subset)**: Given $n$ jobs with values $v_k$, find the subset of mutually non-overlapping jobs that maximizes total value. Prove why simple greedy scheduling works when all values are equal ($v_k = 1$), but fails when values differ, requiring dynamic programming.
2. **Challenge 2.2 (Dynamic Job Cancellation)**: Extend the system to support dynamic cancellations of previously scheduled jobs in $\mathcal{O}(\log n)$ time. *(Hint: Investigate Fenwick Trees or Segment Trees).*

---

## 2.6 Summary & Next Steps
Requirements analysis is the bridge between human ambiguity and algorithmic execution. By extracting constraints, proving invariants, and building adversarial tests first, you eliminate entire classes of fatal production bugs before writing code.

In **Chapter 3**, we will tackle **Brute Force, Search Spaces, and Bottleneck Analysis**, demonstrating how to formalize exponential combinatorial explosions and systematically engineer them down to polynomial time.
