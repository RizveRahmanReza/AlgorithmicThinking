import pytest
from solutions.python.SORT_0001 import three_way_partition, reference_partition, verify_invariants

def test_sort_0001_standard():
    arr = [2, 0, 2, 1, 1, 0]
    pivot = 1
    low, high = three_way_partition(arr, pivot)
    assert verify_invariants(arr, pivot, low, high)
    assert sorted(arr) == sorted([2, 0, 2, 1, 1, 0])

def test_sort_0001_empty():
    arr = []
    pivot = 5
    low, high = three_way_partition(arr, pivot)
    assert low == 0
    assert high == -1

def test_sort_0001_all_identical():
    arr = [4, 4, 4, 4, 4]
    pivot = 4
    low, high = three_way_partition(arr, pivot)
    assert verify_invariants(arr, pivot, low, high)
    assert low == 0
    assert high == 4

def test_sort_0001_all_less():
    arr = [1, 2, 3]
    pivot = 10
    low, high = three_way_partition(arr, pivot)
    assert verify_invariants(arr, pivot, low, high)
    assert low == 3
    assert high == 2

def test_sort_0001_all_greater():
    arr = [10, 20, 30]
    pivot = 5
    low, high = three_way_partition(arr, pivot)
    assert verify_invariants(arr, pivot, low, high)
    assert low == 0
    assert high == -1

def test_sort_0001_differential_oracle():
    import random
    rng = random.Random(42)
    for _ in range(50):
        n = rng.randint(1, 100)
        arr = [rng.randint(0, 10) for _ in range(n)]
        pivot = rng.randint(0, 10)
        arr_copy = list(arr)
        
        low, high = three_way_partition(arr, pivot)
        assert verify_invariants(arr, pivot, low, high)
        assert sorted(arr) == sorted(arr_copy)
