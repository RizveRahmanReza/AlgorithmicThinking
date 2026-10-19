"""
SOLV-0002: Stable Resource Allocation Under Capacity Constraints
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic, O(N log N) Time, O(N) Auxiliary Space)
"""

from typing import Sequence, NamedTuple, Optional


class JobRequest(NamedTuple):
    start_time: int
    end_time: int
    capacity: int


class AllocationAudit(NamedTuple):
    is_feasible: bool
    peak_capacity: int
    first_violation_time: Optional[int]


def audit_resource_allocation(
    jobs: Sequence[JobRequest], 
    global_capacity: int
) -> AllocationAudit:
    """
    Evaluates dynamic capacity allocation feasibility using a Sweep-Line algorithm.
    Target: Python 3.12+ (O(N log N) time, O(N) auxiliary space).
    
    Invariant:
    Sorting ensures events at timestamp T with negative deltas (releases)
    are processed before events with positive deltas (allocations).
    """
    events: list[tuple[int, int]] = []
    for job in jobs:
        if job.start_time >= job.end_time or job.capacity <= 0:
            raise ValueError("Job must satisfy start_time < end_time and capacity > 0.")
        events.append((job.start_time, job.capacity))
        events.append((job.end_time, -job.capacity))

    # Sort key: primary = timestamp ASC, secondary = delta ASC
    # Negative delta sorts before positive delta for identical timestamps
    events.sort(key=lambda ev: (ev[0], ev[1]))

    current_capacity: int = 0
    peak_capacity: int = 0
    first_violation: Optional[int] = None

    for timestamp, delta in events:
        current_capacity += delta

        if current_capacity > peak_capacity:
            peak_capacity = current_capacity

        if current_capacity > global_capacity and first_violation is None:
            first_violation = timestamp

    return AllocationAudit(
        is_feasible=(first_violation is None),
        peak_capacity=peak_capacity,
        first_violation_time=first_violation
    )


if __name__ == "__main__":
    # Self-test harness
    t1 = [JobRequest(1, 5, 10), JobRequest(2, 8, 4), JobRequest(5, 9, 3)]
    r1 = audit_resource_allocation(t1, 15)
    assert r1 == AllocationAudit(True, 14, None), f"Failed test 1: {r1}"

    t2 = [JobRequest(1, 5, 10), JobRequest(5, 10, 10)]
    r2 = audit_resource_allocation(t2, 10)
    assert r2 == AllocationAudit(True, 10, None), f"Failed test 2: {r2}"

    t3 = [JobRequest(1, 5, 10), JobRequest(2, 6, 5)]
    r3 = audit_resource_allocation(t3, 12)
    assert r3 == AllocationAudit(False, 15, 2), f"Failed test 3: {r3}"

    print("All Python 3 self-tests for SOLV-0002 passed successfully.")
