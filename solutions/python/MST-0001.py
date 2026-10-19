"""
Problem ID: MST-0001
Title: Minimax Path and Dynamic Kruskal MST under Bottleneck Edge Weights
Language: Standard Python 3.12+
"""

from __future__ import annotations
from dataclasses import dataclass
from collections import deque
import math


@dataclass(slots=True)
class Edge:
    u: int
    v: int
    weight: int
    id: int = 0


class DisjointSetUnion:
    __slots__ = ("parent", "rank")

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i: int) -> int:
        path = []
        curr = i
        while self.parent[curr] != curr:
            path.append(curr)
            curr = self.parent[curr]
        for node in path:
            self.parent[node] = curr
        return curr

    def unite(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False
        if self.rank[root_i] < self.rank[root_j]:
            root_i, root_j = root_j, root_i
        self.parent[root_j] = root_i
        if self.rank[root_i] == self.rank[root_j]:
            self.rank[root_i] += 1
        return True


class MinimaxMSTSolver:
    __slots__ = ("n", "log_n", "total_mst_weight", "adj", "up", "max_w", "depth")

    def __init__(self, n: int, edges: list[Edge]) -> None:
        self.n = n
        self.total_mst_weight = 0
        self.log_n = max(1, math.ceil(math.log2(max(2, n)))) + 1

        self.adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
        self.up: list[list[int]] = [[0] * self.log_n for _ in range(n)]
        self.max_w: list[list[int]] = [[0] * self.log_n for _ in range(n)]
        self.depth = [-1] * n

        edges_sorted = sorted(edges, key=lambda e: e.weight)
        dsu = DisjointSetUnion(n)
        edges_added = 0

        for edge in edges_sorted:
            if dsu.unite(edge.u, edge.v):
                self.adj[edge.u].append((edge.v, edge.weight))
                self.adj[edge.v].append((edge.u, edge.weight))
                self.total_mst_weight += edge.weight
                edges_added += 1
                if edges_added == n - 1:
                    break

        self._build_tree(root=0)

    def _build_tree(self, root: int) -> None:
        q: deque[int] = deque([root])
        self.depth[root] = 0
        self.up[root][0] = root
        self.max_w[root][0] = 0

        while q:
            u = q.popleft()
            for v, w in self.adj[u]:
                if self.depth[v] == -1:
                    self.depth[v] = self.depth[u] + 1
                    self.up[v][0] = u
                    self.max_w[v][0] = w
                    q.append(v)

        for k in range(1, self.log_n):
            for u in range(self.n):
                mid = self.up[u][k - 1]
                self.up[u][k] = self.up[mid][k - 1]
                self.max_w[u][k] = max(self.max_w[u][k - 1], self.max_w[mid][k - 1])

    def get_total_mst_weight(self) -> int:
        return self.total_mst_weight

    def query_minimax(self, u: int, v: int) -> int:
        if u == v:
            return 0

        ans = 0
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        for k in range(self.log_n - 1, -1, -1):
            if self.depth[u] - (1 << k) >= self.depth[v]:
                ans = max(ans, self.max_w[u][k])
                u = self.up[u][k]

        if u == v:
            return ans

        for k in range(self.log_n - 1, -1, -1):
            if self.up[u][k] != self.up[v][k]:
                ans = max(ans, self.max_w[u][k], self.max_w[v][k])
                u = self.up[u][k]
                v = self.up[v][k]

        ans = max(ans, self.max_w[u][0], self.max_w[v][0])
        return ans

    def query_edge_in_mst(self, u: int, v: int, w: int) -> bool:
        return w <= self.query_minimax(u, v)


if __name__ == "__main__":
    n_nodes = 5
    edge_list = [
        Edge(0, 1, 4, 0),
        Edge(0, 2, 3, 1),
        Edge(1, 2, 2, 2),
        Edge(1, 3, 5, 3),
        Edge(2, 3, 1, 4),
        Edge(3, 4, 7, 5)
    ]
    solver = MinimaxMSTSolver(n_nodes, edge_list)
    assert solver.get_total_mst_weight() == 13
    assert solver.query_minimax(0, 4) == 7
    assert solver.query_minimax(1, 3) == 2
    assert solver.query_minimax(0, 0) == 0
    assert solver.query_edge_in_mst(0, 4, 6) is True
    assert solver.query_edge_in_mst(0, 4, 8) is False
    print("MST-0001 (Python 3.12+) assertions passed successfully.")
