# CHAPTER 24: GRAPH REPRESENTATIONS AND BASIC TRAVERSALS (BFS AND DFS)

> *"Trees are graphs shackled by hierarchy and acyclicity. A general graph unshackles topology: cycles emerge, multiple paths intertwine, and connectivity becomes a labyrinth. Breadth-First Search radiates outward in concentric wavefronts to establish shortest paths, while Depth-First Search plunges along backtracking tendrils, classifying edges and unearthing the fundamental topological skeletons of networks."*

---

## 24.1 Graph Foundations and Representation Trade-Offs

A **graph** $G = (V, E)$ consists of a set of vertices $V$ and a set of edges $E \subseteq V \times V$.
- **Directed Graph (Digraph)**: Edges are ordered pairs $(u, v)$ directed from $u$ to $v$.
- **Undirected Graph**: Edges are unordered pairs $\{u, v\}$, equivalent to bidirectional directed edges.
- Let $|V| = N$ and $|E| = M$. In a simple graph without self-loops: $0 \le M \le \binom{N}{2} \approx \frac{N^2}{2}$.

### Physical Memory Representations

| Representation | Memory Complexity | Edge Existence $(u, v)$ | Iterate Out-Neighbors of $u$ | Cache Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Adjacency Matrix** $M[N][N]$ | $\Theta(N^2)$ | $\Theta(1)$ | $\Theta(N)$ | Excellent spatial locality, but disastrous memory for sparse graphs |
| **Adjacency List** `vector<vector<int>>` | $\Theta(N + M)$ | $O(\text{deg}(u))$ | $\Theta(\text{deg}(u))$ | Optimal memory; pointer chasing across separate dynamic vectors |
| **Compressed Sparse Row (CSR)** | $\Theta(N + M)$ | $O(\log \text{deg}(u))$ | $\Theta(\text{deg}(u))$ | **Optimal memory & optimal L1 cache locality** (two contiguous flat arrays) |

```
Compressed Sparse Row (CSR) Representation:
Vertices: 0, 1, 2, 3
Edges: (0->1), (0->2), (1->2), (2->0), (2->3), (3->1)

row_ptr: [ 0,     2,     3,          5,     6 ]  (Length N + 1)
col_idx: [ 1, 2,  2,     0, 3,       1 ]        (Length M)
           ^---^  ^      ^---^       ^
           deg 0  deg 1  deg 2       deg 3
```
In high-performance graph computing (e.g. GraphBLAS, PageRank engines), CSR eliminates memory fragmentation entirely: all edges for vertex $u$ reside in contiguous memory from `col_idx[row_ptr[u]]` to `col_idx[row_ptr[u+1] - 1]`.

---

## 24.2 Breadth-First Search (BFS): Concentric Wavefronts

BFS explores vertices in increasing order of their distance from the source vertex $s$, using a FIFO queue.

### The BFS Invariant
When node $u$ at distance $d(s, u) = k$ is processed:
1. All vertices at distance $< k$ have already been popped and finalized.
2. The queue contains vertices of distance $k$ followed by vertices of distance $k + 1$.
3. At no point does the queue contain vertices whose distances differ by more than $1$.

```
Concentric Distance Wavefronts:
       [ Level 0: Source s ]
                 |
       [ Level 1: Neighbors of s ]
                 |
       [ Level 2: Neighbors of Level 1 ]
                 |
       [ Level 3: ... ]
```

### Shortest Path Optimality
In an unweighted graph, BFS computes the **exact single-source shortest path** $\delta(s, v)$ to all reachable vertices in strictly $\Theta(V + E)$ time.

---

## 24.3 Depth-First Search (DFS): Backtracking and Edge Classification

DFS explores deeply along each branch before backtracking, utilizing an explicit or recursive LIFO stack.

### Discovery and Finish Times (Parenthesis Theorem)
For each vertex $u$, record:
- $d[u]$: Timestamp when $u$ is first discovered (colored Gray).
- $f[u]$: Timestamp when all neighbors of $u$ have been searched (colored Black).

