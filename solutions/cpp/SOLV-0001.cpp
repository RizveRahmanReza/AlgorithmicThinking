/**
 * SOLV-0001: The Anomaly Subsegment Identification
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(1) Auxiliary Space
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <limits>
#include <span>
#include <stdexcept>
#include <cassert>

struct SubarrayResult {
    int64_t max_sum;
    size_t left_index;
    size_t right_index;

    bool operator==(const SubarrayResult& other) const = default;
};

/**
 * Finds the maximum contiguous subarray sum and its exact boundary indices.
 *
 * Invariant:
 * At iteration i, current_sum is the maximum contiguous subarray sum ending at i.
 * best_result stores the global optimal subarray across prefix [0 ... i].
 */
SubarrayResult find_maximum_anomaly_subsegment(std::span<const int64_t> arr) {
    if (arr.empty()) {
        throw std::invalid_argument("Input sequence must not be empty.");
    }

    int64_t current_sum = arr[0];
    size_t current_left = 0;

    SubarrayResult best_result{
        .max_sum = arr[0],
        .left_index = 0,
        .right_index = 0
    };

    for (size_t i = 1; i < arr.size(); ++i) {
        const int64_t val = arr[i];

        // Inductive choice: extend existing subsegment or reset from index i
        if (current_sum > 0) {
            current_sum += val;
        } else {
            current_sum = val;
            current_left = i;
        }

        // Global best evaluation and tie-breaking
        if (current_sum > best_result.max_sum) {
            best_result.max_sum = current_sum;
            best_result.left_index = current_left;
            best_result.right_index = i;
        } else if (current_sum == best_result.max_sum) {
            size_t current_len = i - current_left + 1;
            size_t best_len = best_result.right_index - best_result.left_index + 1;
            if (current_len < best_len) {
                best_result.left_index = current_left;
                best_result.right_index = i;
            }
        }
    }

    return best_result;
}

// Verification Test Suite
int main() {
    // Test 1: Mixed values
    std::vector<int64_t> t1{2, -4, 3, -1, 4, -6, 2};
    auto r1 = find_maximum_anomaly_subsegment(t1);
    assert(r1.max_sum == 6 && r1.left_index == 2 && r1.right_index == 4);

    // Test 2: All negative values
    std::vector<int64_t> t2{-8, -3, -9, -4};
    auto r2 = find_maximum_anomaly_subsegment(t2);
    assert(r2.max_sum == -3 && r2.left_index == 1 && r2.right_index == 1);

    // Test 3: All positive values
    std::vector<int64_t> t3{1, 2, 3, 4};
    auto r3 = find_maximum_anomaly_subsegment(t3);
    assert(r3.max_sum == 10 && r3.left_index == 0 && r3.right_index == 3);

    // Test 4: Single element
    std::vector<int64_t> t4{42};
    auto r4 = find_maximum_anomaly_subsegment(t4);
    assert(r4.max_sum == 42 && r4.left_index == 0 && r4.right_index == 0);

    // Test 5: Alternating reset with tie-break (shortest window)
    std::vector<int64_t> t5{5, -6, 5, -6, 5};
    auto r5 = find_maximum_anomaly_subsegment(t5);
    assert(r5.max_sum == 5 && r5.left_index == 0 && r5.right_index == 0);

    std::cout << "All C++20 test assertions for SOLV-0001 passed successfully." << std::endl;
    return 0;
}
