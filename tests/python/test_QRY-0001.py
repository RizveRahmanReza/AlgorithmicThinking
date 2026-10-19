import pytest
from solutions.python.QRY_0001 import SparseTable

def test_qry_0001_basic():
    arr = [31, 41, 59, 26, 53, 58, 97]
    st = SparseTable(arr)

    assert st.query_min(0, 6) == 26
    assert st.query_min_index(0, 6) == 3

    assert st.query_min(0, 2) == 31
    assert st.query_min(4, 6) == 53
    assert st.query_min(1, 5) == 26

    # Single element
    assert st.query_min(2, 2) == 59

def test_qry_0001_differential_fuzz():
    import random
    rng = random.Random(42)
    n = 100
    arr = [rng.randint(-500, 500) for _ in range(n)]
    st = SparseTable(arr)

    for _ in range(500):
        l = rng.randint(0, n - 1)
        r = rng.randint(l, n - 1)

        expected = min(arr[l : r + 1])
        actual = st.query_min(l, r)
        assert actual == expected