```
Parenthesis Theorem (CLRS):
For any two vertices u and v, exactly one of three conditions holds:
1. [d[u], f[u]] and [d[v], f[v]] are completely disjoint (neither is an ancestor of the other).
2. [d[u], f[u]] is strictly contained within [d[v], f[v]] (u is a descendant of v in the DFS tree).
3. [d[v], f[v]] is strictly contained within [d[u], f[u]] (v is a descendant of u in the DFS tree).
```

### The Four DFS Edge Classes
When edge $(u, v)$ is traversed during DFS:
1. **Tree Edge**: Leads to an undiscovered vertex $v$ ($v$ is White). Adds edge to DFS spanning forest.
2. **Back Edge**: Leads to an ancestor $v$ currently on the recursion stack ($v$ is Gray).
   - **Fundamental Theorem**: A directed graph contains a cycle if and only if DFS reveals at least one **Back Edge**!
3. **Forward Edge**: Leads to a descendant $v$ already completed ($v$ is Black, $d[u] < d[v]$).
4. **Cross Edge**: Leads to an unrelated node already completed ($v$ is Black, $d[u] > d[v]$).

---

## 24.4 Bipartiteness and 2-Colorability

A graph $G = (V, E)$ is **bipartite** if its vertex set can be partitioned into two disjoint sets $V_1$ and $V_2$ such that every edge connects a vertex in $V_1$ to a vertex in $V_2$:
$$e = (u, v) \in E \implies (u \in V_1 \land v \in V_2) \lor (u \in V_2 \land v \in V_1)$$

### Theorem (Kőnig, 1936)
A graph is bipartite if and only if it contains **no odd-length cycles**.

- *Proof Idea ($\implies$)*: Suppose $G$ is bipartite. Any path must strictly alternate between $V_1$ and $V_2$. To return to the starting vertex, the path must make an even number of hops. Thus, all cycles must have even length.
- *Proof Idea ($\impliedby$)*: Run BFS from an arbitrary root. Assign vertices at even distance $d(s, v)$ to $V_1$ (Color 0) and vertices at odd distance to $V_2$ (Color 1). If an edge exists between two vertices at the same color, their paths to their Lowest Common Ancestor along the BFS tree, together with the cross-edge, form a cycle of odd length $(2k + 1)$. $\blacksquare$

---

## 24.5 The 20-Step Problem Breakdown: Bipartite Verification and 2-Coloring Invariant (`GRPH-0001`)

We now construct a robust, production-grade graph verification engine: testing whether an arbitrary undirected graph (potentially disconnected with self-loops or multi-components) is bipartite, identifying the 2-coloring partition, or isolating an odd-cycle proof certificate.

### Step 1: Real-World Motivation & Context
In compiler register allocation (interference graph coloring), distributed database deadlock conflict detection, medical residency matching (stable matching on two-sided markets), and electronic circuit board dual-layer routing, algorithms must verify if a relationship network can be decoupled into two non-conflicting partitions. If an odd cycle exists, dual-layer scheduling is mathematically impossible.

### Step 2: Formal Problem Specification
- **Requirements**:
  Given an undirected graph of $N$ vertices labeled $0$ to $N - 1$ and an adjacency list:
  1. Return `true` if the graph is bipartite, `false` otherwise.
  2. If bipartite, output a valid 2-coloring array `color` where $\text{color}[u] \in \{0, 1\}$ for all $u$, satisfying:
     $$\forall (u, v) \in E : \text{color}[u] \neq \text{color}[v]$$
  3. Correctly handle disconnected components and isolated vertices.
- **Constraints**:
  - $1 \le N \le 10^5$.
  - $0 \le M \le 2 \times 10^5$.
  - Time complexity: Strictly $\Theta(N + M)$.
  - Auxiliary space: Strictly $O(N)$ memory.

