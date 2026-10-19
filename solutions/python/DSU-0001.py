from typing import List

class OperationRecord:
    __slots__ = ("child", "parent", "prev_parent_size", "was_merged")
    def __init__(self, child: int, parent: int, prev_parent_size: int, was_merged: bool):
        self.child = child
        self.parent = parent
        self.prev_parent_size = prev_parent_size
        self.was_merged = was_merged

class RollbackDSU:
    def __init__(self, n: int):
        self.parent: List[int] = list(range(n))
        self.sz: List[int] = [1] * n
        self.history: List[OperationRecord] = []
        self.num_components: int = n

    def find(self, u: int) -> int:
        """Read-only find without path compression: O(log N) worst case."""
        curr = u
        while curr != self.parent[curr]:
            curr = self.parent[curr]
        return curr

    def connected(self, u: int, v: int) -> bool:
        return self.find(u) == self.find(v)

    def component_size(self, u: int) -> int:
        return self.sz[self.find(u)]

    def count_components(self) -> int:
        return self.num_components

    def unite(self, u: int, v: int) -> bool:
        """Merges components using Union by Size and records state: O(log N)."""
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u == root_v:
            self.history.append(OperationRecord(-1, -1, 0, False))
            return False

        if self.sz[root_u] < self.sz[root_v]:
            root_u, root_v = root_v, root_u

        self.history.append(OperationRecord(root_v, root_u, self.sz[root_u], True))

        self.parent[root_v] = root_u
        self.sz[root_u] += self.sz[root_v]
        self.num_components -= 1
        return True

    def rollback(self) -> None:
        """Reverts the single most recent unite operation in strictly O(1) time."""
        if not self.history:
            raise IndexError("History stack underflow during rollback")

        rec = self.history.pop()
        if not rec.was_merged:
            return

        self.parent[rec.child] = rec.child
        self.sz[rec.parent] = rec.prev_parent_size
        self.num_components += 1

    def checkpoint(self) -> int:
        return len(self.history)

    def rollback_to(self, cp: int) -> None:
        if cp > len(self.history):
            raise ValueError("Invalid checkpoint")
        while len(self.history) > cp:
            self.rollback()
