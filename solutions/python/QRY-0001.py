from typing import List

class SparseTable:
    def __init__(self, arr: List[int]):
        self.raw_data = arr
        self.n = len(arr)
        if self.n == 0:
            return

        # 1. Precompute log table
        self.log_table = [0] * (self.n + 1)
        for i in range(2, self.n + 1):
            self.log_table[i] = self.log_table[i // 2] + 1

        self.max_log = self.log_table[self.n] + 1

        # 2. Build Sparse Table storing indices of minimums
        self.st: List[List[int]] = [[0] * self.n for _ in range(self.max_log)]
        for i in range(self.n):
            self.st[0][i] = i

        for k in range(1, self.max_log):
            half = 1 << (k - 1)
            full = 1 << k
            for i in range(self.n - full + 1):
                idx1 = self.st[k - 1][i]
                idx2 = self.st[k - 1][i + half]
                self.st[k][i] = idx1 if self.raw_data[idx1] <= self.raw_data[idx2] else idx2

    def query_min_index(self, l: int, r: int) -> int:
        """Returns the index of the minimum element in arr[l..r] in strictly O(1) time."""
        length = r - l + 1
        k = self.log_table[length]
        idx1 = self.st[k][l]
        idx2 = self.st[k][r - (1 << k) + 1]
        return idx1 if self.raw_data[idx1] <= self.raw_data[idx2] else idx2

    def query_min(self, l: int, r: int) -> int:
        """Returns the minimum value in arr[l..r] in strictly O(1) time."""
        return self.raw_data[self.query_min_index(l, r)]
