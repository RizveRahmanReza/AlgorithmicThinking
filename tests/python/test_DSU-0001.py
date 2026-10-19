import pytest
from solutions.python.DSU_0001 import RollbackDSU

def test_dsu_0001_basic():
    dsu = RollbackDSU(6)
    assert dsu.count_components() == 6

    assert dsu.unite(0, 1)
    assert dsu.unite(2, 3)
    assert dsu.count_components() == 4
    assert dsu.component_size(0) == 2
    assert dsu.component_size(2) == 2

    snap = dsu.checkpoint()

    assert dsu.unite(1, 2)
    assert dsu.connected(0, 3)
    assert dsu.count_components() == 3
    assert dsu.component_size(0) == 4

    dsu.rollback_to(snap)
    assert not dsu.connected(0, 3)
    assert dsu.count_components() == 4
    assert dsu.component_size(0) == 2

    # Redundant union
    assert not dsu.unite(0, 1)
    dsu.rollback()
    assert dsu.connected(0, 1)

def test_dsu_0001_differential_fuzz():
    import random
    rng = random.Random(42)
    n = 20
    dsu = RollbackDSU(n)

    # Maintain an explicit edge list history to compare against BFS connectivity
    edge_history = []

    def get_components(edges):
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = [False] * n
        comps = 0
        for i in range(n):
            if not visited[i]:
                comps += 1
                q = [i]
                visited[i] = True
                while q:
                    curr = q.pop()
                    for neighbor in adj[curr]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            q.append(neighbor)
        return comps

    for _ in range(300):
        if rng.random() < 0.65 or not edge_history:
            u = rng.randint(0, n - 1)
            v = rng.randint(0, n - 1)
            dsu.unite(u, v)
            edge_history.append((u, v))
        else:
            dsu.rollback()
            edge_history.pop()

        expected_comps = get_components(edge_history)
        assert dsu.count_components() == expected_comps
