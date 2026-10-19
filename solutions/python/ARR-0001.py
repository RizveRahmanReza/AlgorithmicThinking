"""
ARR-0001: In-Place Array Rotation and Cache Line Alignment
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Three-Step Reversal in-place algorithm and Quadratic Oracle for differential validation.
"""

from typing import MutableSequence


def reverse_range(arr: MutableSequence[int], left: int, right: int) -> None:
    """Reverses elements in arr between indices left and right in-place."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def rotate_right_in_place(arr: MutableSequence[int], k: int) -> None:
    """
    Rotates arr in place cyclically to the right by k positions.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    n = len(arr)
    if n <= 1:
        return

    effective_k = k % n
    if effective_k == 0:
        return

    split_point = n - effective_k

    # Step 1: Reverse prefix [0 ... split_point - 1]
    reverse_range(arr, 0, split_point - 1)
    # Step 2: Reverse suffix [split_point ... n - 1]
    reverse_range(arr, split_point, n - 1)
    # Step 3: Reverse entire array [0 ... n - 1]
    reverse_range(arr, 0, n - 1)


def rotate_right_oracle(arr: MutableSequence[int], k: int) -> None:
    """Quadratic baseline oracle for differential testing (O(N * k))."""
    n = len(arr)
    if n <= 1:
        return
    eff_k = k % n
    for _ in range(eff_k):
        last = arr[-1]
        for i in range(n - 1, 0, -1):
            arr[i] = arr[i - 1]
        arr[0] = last


if __name__ == "__main__":
    t1 = [1, 2, 3, 4, 5, 6, 7]
    o1 = list(t1)
    rotate_right_in_place(t1, 3)
    rotate_right_oracle(o1, 3)
    assert t1 == o1 == [5, 6, 7, 1, 2, 3, 4], f"Failed: {t1}"

    t2 = [10, 20, 30, 40]
    rotate_right_in_place(t2, 10)
    assert t2 == [30, 40, 10, 20]

    print("All Python 3 self-tests for ARR-0001 passed successfully.")
