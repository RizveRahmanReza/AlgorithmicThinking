import pytest
from solutions.python.GRPH_0001 import check_bipartite

def test_grph_0001_even_cycle():
    n = 4
    adj = [[1, 3], [0, 2], [1, 3], [0, 2]]
    is_bip, colors = check_bipartite(n, adj)
    assert is_bip
    for u in range(n):
        for v in adj[u]:
            assert colors[u] != colors[v]

def test_grph_0001_odd_cycle():
    n = 3
    adj = [[1, 2], [0, 2], [0, 1]]
    is_bip, colors = check_bipartite(n, adj)
    assert not is_bip
    assert colors == []

def test_grph_0001_disconnected_forest():
    n = 5
    adj = [[1], [0], [3], [2], []]
    is_bip, colors = check_bipartite(n, adj)
    assert is_bip
    for u in range(n):
        for v in adj[u]:
            assert colors[u] != colors[v]

def test_grph_0001_self_loop():
    n = 2
    adj = [[0, 1], [0]]
    is_bip, colors = check_bipartite(n, adj)
    assert not is_bip
