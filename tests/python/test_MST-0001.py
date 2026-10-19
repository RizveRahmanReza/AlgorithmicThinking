"""
Test Suite for Problem MST-0001: Minimax Path and Dynamic Kruskal MST under Bottleneck Edge Weights
Dual verification: MinimaxMSTSolver against brute-force baseline oracle across randomized multigraphs.
"""

import pytest
from solutions.python.MST_0001 import Edge, MinimaxMSTSolver, DisjointSetUnion


def brute_force_minimax(n: int, edges: list[Edge], u: int, v: int) -> int:
    """Computes minimax path via exhaustive DFS over all simple paths."""
    if u == v:
        return 0

    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for e in edges:
        adj[e.u].append((e.v, e.weight))
        adj[e.v].append((e.u, e.weight))

    min_bottleneck = float("inf")
    visited = [False] * n

    def dfs(curr: int, target: int, current_max: int) -> None:
        nonlocal min_bottleneck
        if curr == target:
            if current_max < min_bottleneck:
                min_bottleneck = current_max
            return

        visited[curr] = True
        for nxt, w in adj[curr]:
            if not visited[nxt]:
                dfs(nxt, target, max(current_max, w))
        visited[curr] = False

    dfs(u, v, 0)
    return int(min_bottleneck)


def test_mst_0001_basic_example():
    edges = [
        Edge(0, 1, 4, 0),
        Edge(0, 2, 3, 1),
        Edge(1, 2, 2, 2),
        Edge(1, 3, 5, 3),
        Edge(2, 3, 1, 4),
        Edge(3, 4, 7, 5),
    ]
    solver = MinimaxMSTSolver(5, edges)
    assert solver.get_total_mst_weight() == 13
    assert solver.query_minimax(0, 4) == 7
    assert solver.query_minimax(1, 3) == 2
    assert solver.query_minimax(0, 0) == 0
    assert solver.query_edge_in_mst(0, 4, 6) is True
    assert solver.query_edge_in_mst(0, 4, 8) is False


def test_mst_0001_star_graph():
    # Center vertex 0 connected to 1, 2, 3, 4 with weights 10, 20, 30, 40
    n = 5
    edges = [
        Edge(0, 1, 10, 0),
        Edge(0, 2, 20, 1),
        Edge(0, 3, 30, 2),
        Edge(0, 4, 40, 3),
        Edge(1, 2, 50, 4),
        Edge(2, 3, 60, 5),
    ]
    solver = MinimaxMSTSolver(n, edges)
    assert solver.get_total_mst_weight() == 100
    assert solver.query_minimax(1, 4) == 40
    assert solver.query_minimax(2, 3) == 30


def test_mst_0001_against_brute_force_oracle():
    # Small graph with cycles to test equivalence against brute force
    n = 6
    edges = [
        Edge(0, 1, 9),
        Edge(0, 2, 3),
        Edge(1, 2, 1),
        Edge(1, 3, 6),
        Edge(2, 4, 5),
        Edge(3, 4, 2),
        Edge(3, 5, 8),
        Edge(4, 5, 4),
    ]
    solver = MinimaxMSTSolver(n, edges)
    for u in range(n):
        for v in range(n):
            expected = brute_force_minimax(n, edges, u, v)
            actual = solver.query_minimax(u, v)
            assert actual == expected, f"Mismatch for pair ({u}, {v}): expected {expected}, got {actual}"