### Step 3: Algorithmic Decision Framework (ADF) Formulation
1. *Graph Type*: Undirected general graph, possibly disconnected.
2. *Decision Target*: Partition into 2 independent sets $\implies$ 2-Coloring problem.
3. *Traversal Paradigm*: BFS or DFS. BFS is preferred because queue-based distance parity directly mirrors Kőnig's theorem without risk of recursion stack overflow on deep linear chains.
4. *Decision*: Multi-source BFS wavefront coloring with state array $\{-1, 0, 1\}$.

### Step 4: Mathematical Invariant Definition
Let $\text{color}[u] \in \{-1, 0, 1\}$:
- $-1$: Unvisited.
- $0$: Partition $V_1$ (Color 0).
- $1$: Partition $V_2$ (Color 1).

**Coloring Invariant**:
For every visited vertex $u$ and every explored neighbor $v \in \text{adj}[u]$:
$$\text{color}[v] = 1 - \text{color}[u]$$
If at any point during traversal a neighbor $v$ is encountered such that:
$$\text{color}[v] == \text{color}[u]$$
Then an odd cycle is detected, violating bipartiteness immediately.

### Step 5: Algorithm Mechanics Across Disconnected Components
1. Initialize $\text{color}[i] = -1$ for all $i \in [0, N-1]$.
2. For each vertex $i \in [0, N-1]$:
   - If $\text{color}[i] == -1$:
     - Set $\text{color}[i] = 0$.
     - Push $i$ to queue $Q$.
     - While $Q$ is not empty:
       - Pop $u = Q.\text{front}()$.
       - For each neighbor $v \in \text{adj}[u]$:
         - If $\text{color}[v] == -1$:
           - Set $\text{color}[v] = 1 - \text{color}[u]$.
           - Push $v$ to $Q$.
         - Else if $\text{color}[v] == \text{color}[u]$:
           - **Return `false`** (Contradiction found!).
3. If all components complete without contradiction, **Return `true`**.

### Step 6: Loop Variant & Complexity Proof
- The outer loop inspects each of the $N$ vertices.
- Each vertex is pushed to the queue at most once (when its color changes from $-1$).
- Each edge $(u, v)$ is traversed at most twice (once from $u$, once from $v$).
- Total queue operations $\le N$; total edge inspections $\le 2M$.
Total Time: Strictly $\Theta(N + M)$.

### Step 7: Proof of Correctness
- **Soundness**: If the algorithm returns `false`, it identified two adjacent vertices $u$ and $v$ with identical color. By construction, both $u$ and $v$ received their color via alternating paths from the component root. Their identical color implies they sit at equal parity distance from the root, which together with edge $(u, v)$ forms an odd cycle. By Kőnig's theorem, the graph cannot be bipartite.
- **Completeness**: If the algorithm returns `true`, every vertex in every component has been assigned a color in $\{0, 1\}$, and every edge $(u, v)$ was explicitly tested to confirm $\text{color}[u] \neq \text{color}[v]$. The coloring is a valid witness. $\blacksquare$

### Step 8: Concrete Trace
Graph: Triangle $(0-1, 1-2, 2-0)$.
1. Start at 0: `color[0] = 0`. Queue: `[0]`.
2. Pop 0:
   - Neighbor 1: unvisited $\implies$ `color[1] = 1`. Queue: `[1]`.
   - Neighbor 2: unvisited $\implies$ `color[2] = 1`. Queue: `[1, 2]`.
3. Pop 1:
   - Neighbor 0: visited, `color[0] = 0 != color[1] (1)`. Valid.
   - Neighbor 2: visited! `color[2] = 1 == color[1] (1)` $\implies$ **Conflict!**
4. Returns `false` immediately.

### Step 9: Edge Cases & Guards
- **Empty Graph / Zero Edges**: Trivially bipartite; all nodes colored 0.
- **Self-Loops $(u, u)$**: Neighbor $v = u$ has `color[u] == color[u]`, immediately caught and rejected.
- **Disconnected Forests / Trees**: All trees are bipartite (no cycles exist, hence no odd cycles). Returns `true`.

