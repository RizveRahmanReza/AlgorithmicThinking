"""
STACK-0002: Next Greater Element with Circular Invariant
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Monotonic Stack implementation and Quadratic Oracle for differential validation.
"""

from typing import Sequence


def next_greater_elements(arr: Sequence[int]) -> list[int]:
    """
    Finds next greater element in circular array using a Monotonic Stack.
    Target: Python 3.12+ (O(N) Time, O(N) Auxiliary Space).
    """
    n = len(arr)
    if n == 0:
        return []

    result = [-1] * n
    stack: list[int] = []  # Stores indices

    for i in range(2 * n):
        curr_idx = i % n
        curr_val = arr[curr_idx]

        while stack and arr[stack[-1]] < curr_val:
            resolved_idx = stack.pop()
            result[resolved_idx] = curr_val

        if i < n:
            stack.append(curr_idx)

    return result


def next_greater_oracle(arr: Sequence[int]) -> list[int]:
    """Quadratic baseline oracle for differential testing."""
    n = len(arr)
    if n == 0:
        return []
    result = [-1] * n
    for i in range(n):
        for step in range(1, n):
            j = (i + step) % n
            if arr[j] > arr[i]:
                result[i] = arr[j]
                break
    return result


if __name__ == "__main__":
    t1 = [1, 2, 1]
    r1 = next_greater_elements(t1)
    o1 = next_greater_oracle(t1)
    assert r1 == o1 == [2, -1, 2], f"Failed: {r1}"

    t2 = [1, 2, 3, 4, 3]
    r2 = next_greater_elements(t2)
    o2 = next_greater_oracle(t2)
    assert r2 == o2 == [2, 3, 4, -1, 4], f"Failed: {r2}"

    print("All Python 3 self-tests for STACK-0002 passed successfully.")
