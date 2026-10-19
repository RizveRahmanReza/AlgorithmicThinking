"""
MATH-0002: Inversion Counting via Divide-and-Conquer
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Linearithmic MergeSort counting implementation and Quadratic Oracle for differential validation.
"""

from typing import Sequence


def count_inversions(arr: Sequence[int]) -> int:
    """
    Computes total inversions in O(N log N) time and O(N) auxiliary space.
    Target: Python 3.12+
    """
    if len(arr) <= 1:
        return 0

    mutable_arr = list(arr)
    temp_buffer = [0] * len(mutable_arr)

    def _sort_and_count(left: int, right: int) -> int:
        if left >= right:
            return 0

        mid = left + (right - left) // 2
        inv = _sort_and_count(left, mid)
        inv += _sort_and_count(mid + 1, right)

        # Merge and count split inversions
        p = left
        q = mid + 1
        k = left
        split_inv = 0

        while p <= mid and q <= right:
            if mutable_arr[p] <= mutable_arr[q]:
                temp_buffer[k] = mutable_arr[p]
                p += 1
            else:
                temp_buffer[k] = mutable_arr[q]
                q += 1
                # Key Invariant: elements mutable_arr[p ... mid] are all strictly greater than mutable_arr[q]
                split_inv += (mid - p + 1)
            k += 1

        while p <= mid:
            temp_buffer[k] = mutable_arr[p]
            p += 1
            k += 1

        while q <= right:
            temp_buffer[k] = mutable_arr[q]
            q += 1
            k += 1

        mutable_arr[left:right + 1] = temp_buffer[left:right + 1]
        return inv + split_inv

    return _sort_and_count(0, len(mutable_arr) - 1)


def count_inversions_oracle(arr: Sequence[int]) -> int:
    """Quadratic baseline oracle for differential verification (O(N^2))."""
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


if __name__ == "__main__":
    t1 = [8, 4, 2, 1]
    assert count_inversions(t1) == count_inversions_oracle(t1) == 6

    t2 = [2, 4, 1, 3, 5]
    assert count_inversions(t2) == count_inversions_oracle(t2) == 3

    t3 = [1, 2, 3, 4]
    assert count_inversions(t3) == 0

    print("All Python 3 self-tests for MATH-0002 passed successfully.")
