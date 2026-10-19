"""
MATH-0001: Strict Two-Sum Uniqueness and Invariant Verification
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Linear Two-Pointer implementation and Quadratic Oracle for differential validation.
"""

from typing import Sequence, Optional, NamedTuple


class PairIndices(NamedTuple):
    left: int
    right: int


def find_sorted_two_sum(arr: Sequence[int], target: int) -> Optional[PairIndices]:
    """
    Finds two distinct indices in a sorted sequence summing to target.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    if len(arr) < 2:
        return None

    left: int = 0
    right: int = len(arr) - 1

    while left < right:
        current_sum: int = arr[left] + arr[right]

        if current_sum == target:
            return PairIndices(left, right)
        elif current_sum > target:
            right -= 1
        else:
            left += 1

    return None


def find_sorted_two_sum_oracle(arr: Sequence[int], target: int) -> Optional[PairIndices]:
    """Quadratic baseline oracle for differential verification (O(N^2))."""
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] + arr[j] == target:
                return PairIndices(i, j)
    return None


if __name__ == "__main__":
    data = [1, 3, 5, 8, 12, 15, 19]
    ans = find_sorted_two_sum(data, 17)
    oracle_ans = find_sorted_two_sum_oracle(data, 17)
    assert ans == oracle_ans == PairIndices(2, 4), f"Failed: {ans}"

    assert find_sorted_two_sum(data, 100) is None
    print("All Python 3 self-tests for MATH-0001 passed successfully.")
