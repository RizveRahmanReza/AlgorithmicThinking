from typing import List

MOD = 1_000_000_007

class AffineSegmentTree:
    def __init__(self, arr: List[int]):
        self.n = len(arr)
        self.tree_sum = [0] * (4 * self.n)
        self.lazy_mul = [1] * (4 * self.n)
        self.lazy_add = [0] * (4 * self.n)
        if self.n > 0:
            self._build(1, 0, self.n - 1, arr)

    def _apply_affine(self, p: int, l: int, r: int, mul_val: int, add_val: int) -> None:
        length = r - l + 1
        self.tree_sum[p] = (self.tree_sum[p] * mul_val + add_val * length) % MOD
        self.lazy_mul[p] = (self.lazy_mul[p] * mul_val) % MOD
        self.lazy_add[p] = (self.lazy_add[p] * mul_val + add_val) % MOD

    def _push_down(self, p: int, l: int, r: int) -> None:
        if self.lazy_mul[p] == 1 and self.lazy_add[p] == 0:
            return
        mid = (l + r) // 2
        self._apply_affine(2 * p, l, mid, self.lazy_mul[p], self.lazy_add[p])
        self._apply_affine(2 * p + 1, mid + 1, r, self.lazy_mul[p], self.lazy_add[p])
        self.lazy_mul[p] = 1
        self.lazy_add[p] = 0

    def _push_up(self, p: int) -> None:
        self.tree_sum[p] = (self.tree_sum[2 * p] + self.tree_sum[2 * p + 1]) % MOD

    def _build(self, p: int, l: int, r: int, arr: List[int]) -> None:
        if l == r:
            self.tree_sum[p] = arr[l] % MOD
            return
        mid = (l + r) // 2
        self._build(2 * p, l, mid, arr)
        self._build(2 * p + 1, mid + 1, r, arr)
        self._push_up(p)

    def range_add(self, l: int, r: int, val: int) -> None:
        self._update(1, 0, self.n - 1, l, r, 1, val % MOD)

    def range_multiply(self, l: int, r: int, val: int) -> None:
        self._update(1, 0, self.n - 1, l, r, val % MOD, 0)

    def _update(self, p: int, l: int, r: int, ql: int, qr: int, mul_val: int, add_val: int) -> None:
        if ql <= l and r <= qr:
            self._apply_affine(p, l, r, mul_val, add_val)
            return
        self._push_down(p, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._update(2 * p, l, mid, ql, qr, mul_val, add_val)
        if qr > mid:
            self._update(2 * p + 1, mid + 1, r, ql, qr, mul_val, add_val)
        self._push_up(p)

    def query_sum(self, l: int, r: int) -> int:
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, p: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.tree_sum[p]
        self._push_down(p, l, r)
        mid = (l + r) // 2
        total = 0
        if ql <= mid:
            total = (total + self._query(2 * p, l, mid, ql, qr)) % MOD
        if qr > mid:
            total = (total + self._query(2 * p + 1, mid + 1, r, ql, qr)) % MOD
        return total
