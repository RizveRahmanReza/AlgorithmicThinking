from typing import List
import bisect

class FenwickTree:
    def __init__(self, size: int):
        self.n = size
        self.tree: List[int] = [0] * (size + 1)

    def update(self, i: int, delta: int) -> None:
        """Adds delta to 1-based index i: O(log N)."""
        while i <= self.n:
            self.tree[i] += delta
            i += (i & -i)

    def query(self, i: int) -> int:
        """Computes prefix sum [1..i]: O(log N)."""
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= (i & -i)
        return s

    def query_range(self, l: int, r: int) -> int:
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)

def count_inversions(arr: List[int]) -> int:
    """
    Computes total inversions in arr via coordinate compression and Fenwick Tree.
    Runs in strictly O(N log N) time and O(N) space.
    """
    n = len(arr)
    if n <= 1:
        return 0

    sorted_unique = sorted(set(arr))
    u = len(sorted_unique)
    bit = FenwickTree(u)

    total_inversions = 0

    for i, val in enumerate(arr):
        rank = bisect.bisect_left(sorted_unique, val) + 1
        greater_count = i - bit.query(rank)
        total_inversions += greater_count
        bit.update(rank, 1)

    return total_inversions

def reference_count_inversions(arr: List[int]) -> int:
    """Quadratic oracle for testing."""
    inv = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inv += 1
    return inv
