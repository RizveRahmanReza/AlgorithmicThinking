# MASTER OUTLINE — THE ART OF ALGORITHMIC THINKING

## 18 Major Curriculum Parts & Detailed Chapters

### PART I — THE ART OF PROBLEM SOLVING
- **Chapter 1: The Essence of Computational Problems**
  - 1.1 What is a Computational Problem? (Input, Output, Domain, Mapping)
  - 1.2 Distinguishing Problems from Instances and Real-World Ambiguity
  - 1.3 The Mechanics of Problem Decomposition and Abstraction
  - 1.4 Formulating Invariants: The Heartbeat of Correctness
  - 1.5 The Algorithmic Decision Framework (ADF): 20 Diagnostic Questions
  - 1.6 Worked Problem: `SOLV-0001` — The Anomaly Subsegment Identification
  - 1.7 Mental Models, Common Cognitive Biases, and Debugging Hypotheses
  - 1.8 Exercises, Explorations, and Chapter Synthesis
- **Chapter 2: Requirements Analysis, Constraints, and Invariants**
  - 2.1 Translating Real-World Requirements into Mathematical Formalisms
  - 2.2 Finding Hidden Constraints: Time, Space, Monotonicity, and Invertibility
  - 2.3 Designing Edge Cases and Adversarial Tests Before Writing Code
  - 2.4 The Technique of Counterexample Construction
  - 2.5 Worked Problem: `SOLV-0002` — Stable Resource Allocation Under Capacity Constraints
- **Chapter 3: Brute Force, Search Spaces, and Bottleneck Analysis**
  - 3.1 The Value of the Baseline: Why Brute Force Must Precede Optimization
  - 3.2 Formalizing the Search Space: Combinatorial Explosion and Growth
  - 3.3 Pinpointing the Bottleneck: Redundant Recomputation vs. Redundant Inspection
  - 3.4 Systematic Derivation: From Exponential Search to Polynomial Execution
  - 3.5 Worked Problem: `SOLV-0003` — Maximum Subarray Sum: From $O(N^3)$ to $O(N)$ Kadane's Invariant

### PART II — MATHEMATICS, LOGIC, AND COMPLEXITY
- **Chapter 4: Discrete Foundations, Logic, and Proof Techniques** (Direct, Contradiction, Induction, Loop Invariants)
- **Chapter 5: Counting, Combinatorics, and Recurrences** (Permutations, Pigeonhole, Generating Functions, Divide-and-Conquer Recurrences)
- **Chapter 6: Asymptotic Analysis and Complexity Classes** (Big-$O$, $\Omega$, $\Theta$, Amortized Analysis, Master Theorem, Lower Bounds)

### PART III — ARRAYS, STRINGS, AND LINKED LISTS
- **Chapter 7: Contiguous Memory, Dynamic Arrays, and Memory Locality** (Cache Lines, Amortized Geometric Resizing, In-Place Transformations)
- **Chapter 8: Strings, Encodings, and In-Place Sequence Manipulation** (ASCII, UTF-8, Sliding Character Buffers, Prefix/Suffix Accumulations)
- **Chapter 9: Pointer-Based Structures and Linked Lists** (Singly, Doubly, Circular Lists, Fast/Slow Pointers, Cycle Detection, Reversals)

### PART IV — STACKS, QUEUES, HASHING, AND SETS
- **Chapter 10: Linear LIFO and FIFO Structures** (Stacks, Queues, Circular Buffers, Priority Queues)
- **Chapter 11: Monotonic Stacks and Queues** (Next Greater Element, Sliding Window Maximums, Historical Minimums)
- **Chapter 12: Hash Tables, Collision Resolution, and Load Factors** (Hash Functions, Chaining, Open Addressing, Robin Hood Hashing, Bloom Filters)

### PART V — SEARCHING, SORTING, AND CORE PATTERNS
- **Chapter 13: Search Paradigms** (Linear, Binary Search on Arrays, Binary Search on Answer Space, Ternary Search)
- **Chapter 14: Comparison Sorting and Linear-Time Sorting** (QuickSort, MergeSort, HeapSort, Counting Sort, Radix Sort, Information-Theoretic $\Omega(N \log N)$ Lower Bound)
- **Chapter 15: Fundamental Array Patterns** (Two Pointers, Sliding Window, Prefix Sums, Difference Arrays, Sweep-Line)

### PART VI — TREES, HEAPS, AND TRIES
- **Chapter 16: Hierarchical Trees and Binary Search Trees** (Traversals, Tree Invariants, Binary Search Trees, Serialization)
- **Chapter 17: Balanced Binary Trees and Multiway Trees** (AVL, Red-Black Trees, B-Trees and B+ Trees in Databases)
- **Chapter 18: Heaps and Priority Scheduling** (Binary Min/Max Heaps, Heapify, D-ary Heaps, Priority Queues)
- **Chapter 19: Tries, Radix Trees, and Prefix Processing** (Standard Trie, Bitwise Trie, Compressed Radix Trees)

