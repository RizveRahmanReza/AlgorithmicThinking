"""
SOLV-0003: Maximum Subarray Sum: Evolution and Invariant Derivation
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains both Linear Kadane implementation and Quadratic Oracle for differential validation.
"""

from typing import Sequence, NamedTuple


class SubarrayResult(NamedTuple):
    max_sum: int
    left_index: int
    right_index: int


def find_max_subarray_kadane(arr: Sequence[int]) -> SubarrayResult:
    """
    Computes maximum subarray sum in O(N) time and O(1) space.
    Target: Python 3.12+
    """
    if not arr:
        raise ValueError("Input array must be non-empty.")

    current_sum: int = arr[0]
    current_left: int = 0

    best_sum: int = arr[0]
    best_left: int = 0
    best_right: int = 0

    for j in range(1, len(arr)):
        val: int = arr[j]

        if current_sum > 0:
            current_sum += val
        else:
            current_sum = val
            current_left = j

        if current_sum > best_sum:
            best_sum = current_sum
            best_left = current_left
            best_right = j
        elif current_sum == best_sum:
            curr_len = j - current_left + 1
            best_len = best_right - best_left + 1
            if curr_len < best_len:
                best_left = current_left
                best_right = j

    return SubarrayResult(best_sum, best_left, best_right)


def find_max_subarray_oracle(arr: Sequence[int]) -> SubarrayResult:
    """Quadratic oracle for differential verification (O(N^2))."""
    if not arr:
        raise ValueError("Input array must be non-empty.")

    best_sum = arr[0]
    best_left = 0
    best_right = 0

    n = len(arr)
    for i in range(n):
        curr_sum = 0
        for j in range(i, n):
            curr_sum += arr[j]
            if curr_sum > best_sum:
                best_sum = curr_sum
                best_left = i
                best_right = j
            elif curr_sum == best_sum:
                curr_len = j - i + 1
                best_len = best_right - best_left + 1
                if curr_len < best_len:
                    best_left = i
                    best_right = j

    return SubarrayResult(best_sum, best_left, best_right)


if __name__ == "__main__":
    sample = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    rk = find_max_subarray_kadane(sample)
    ro = find_max_subarray_oracle(sample)
    assert rk == ro == SubarrayResult(6, 3, 6), f"Mismatch: {rk} vs {ro}"

    neg = [-5, -2, -9, -3]
    nk = find_max_subarray_kadane(neg)
    no = find_max_subarray_oracle(neg)
    assert nk == no == SubarrayResult(-2, 1, 1), f"Mismatch: {nk} vs {no}"

    print("All Python 3 differential tests for SOLV-0003 passed successfully.")
