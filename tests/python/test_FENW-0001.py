import pytest
from solutions.python.FENW_0001 import count_inversions, reference_count_inversions

def test_fenw_0001_reverse_sorted():
    arr = [8, 4, 2, 1]
    assert count_inversions(arr) == 6
    assert count_inversions(arr) == reference_count_inversions(arr)

def test_fenw_0001_already_sorted():
    arr = [1, 2, 3, 4, 5]
    assert count_inversions(arr) == 0

def test_fenw_0001_duplicates():
    arr = [2, 4, 1, 3, 2]
    assert count_inversions(arr) == 4
    assert count_inversions(arr) == reference_count_inversions(arr)

def test_fenw_0001_empty_and_single():
    assert count_inversions([]) == 0
    assert count_inversions([100]) == 0

def test_fenw_0001_differential_fuzz():
    import random
    rng = random.Random(42)
    for _ in range(50):
        n = rng.randint(1, 60)
        arr = [rng.randint(-100, 100) for _ in range(n)]
        expected = reference_count_inversions(arr)
        actual = count_inversions(arr)
        assert actual == expected