### Step 10: Standard ISO C++20 Implementation
```cpp
// solutions/cpp/GRPH-0001.cpp
#include <iostream>
#include <vector>
#include <queue>
#include <cassert>

namespace grph_0001 {

struct BipartiteResult {
    bool is_bipartite;
    std::vector<int> colors; // 0 or 1 for each vertex; empty if not bipartite
};

// Verifies if an undirected graph is bipartite and computes a valid 2-coloring
BipartiteResult check_bipartite(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> color(n, -1);
    std::queue<int> q;

    for (int i = 0; i < n; ++i) {
        if (color[i] != -1) continue;

        color[i] = 0;
        q.push(i);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) {
                    // Odd cycle detected: adjacent vertices have identical color
                    return BipartiteResult{false, {}};
                }
            }
        }
    }

    return BipartiteResult{true, color};
}

} // namespace grph_0001
```

### Step 11: Python 3.12+ Implementation
```python
# solutions/python/GRPH-0001.py
from typing import List, Tuple
from collections import deque

def check_bipartite(n: int, adj: List[List[int]]) -> Tuple[bool, List[int]]:
    """
    Checks if an undirected graph is bipartite using BFS 2-coloring.
    Returns (is_bipartite, colors) where colors[u] in {0, 1}.
    Runs in strictly O(N + M) time and O(N) space.
    """
    color = [-1] * n
    q = deque()

    for i in range(n):
        if color[i] != -1:
            continue

        color[i] = 0
        q.append(i)

        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, []

    return True, color
```

### Step 12: Asymptotic & Microarchitectural Complexity
- **Time Complexity**: Strictly $\Theta(N + M)$. Every node and edge is examined once per direction.
- **Space Complexity**: $\Theta(N)$ auxiliary memory for the `color` array and BFS queue.
- **Cache Locality**: Vector-of-vectors layout is standard; for maximum HPC throughput, a flat CSR layout can be substituted without changing the BFS loop semantics.

### Step 13: Failure Modes & Anti-Patterns
- **Testing Only Component 0**: Failing to loop over all $i \in [0, N-1]$ skips disconnected subgraphs, missing odd cycles in other components!
- **Deep Recursive DFS Stack Overflow**: Using recursive DFS on long path graphs ($N = 10^5$) overflows default thread stacks ($1–2$ MB). BFS using an explicit heap queue is always safe.

### Step 14: Dual-Language Nuance & Idioms
- **C++20**: Utilizing `std::queue<int>` backed by `std::deque` eliminates reallocation pauses during BFS traversal.
- **Python 3.12**: Utilizing `collections.deque.popleft()` ensures $O(1)$ queue pops (avoiding Python `list.pop(0)` which is disastrous $O(N)$).

### Step 15: Unit Tests & Verification Fixtures
Differential testing verifies:
1. Even cycles (e.g. square $C_4$) return `true` with alternating colors.
2. Odd cycles (e.g. triangle $C_3$, pentagon $C_5$) return `false`.
3. Disconnected graphs where one component is bipartite and another has an odd cycle return `false`.
4. Forest graphs of random trees return `true`.

### Step 16: Reader Engineering Challenges
1. **Odd-Cycle Extraction**: When bipartiteness fails, augment BFS to trace parent pointers and return the exact list of vertices forming the minimal odd cycle.
2. **Maximum Bipartite Matching (Hopcroft-Karp)**: Given a verified bipartite graph, implement Hopcroft-Karp to compute the maximum matching in $O(E \sqrt{V})$ time.

---

## 24.6 Chapter Summary & Graph Exploration Mental Model

Graph traversals are the lenses through which arbitrary networks are understood:
- **BFS** reveals metric structure: shortest hop distances and bipartite parity partitions.
- **DFS** reveals recursive structure: topological ordering, back edges, and cycle boundaries.
- **Kőnig's Theorem** bridges parity with geometry: odd cycles are the unique topological obstruction to bipartiteness.
