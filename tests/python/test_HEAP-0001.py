import pytest
from solutions.python.HEAP_0001 import MinMaxHeap

def test_heap_0001_basic_operations():
    mmh = MinMaxHeap()
    vals = [30, 10, 50, 5, 80, 2, 90, 70]
    for v in vals:
        mmh.insert(v)

    assert mmh.get_min() == 2
    assert mmh.get_max() == 90

    assert mmh.extract_min() == 2
    assert mmh.get_min() == 5

    assert mmh.extract_max() == 90
    assert mmh.get_max() == 80

    assert mmh.extract_min() == 5
    assert mmh.extract_max() == 80

def test_heap_0001_small_elements():
    mmh = MinMaxHeap()
    mmh.insert(42)
    assert mmh.get_min() == 42
    assert mmh.get_max() == 42
    assert mmh.extract_max() == 42

    mmh.insert(10)
    mmh.insert(20)
    assert mmh.get_min() == 10
    assert mmh.get_max() == 20
    assert mmh.extract_min() == 10
    assert mmh.get_min() == 20
    assert mmh.get_max() == 20

def test_heap_0001_random_oracle():
    import random
    rng = random.Random(42)
    mmh = MinMaxHeap()
    oracle = []

    for _ in range(300):
        action = rng.choice(["insert", "insert", "min", "max"])
        if action == "insert":
            val = rng.randint(-1000, 1000)
            mmh.insert(val)
            oracle.append(val)
        elif action == "min" and oracle:
            expected = min(oracle)
            assert mmh.get_min() == expected
            actual = mmh.extract_min()
            assert actual == expected
            oracle.remove(expected)
        elif action == "max" and oracle:
            expected = max(oracle)
            assert mmh.get_max() == expected
            actual = mmh.extract_max()
            assert actual == expected
            oracle.remove(expected)
