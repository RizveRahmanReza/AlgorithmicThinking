from typing import List, Tuple

def three_way_partition(arr: List[int], pivot: int) -> Tuple[int, int]:
    """
    In-place Dutch National Flag 3-way partitioning.
    Rearranges arr into three contiguous blocks:
      arr[0 : low]        < pivot
      arr[low : high + 1] == pivot
      arr[high + 1 : N]   > pivot
    Returns (low, high).
    """
    low = 0
    mid = 0
    high = len(arr) - 1

    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == pivot:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
            # Do not increment mid; examine swapped value from high

    return low, high

def reference_partition(arr: List[int], pivot: int) -> List[int]:
    """Stable out-of-place oracle partition for validation."""
    lt = [x for x in arr if x < pivot]
    eq = [x for x in arr if x == pivot]
    gt = [x for x in arr if x > pivot]
    return lt + eq + gt

def verify_invariants(arr: List[int], pivot: int, low: int, high: int) -> bool:
    """Verifies that the Dutch National Flag partitioning invariants hold strictly."""
    for i in range(low):
        if arr[i] >= pivot:
            return False
    for i in range(low, high + 1):
        if arr[i] != pivot:
            return False
    for i in range(high + 1, len(arr)):
        if arr[i] <= pivot:
            return False
    return True
