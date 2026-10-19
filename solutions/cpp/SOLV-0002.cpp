/**
 * SOLV-0002: Stable Resource Allocation Under Capacity Constraints
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N log N) Time, O(N) Auxiliary Space
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <algorithm>
#include <span>
#include <optional>
#include <stdexcept>
#include <cassert>

struct JobRequest {
    int64_t start_time;
    int64_t end_time;
    int64_t capacity;
};

struct AllocationAudit {
    bool is_feasible;
    int64_t peak_capacity;
    std::optional<int64_t> first_violation_time;

    bool operator==(const AllocationAudit& other) const = default;
};

// Event representation for Sweep-Line
struct ResourceEvent {
    int64_t timestamp;
    int64_t capacity_delta; // Negative for release, positive for acquisition

    // Tie-break invariant: if timestamps are identical, process negative deltas (releases) first
    bool operator<(const ResourceEvent& other) const noexcept {
        if (timestamp != other.timestamp) {
            return timestamp < other.timestamp;
        }
        return capacity_delta < other.capacity_delta;
    }
};

/**
 * Audits interval resource allocation using an O(N log N) sweep-line algorithm.
 * Conforms to ISO C++20 standard.
 */
AllocationAudit audit_resource_allocation(
    std::span<const JobRequest> jobs, 
    int64_t global_capacity
) {
    std::vector<ResourceEvent> events;
    events.reserve(jobs.size() * 2);

    for (const auto& job : jobs) {
        if (job.start_time >= job.end_time || job.capacity <= 0) {
            throw std::invalid_argument("Invalid job parameters: must have start < end and capacity > 0.");
        }
        events.push_back(ResourceEvent{job.start_time, job.capacity});
        events.push_back(ResourceEvent{job.end_time, -job.capacity});
    }

    std::sort(events.begin(), events.end());

    int64_t current_capacity = 0;
    int64_t peak_capacity = 0;
    std::optional<int64_t> violation_time = std::nullopt;

    for (const auto& ev : events) {
        current_capacity += ev.capacity_delta;

        if (current_capacity > peak_capacity) {
            peak_capacity = current_capacity;
        }

        if (current_capacity > global_capacity && !violation_time.has_value()) {
            violation_time = ev.timestamp;
        }
    }

    return AllocationAudit{
        .is_feasible = !violation_time.has_value(),
        .peak_capacity = peak_capacity,
        .first_violation_time = violation_time
    };
}

int main() {
    // Test 1: Standard Feasible Case
    std::vector<JobRequest> t1{
        {1, 5, 10},
        {2, 8, 4},
        {5, 9, 3}
    };
    auto r1 = audit_resource_allocation(t1, 15);
    assert(r1.is_feasible == true);
    assert(r1.peak_capacity == 14);
    assert(!r1.first_violation_time.has_value());

    // Test 2: Abutting intervals at timestamp 5 (no overlap)
    std::vector<JobRequest> t2{
        {1, 5, 10},
        {5, 10, 10}
    };
    auto r2 = audit_resource_allocation(t2, 10);
    assert(r2.is_feasible == true);
    assert(r2.peak_capacity == 10);

    // Test 3: Capacity Violation at timestamp 2
    std::vector<JobRequest> t3{
        {1, 5, 10},
        {2, 6, 5}
    };
    auto r3 = audit_resource_allocation(t3, 12);
    assert(r3.is_feasible == false);
    assert(r3.peak_capacity == 15);
    assert(r3.first_violation_time.value() == 2);

    std::cout << "All C++20 test assertions for SOLV-0002 passed successfully." << std::endl;
    return 0;
}
