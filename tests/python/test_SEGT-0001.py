import pytest
from solutions.python.SEGT_0001 import AffineSegmentTree, MOD

def test_segt_0001_basic():
    arr = [1, 2, 3, 4, 5]
    st = AffineSegmentTree(arr)

    assert st.query_sum(0, 4) == 15
    assert st.query_sum(1, 3) == 9

    st.range_multiply(0, 3, 2)
    # [2, 4, 6, 8, 5]
    assert st.query_sum(0, 4) == 25
    assert st.query_sum(1, 3) == 18

    st.range_add(2, 4, 3)
    # [2, 4, 9, 11, 8]
    assert st.query_sum(0, 4) == 34
    assert st.query_sum(2, 3) == 20

def test_segt_0001_differential_fuzz():
    import random
    rng = random.Random(42)
    n = 30
    arr = [rng.randint(0, 100) for _ in range(n)]
    st = AffineSegmentTree(arr)
    sim = list(arr)

    for _ in range(200):
        op = rng.choice(["add", "mul", "query"])
        l = rng.randint(0, n - 1)
        r = rng.randint(l, n - 1)

        if op == "add":
            v = rng.randint(1, 50)
            st.range_add(l, r, v)
            for i in range(l, r + 1):
                sim[i] = (sim[i] + v) % MOD
        elif op == "mul":
            v = rng.randint(0, 10)
            st.range_multiply(l, r, v)
            for i in range(l, r + 1):
                sim[i] = (sim[i] * v) % MOD
        else:
            expected = sum(sim[l : r + 1]) % MOD
            actual = st.query_sum(l, r)
            assert actual == expected
