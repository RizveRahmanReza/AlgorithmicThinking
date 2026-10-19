# THE ALGORITHMIC DECISION FRAMEWORK (ADF)

The **Algorithmic Decision Framework (ADF)** is the core mental methodology taught throughout *The Art of Algorithmic Thinking*. Instead of guessing or pattern-matching by keyword, engineers evaluate computational problems systematically using twenty foundational diagnostic vectors.

---

## The 20 Diagnostic Questions

### 1. Problem Classification & Output Nature
- **Q1: What is the formal computational objective?**
  - Search (find instance), Optimization (minimize/maximize cost function), Decision (Yes/No boolean), Enumeration (generate all configurations), or Counting (compute cardinality)?
- **Q2: Does exact optimality matter, or is an approximation/probabilistic result sufficient?**
  - If exact: DP, Branch & Bound, Greedy, Flow.
  - If approximation acceptable: Heuristics, $\alpha$-approximation, Monte Carlo, randomized sketch.

### 2. Data Properties & Layout
- **Q3: What is the input domain, scale, and distribution?**
  - Input size $N$: Is $N \le 20$ (exponential $O(2^N)$), $N \le 500$ ($O(N^3)$), $N \le 10^5$ ($O(N \log N)$), or $N \ge 10^7$ ($O(N)$ or $O(\log N)$)?
- **Q4: Is the input static or continuously modified (dynamic)?**
  - Static: Precompute with Prefix Sums, Sparse Tables, Suffix Arrays.
  - Dynamic: Segment Trees, Balanced BSTs, Skip Lists, B-Trees.
- **Q5: Is data ordered, sorted, or partially ordered?**
  - If sorted or monotonic: Binary Search, Two Pointers, Sweep-Line.
  - If unsorted: Hash Tables, Sorting pre-pass, Heaps.
- **Q6: Are duplicate values allowed, and what do they signify?**
  - Multiset vs. Set semantics, stability requirement in sorting.

### 3. Workload Dynamics & Access Patterns
- **Q7: What is the read-to-write ratio?**
  - Read-heavy: Contiguous flat arrays, immutable compressed structures, B+ Trees.
  - Write-heavy: Log-structured Merge-Trees (LSM), Append-only logs, Doubly-linked lists.
- **Q8: Is random access required, or is sequential stream access sufficient?**
  - Random access: Contiguous arrays, Hash Tables ($O(1)$ amortized).
  - Sequential: Stacks, Queues, Iterators, File streams.
- **Q9: Are queries single-point or range-based?**
  - Single-point: Hash Map, Trie.
  - Range-based: Fenwick Tree, Segment Tree, Interval Tree, B-Tree.
- **Q10: Is the workload offline (all queries known upfront) or online (queries answered sequentially)?**
  - Offline: Coordinate compression, Mo's Algorithm, static Sweep-Line.
  - Online: Persistent Segment Trees, Dynamic Graph algorithms.

### 4. Structural Relations & Invariants
- **Q11: Can the problem be mapped to a graph or tree topology?**
  - Peer-to-peer relationships: General Graph (DFS/BFS, Shortest Path).
  - Strict hierarchy or dependency order: DAG (Topological Sort), Tree (Tree DP, LCA).
- **Q12: Does the problem exhibit optimal substructure and overlapping subproblems?**
  - Yes: Dynamic Programming.
  - Substructure without overlapping: Divide and Conquer.
- **Q13: Does a local greedy choice provably yield global optimality?**
  - Prove via Exchange Argument or Matroid theory. If proof fails, switch immediately to Dynamic Programming or Search.
- **Q14: What mathematical invariant remains invariant across transformations?**
  - Parity, conservation of sum, monotonic stack property, loop invariant.

### 5. Systems, Memory, and Latency Constraints
- **Q15: What is the strict memory budget?**
  - In-place $O(1)$ auxiliary space needed? Or is $O(N)$ space acceptable?
- **Q16: How does the algorithm interact with CPU cache hierarchies?**
  - Cache-friendly contiguous flat vectors vs. Cache-hostile pointer-chasing linked lists/trees.
- **Q17: Is worst-case latency critical (hard real-time)?**
  - If real-time: Disallow resizing hash tables with $O(N)$ rehash spikes or unbounded QuickSort recursion; prefer deterministic $O(\log N)$ AVL/Red-Black or fixed-capacity ring buffers.
- **Q18: Is deterministic execution required?**
  - Avoid unseeded randomized algorithms; ensure reproducible execution paths.
- **Q19: Does the workload involve parallel execution or concurrency?**
  - Lock-free queues, read-copy-update (RCU), partitioned sharding, atomic operations.
- **Q20: What are the failure modes, edge boundaries, and adversarial inputs?**
  - Empty sets, single elements, integer overflow ($N \times M > 2^{31}-1$), hash collision attacks.

---

## The ADF Decision Matrix (High-Level Summary)

| Query / Constraint | Primary Family | Preferred Structures | Avoid |
| :--- | :--- | :--- | :--- |
| Dynamic Range Sum | Range Query | Fenwick Tree, Segment Tree | Repeated Linear Scan ($O(N)$ per query) |
| Monotonic Extremum in Window | Monotonic Queue / Deque | Deque storing indices | Re-scanning Window ($O(K)$) |
| Range Minimum on Static Array | Static Query | Sparse Table ($O(1)$ query, $O(N \log N)$ build) | Recomputed Segment Tree |
| Graph Shortest Path (non-negative) | Graph Search | Dijkstra with Min-Heap ($O((V+E)\log V)$) | Bellman-Ford ($O(VE)$) |
| High-Write Throughput DB | System Indexing | LSM-Tree (Append-only + Compaction) | Direct B-Tree Random Disk Writes |
| Memory-Constrained Real-Time | Embedded / Deterministic | Static Flat Array / Ring Buffer | Dynamic Allocations (`malloc`/`new`) |
