"""
SOLV-0001: The Anomaly Subsegment Identification
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic, O(N) Time, O(1) Auxiliary Space)
"""

from typing import Sequence, NamedTuple


class SubarrayResult(NamedTuple):
    max_sum: int
    left_index: int
    right_index: int


def find_maximum_anomaly_subsegment(arr: Sequence[int]) -> SubarrayResult:
    """
    Identifies the contiguous subsegment maximizing the sum of elements.
    
    Invariant:
    current_sum maintains the maximum subarray sum ending at index i.
    best_result stores the global maximum subarray across prefix [0 ... i].
    
    Tie-breaking:
    1. Maximum sum.
    2. Shortest window length.
    3. Smallest left starting index.
    """
    if not arr:
        raise ValueError("Input sequence must not be empty.")

    current_sum: int = arr[0]
    current_left: int = 0

    best_max_sum: int = arr[0]
    best_left: int = 0
    best_right: int = 0

    for i in range(1, len(arr)):
        val: int = arr[i]

        if current_sum > 0:
            current_sum += val
        else:
            current_sum = val
            current_left = i

        if current_sum > best_max_sum:
            best_max_sum = current_sum
            best_left = current_left
            best_right = i
        elif current_sum == best_max_sum:
            current_len = i - current_left + 1
            best_len = best_right - best_left + 1
            if current_len < best_len:
                best_left = current_left
                best_right = i

    return SubarrayResult(best_max_sum, best_left, best_right)


if __name__ == "__main__":
    # Self-test harness
    r1 = find_maximum_anomaly_subsegment([2, -4, 3, -1, 4, -6, 2])
    assert r1 == SubarrayResult(6, 2, 4), f"Failed test 1: {r1}"

    r2 = find_maximum_anomaly_subsegment([-8, -3, -9, -4])
    assert r2 == SubarrayResult(-3, 1, 1), f"Failed test 2: {r2}"

    r3 = find_maximum_anomaly_subsegment([1, 2, 3, 4])
    assert r3 == SubarrayResult(10, 0, 3), f"Failed test 3: {r3}"

    r4 = find_maximum_anomaly_subsegment([42])
    assert r4 == SubarrayResult(42, 0, 0), f"Failed test 4: {r4}"

    r5 = find_maximum_anomaly_subsegment([5, -6, 5, -6, 5])
    assert r5 == SubarrayResult(5, 0, 0), f"Failed test 5: {r5}"

    print("All Python 3 self-tests for SOLV-0001 passed successfully.")
