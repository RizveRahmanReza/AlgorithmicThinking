import pytest
from solutions.python.PATH_0001 import shortest_path_k_passes

def test_path_0001_standard():
    n = 3
    adj = [
        [(1, 10), (2, 100)],
        [(2, 20)],
        []
    ]

    # K = 0 -> 10 + 20 = 30
    assert shortest_path_k_passes(n, adj, 0, 2, 0) == 30

    # K = 1 -> 10 + 0 = 10
    assert shortest_path_k_passes(n, adj, 0, 2, 1) == 10

    # K = 2 -> 0 + 0 = 0
    assert shortest_path_k_passes(n, adj, 0, 2, 2) == 0

def test_path_0001_unreachable():
    n = 4
    adj = [[(1, 5)], [], [], []]
    assert shortest_path_k_passes(n, adj, 0, 3, 2) == -1

def test_path_0001_same_source_target():
    n = 3
    adj = [[(1, 10)], [(2, 10)], []]
    assert shortest_path_k_passes(n, adj, 1, 1, 0) == 0
