"""
SRCH-0001: Capacity Allocation via Binary Search on Answer Space
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Binary Search on Answer implementation and Linear Search Oracle.
"""

from typing import Sequence


def can_ship_within_days(weights: Sequence[int], max_days: int, capacity: int) -> bool:
    """Evaluates feasibility of capacity under greedy allocation."""
    days_used = 1
    current_load = 0

    for w in weights:
        if current_load + w > capacity:
            days_used += 1
            current_load = w
            if days_used > max_days:
                return False
        else:
            current_load += w

    return True


def ship_within_days(weights: Sequence[int], max_days: int) -> int:
    """
    Finds minimum capacity using Binary Search on Answer Space.
    Target: Python 3.12+ (O(N * log(Sum(W))) Time, O(1) Auxiliary Space).
    """
    if not weights or max_days <= 0:
        raise ValueError("Invalid weights or max_days.")

    left = max(weights)
    right = sum(weights)

    while left < right:
        mid = left + (right - left) // 2

        if can_ship_within_days(weights, max_days, mid):
            right = mid
        else:
            left = mid + 1

    return left


def ship_within_days_oracle(weights: Sequence[int], max_days: int) -> int:
    """Linear search baseline oracle for differential testing."""
    cap = max(weights)
    while not can_ship_within_days(weights, max_days, cap):
        cap += 1
    return cap


if __name__ == "__main__":
    t1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    r1 = ship_within_days(t1, 5)
    o1 = ship_within_days_oracle(t1, 5)
    assert r1 == o1 == 15, f"Failed: {r1}"

    t2 = [3, 2, 2, 4, 1, 4]
    r2 = ship_within_days(t2, 3)
    o2 = ship_within_days_oracle(t2, 3)
    assert r2 == o2 == 6, f"Failed: {r2}"

    print("All Python 3 self-tests for SRCH-0001 passed successfully.")
