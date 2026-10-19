"""
HASH-0001: Cache-Conscious Flat Hash Map with Linear Probing
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Open-Addressing Linear Probing Map with SplitMix64 and Tombstone Recycling.
"""

from typing import Optional
from enum import Enum


class SlotState(Enum):
    EMPTY = 0
    OCCUPIED = 1
    TOMBSTONE = 2


class Entry:
    def __init__(self, key: int = 0, value: int = 0, state: SlotState = SlotState.EMPTY):
        self.key = key
        self.value = value
        self.state = state


def splitmix64(x: int) -> int:
    """SplitMix64 bit avalanche mixer."""
    x = (x + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return x ^ (x >> 31)


class FlatHashMap:
    """
    Open-Addressing Flat Hash Map with Linear Probing and Tombstone Recycling.
    Target: Python 3.12+ (Expected O(1) ops, contiguous backing array).
    """
    MAX_LOAD_FACTOR = 0.70

    def __init__(self, initial_capacity: int = 8):
        self.capacity = max(8, self._next_power_of_two(initial_capacity))
        self.size = 0
        self.tombstone_count = 0
        self.table = [Entry() for _ in range(self.capacity)]

    @staticmethod
    def _next_power_of_two(v: int) -> int:
        p = 1
        while p < v:
            p <<= 1
        return p

    def insert(self, key: int, value: int) -> bool:
        if (self.size + self.tombstone_count + 1) / self.capacity > self.MAX_LOAD_FACTOR:
            self._rehash(self.capacity * 2)

        mask = self.capacity - 1
        idx = splitmix64(key) & mask
        first_tombstone: Optional[int] = None

        while self.table[idx].state != SlotState.EMPTY:
            if self.table[idx].state == SlotState.OCCUPIED:
                if self.table[idx].key == key:
                    self.table[idx].value = value
                    return False
            elif self.table[idx].state == SlotState.TOMBSTONE and first_tombstone is None:
                first_tombstone = idx
            idx = (idx + 1) & mask

        target_slot = idx if first_tombstone is None else first_tombstone
        if self.table[target_slot].state == SlotState.TOMBSTONE:
            self.tombstone_count -= 1

        self.table[target_slot].key = key
        self.table[target_slot].value = value
        self.table[target_slot].state = SlotState.OCCUPIED
        self.size += 1
        return True

    def get(self, key: int) -> Optional[int]:
        mask = self.capacity - 1
        idx = splitmix64(key) & mask

        while self.table[idx].state != SlotState.EMPTY:
            if self.table[idx].state == SlotState.OCCUPIED and self.table[idx].key == key:
                return self.table[idx].value
            idx = (idx + 1) & mask
        return None

    def remove(self, key: int) -> bool:
        mask = self.capacity - 1
        idx = splitmix64(key) & mask

        while self.table[idx].state != SlotState.EMPTY:
            if self.table[idx].state == SlotState.OCCUPIED and self.table[idx].key == key:
                self.table[idx].state = SlotState.TOMBSTONE
                self.size -= 1
                self.tombstone_count += 1
                return True
            idx = (idx + 1) & mask
        return False

    def _rehash(self, new_capacity: int) -> None:
        old_table = self.table
        self.capacity = new_capacity
        self.size = 0
        self.tombstone_count = 0
        self.table = [Entry() for _ in range(self.capacity)]

        for entry in old_table:
            if entry.state == SlotState.OCCUPIED:
                self.insert(entry.key, entry.value)


if __name__ == "__main__":
    m = FlatHashMap(4)
    assert m.insert(5, 100) is True
    assert m.insert(9, 200) is True
    assert m.insert(5, 150) is False
    assert m.get(5) == 150
    assert m.get(9) == 200

    assert m.remove(5) is True
    assert m.get(5) is None
    assert m.get(9) == 200  # Probing past tombstone

    for i in range(50):
        m.insert(i * 10, i)
    for i in range(50):
        assert m.get(i * 10) == i

    print("All Python 3 self-tests for HASH-0001 passed successfully.")
