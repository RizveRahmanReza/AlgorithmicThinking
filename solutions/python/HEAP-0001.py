from typing import List

class MinMaxHeap:
    def __init__(self):
        self.h: List[int] = []

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _grandparent(i: int) -> int:
        return (i - 3) // 4

    @staticmethod
    def _is_min_level(i: int) -> bool:
        level = 0
        idx = i + 1
        while idx > 1:
            idx >>= 1
            level += 1
        return (level % 2) == 0

    def insert(self, key: int) -> None:
        self.h.append(key)
        self._sift_up(len(self.h) - 1)

    def _sift_up(self, i: int) -> None:
        if i == 0:
            return
        p = self._parent(i)
        if self._is_min_level(i):
            if self.h[i] > self.h[p]:
                self.h[i], self.h[p] = self.h[p], self.h[i]
                self._sift_up_max(p)
            else:
                self._sift_up_min(i)
        else:
            if self.h[i] < self.h[p]:
                self.h[i], self.h[p] = self.h[p], self.h[i]
                self._sift_up_min(p)
            else:
                self._sift_up_max(i)

    def _sift_up_min(self, i: int) -> None:
        while i >= 3:
            gp = self._grandparent(i)
            if self.h[i] < self.h[gp]:
                self.h[i], self.h[gp] = self.h[gp], self.h[i]
                i = gp
            else:
                break

    def _sift_up_max(self, i: int) -> None:
        while i >= 3:
            gp = self._grandparent(i)
            if self.h[i] > self.h[gp]:
                self.h[i], self.h[gp] = self.h[gp], self.h[i]
                i = gp
            else:
                break

    def _find_min_descendant(self, i: int) -> int:
        n = len(self.h)
        best = 2 * i + 1
        for c in [2 * i + 1, 2 * i + 2]:
            if c < n and self.h[c] < self.h[best]:
                best = c
        for gc in range(4 * i + 3, min(n, 4 * i + 7)):
            if self.h[gc] < self.h[best]:
                best = gc
        return best

    def _find_max_descendant(self, i: int) -> int:
        n = len(self.h)
        best = 2 * i + 1
        for c in [2 * i + 1, 2 * i + 2]:
            if c < n and self.h[c] > self.h[best]:
                best = c
        for gc in range(4 * i + 3, min(n, 4 * i + 7)):
            if self.h[gc] > self.h[best]:
                best = gc
        return best

    def _sift_down(self, i: int) -> None:
        if self._is_min_level(i):
            self._sift_down_min(i)
        else:
            self._sift_down_max(i)

    def _sift_down_min(self, i: int) -> None:
        n = len(self.h)
        if 2 * i + 1 >= n:
            return
        m = self._find_min_descendant(i)
        if m >= 4 * i + 3:
            if self.h[m] < self.h[i]:
                self.h[m], self.h[i] = self.h[i], self.h[m]
                p = self._parent(m)
                if self.h[m] > self.h[p]:
                    self.h[m], self.h[p] = self.h[p], self.h[m]
                self._sift_down_min(m)
        else:
            if self.h[m] < self.h[i]:
                self.h[m], self.h[i] = self.h[i], self.h[m]

    def _sift_down_max(self, i: int) -> None:
        n = len(self.h)
        if 2 * i + 1 >= n:
            return
        m = self._find_max_descendant(i)
        if m >= 4 * i + 3:
            if self.h[m] > self.h[i]:
                self.h[m], self.h[i] = self.h[i], self.h[m]
                p = self._parent(m)
                if self.h[m] < self.h[p]:
                    self.h[m], self.h[p] = self.h[p], self.h[m]
                self._sift_down_max(m)
        else:
            if self.h[m] > self.h[i]:
                self.h[m], self.h[i] = self.h[i], self.h[m]

    def get_min(self) -> int:
        if not self.h:
            raise IndexError("Heap is empty")
        return self.h[0]

    def get_max(self) -> int:
        if not self.h:
            raise IndexError("Heap is empty")
        if len(self.h) == 1:
            return self.h[0]
        if len(self.h) == 2:
            return self.h[1]
        return max(self.h[1], self.h[2])

    def extract_min(self) -> int:
        if not self.h:
            raise IndexError("Heap is empty")
        min_val = self.h[0]
        last = self.h.pop()
        if self.h:
            self.h[0] = last
            self._sift_down(0)
        return min_val

    def extract_max(self) -> int:
        if not self.h:
            raise IndexError("Heap is empty")
        if len(self.h) == 1:
            return self.h.pop()
        max_idx = 1
        if len(self.h) > 2 and self.h[2] > self.h[1]:
            max_idx = 2
        max_val = self.h[max_idx]
        last = self.h.pop()
        if max_idx < len(self.h):
            self.h[max_idx] = last
            self._sift_down(max_idx)
        return max_val
