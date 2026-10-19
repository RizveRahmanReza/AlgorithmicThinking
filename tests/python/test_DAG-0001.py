import pytest
from solutions.python.DAG_0001 import lexicographical_toposort

def test_dag_0001_diamond():
    n = 4
    adj = [
        [],        # 0
        [0, 3],    # 1
        [0],       # 2
        []         # 3
    ]
    # In-degrees: 0: 2 (from 1, 2), 1: 0, 2: 0, 3: 1 (from 1)
    res = lexicographical_toposort(n, adj)
    assert res == [1, 2, 0, 3]

def test_dag_0001_cycle():
    n = 3
    adj = [[1], [2], [0]]
    assert lexicographical_toposort(n, adj) == []

def test_dag_0001_disconnected():
    n = 4
    adj = [[], [], [], []]
    assert lexicographical_toposort(n, adj) == [0, 1, 2, 3]

def test_dag_0001_self_loop():
    n = 2
    adj = [[0, 1], []]
    assert lexicographical_toposort(n, adj) == []