### PART VII — RANGE QUERIES AND ADVANCED DATA STRUCTURES
- **Chapter 20: Disjoint Set Union (DSU)** (Union by Rank, Path Compression, Rollback DSU)
- **Chapter 21: Fenwick Trees (Binary Indexed Trees)** (Point Update Range Query, Range Update Point Query, Multidimensional Fenwick)
- **Chapter 22: Segment Trees and Lazy Propagation** (Segment Tree Construction, Range Updates, Lazy Propagation, Dynamic Segment Trees)
- **Chapter 23: Advanced Query Structures** (Sparse Tables, Square-Root Decomposition, Mo's Algorithm, Heavy-Light Decomposition)

### PART VIII — GRAPH ALGORITHMS: FOUNDATIONS
- **Chapter 24: Graph Modeling, Traversals, and Connectivity** (Adjacency Representations, BFS, DFS, Connected Components, Bipartite Graphs)
- **Chapter 25: Directed Acyclic Graphs and Topological Ordering** (DAG Properties, Topological Sort, Cycle Detection, Task Scheduling)
- **Chapter 26: Shortest Paths in Weighted Graphs** (Dijkstra, 0-1 BFS, Bellman-Ford, Floyd-Warshall)
- **Chapter 27: Minimum Spanning Trees** (Kruskal, Prim, Cut and Cycle Properties)

### PART IX — ADVANCED GRAPH ALGORITHMS
- **Chapter 28: Connectivity, Articulation Points, and Bridges** (Tarjan's SCC, Kosaraju, Bridges, Bi-connected Components)
- **Chapter 29: Network Flows and Cuts** (Ford-Fulkerson, Edmonds-Karp, Dinic's Algorithm, Max-Flow Min-Cut Theorem)
- **Chapter 30: Matchings and Specialized Graph Problems** (Bipartite Matching, Hungarian Algorithm, 2-SAT, Eulerian Paths)

### PART X — RECURSION, GREEDY, BACKTRACKING, AND DYNAMIC PROGRAMMING
- **Chapter 31: Exhaustive Search, Backtracking, and Branch-and-Bound** (Pruning, Constraint Satisfaction)
- **Chapter 32: Greedy Algorithms and Exchange Arguments** (Matroids, Interval Scheduling, Greedy Choice Property)
- **Chapter 33: Foundations of Dynamic Programming** (Memoization, Tabulation, Optimal Substructure, Overlapping Subproblems)
- **Chapter 34: Classic and Advanced DP Paradigms** (Knapsack Variants, LIS, LCS, Interval DP, Bitmask DP, Digit DP, Tree DP, Convex Hull Trick)

### PART XI — ADVANCED STRING ALGORITHMS
- **Chapter 35: Pattern Matching** (KMP, Rabin-Karp, Z-Algorithm)
- **Chapter 36: Suffix Arrays and Suffix Automata** (Suffix Array with LCP, Suffix Automaton, Manacher's Algorithm)

### PART XII — BIT MANIPULATION, NUMBER THEORY, AND COMBINATORICS
- **Chapter 37: Bitwise Computation and Low-Level Tricks** (Bitwise Arithmetic, Popcount, Subset Iteration)
- **Chapter 38: Number Theory and Modular Arithmetic** (GCD, Extended Euclid, Prime Sieves, Modular Inverses, Chinese Remainder Theorem)
- **Chapter 39: Combinatorial and Algebraic Algorithms** (Inclusion-Exclusion, Matrix Exponentiation, Fast Fourier Transform)

### PART XIII — COMPUTATIONAL GEOMETRY AND NUMERICAL ALGORITHMS
- **Chapter 40: Vector Geometry and Primitives** (Orientation, Cross Products, Line Intersections)
- **Chapter 41: Polygons and Geometric Search** (Convex Hull: Graham Scan & Monotone Chain, Closest Pair, KD-Trees)
- **Chapter 42: Numerical Stability and Continuous Optimization** (Root Finding, Newton's Method, Numerical Precision Pitfalls)

### PART XIV — ADVANCED ALGORITHM DESIGN
- **Chapter 43: Randomized and Streaming Algorithms** (Reservoir Sampling, HyperLogLog, Count-Min Sketch, Bloom Filters)
- **Chapter 44: Approximation Algorithms and Heuristics** (Vertex Cover, Metric TSP, Simulated Annealing)
- **Chapter 45: Complexity Theory, Reductions, and NP-Completeness** (P vs NP, Karp Reductions, Tractable Subclasses)

### PART XV — BACKEND, DATABASES, AND DISTRIBUTED SYSTEMS
- **Chapter 46: Database Indexing Internals** (B+ Tree Pages, LSM-Trees, Write Amplification)
- **Chapter 47: Distributed Caching and Partitioning** (LRU/LFU, Consistent Hashing, Virtual Nodes)
- **Chapter 48: High-Throughput Stream Processing and Concurrency** (Rate Limiting: Token Bucket / Leaky Bucket, Lock-Free Ring Buffers)

### PART XVI — EMBEDDED SYSTEMS, ROBOTICS, AND REAL-TIME COMPUTING
- **Chapter 49: Memory-Constrained and Deterministic Systems** (Zero-Allocation Data Structures, Fixed-Capacity Ring Buffers, WCET)
- **Chapter 50: Robotics Pathfinding and Spatial Geometry** (A* Search, Dijkstra on Grids, Rapidly-exploring Random Trees)

### PART XVII — AI, MACHINE LEARNING, AND ALGORITHMIC COMPUTING
- **Chapter 51: High-Dimensional Vectors and Vector Search** (Cosine Similarity, Approximate Nearest Neighbors: HNSW, LSH)
- **Chapter 52: Computational Graphs and Sequence Processing** (Autodiff Topological Evaluation, Attention Complexity, Beam Search)

### PART XVIII — INTERVIEW MASTERY, RESEARCH, AND CAPSTONE CHALLENGES
- **Chapter 53: Algorithmic Interview Mastery and Whiteboard Communication** (Structuring Thought, Explaining Invariants, Handling Pressure)
- **Chapter 54: Capstone Engineering Projects** (Full Production Implementations: In-Memory Search Engine, Miniature KV Store, Multi-Constraint Task Scheduler)
- **Chapter 55: Research Horizons and Open Algorithmic Challenges** (Quantum Algorithms Overview, Sublinear Algorithms, Next-Gen Hardware)
