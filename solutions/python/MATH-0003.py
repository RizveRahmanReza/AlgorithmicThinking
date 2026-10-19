"""
MATH-0003: Amortized Analysis of Dynamic Array Geometric Growth
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Demonstrates: O(1) Amortized Geometric Resizing vs O(N) Arithmetic Degradation
"""

from typing import NamedTuple


class SimulationMetrics(NamedTuple):
    total_operations: int
    total_copies: int
    amortized_cost_per_op: float


def simulate_geometric_appends(n: int) -> SimulationMetrics:
    """
    Simulates append cost under Geometric Growth (x2).
    Target: Python 3.12+ (O(N) total operations, O(1) space).
    """
    if n <= 0:
        return SimulationMetrics(0, 0, 0.0)

    capacity = 1
    size = 0
    total_ops = 0
    total_copies = 0

    for _ in range(n):
        if size == capacity:
            total_copies += size
            total_ops += size
            capacity *= 2
        total_ops += 1
        size += 1

    return SimulationMetrics(
        total_operations=total_ops,
        total_copies=total_copies,
        amortized_cost_per_op=total_ops / n
    )


def simulate_arithmetic_appends(n: int, k: int) -> SimulationMetrics:
    """Simulates append cost under Arithmetic Growth (+K)."""
    if n <= 0 or k <= 0:
        return SimulationMetrics(0, 0, 0.0)

    capacity = k
    size = 0
    total_ops = 0
    total_copies = 0

    for _ in range(n):
        if size == capacity:
            total_copies += size
            total_ops += size
            capacity += k
        total_ops += 1
        size += 1

    return SimulationMetrics(
        total_operations=total_ops,
        total_copies=total_copies,
        amortized_cost_per_op=total_ops / n
    )


if __name__ == "__main__":
    N = 100000
    geom = simulate_geometric_appends(N)
    assert geom.amortized_cost_per_op < 3.0, f"Geometric failed: {geom}"

    arith = simulate_arithmetic_appends(N, 100)
    assert arith.amortized_cost_per_op > 100.0, f"Arithmetic failed: {arith}"

    print(f"All Python 3 self-tests for MATH-0003 passed.\n"
          f"Geometric Amortized Cost: {geom.amortized_cost_per_op:.4f} ops/insert\n"
          f"Arithmetic (+100) Amortized Cost: {arith.amortized_cost_per_op:.4f} ops/insert")
