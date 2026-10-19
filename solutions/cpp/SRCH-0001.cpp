/**
 * SRCH-0001: Capacity Allocation via Binary Search on Answer Space
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N * log(Sum(W))) Time, O(1) Auxiliary Space
 * Companion: Contains Linear Search Baseline Oracle for differential testing
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <numeric>
#include <algorithm>
#include <span>
#include <stdexcept>
#include <cassert>

namespace alg {

/**
 * Evaluates whether packages can be shipped within max_days using given capacity.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 */
bool can_ship_within_days(
    std::span<const int64_t> weights, 
    int64_t max_days, 
    int64_t capacity
) noexcept {
    int64_t days_used = 1;
    int64_t current_day_load = 0;

    for (int64_t w : weights) {
        if (current_day_load + w > capacity) {
            ++days_used;
            current_day_load = w;
            if (days_used > max_days) {
                return false;
            }
        } else {
            current_day_load += w;
        }
    }

    return true;
}

/**
 * Finds minimum ship capacity using Binary Search on Answer Space.
 * Complexity: O(N * log(Sum(W))) Time, O(1) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
int64_t ship_within_days(std::span<const int64_t> weights, int64_t max_days) {
    if (weights.empty() || max_days <= 0) {
        throw std::invalid_argument("Invalid weights or deadline.");
    }

    int64_t left = *std::max_element(weights.begin(), weights.end());
    int64_t right = std::accumulate(weights.begin(), weights.end(), int64_t{0});

    while (left < right) {
        int64_t mid = left + (right - left) / 2;

        if (can_ship_within_days(weights, max_days, mid)) {
            right = mid;      // mid is feasible, try smaller
        } else {
            left = mid + 1;   // mid is infeasible, must increase
        }
    }

    return left;
}

} // namespace alg

// Differential Linear Search Baseline Oracle
int64_t ship_within_days_oracle(std::span<const int64_t> weights, int64_t max_days) {
    int64_t cap = *std::max_element(weights.begin(), weights.end());
    while (!alg::can_ship_within_days(weights, max_days, cap)) {
        ++cap;
    }
    return cap;
}

int main() {
    std::vector<int64_t> t1{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto r1 = alg::ship_within_days(t1, 5);
    auto o1 = ship_within_days_oracle(t1, 5);
    assert(r1 == o1 && r1 == 15);

    std::vector<int64_t> t2{3, 2, 2, 4, 1, 4};
    auto r2 = alg::ship_within_days(t2, 3);
    auto o2 = ship_within_days_oracle(t2, 3);
    assert(r2 == o2 && r2 == 6);

    std::vector<int64_t> t3{1, 2, 3, 1, 1};
    auto r3 = alg::ship_within_days(t3, 4);
    assert(r3 == 3);

    std::cout << "All C++20 assertions for SRCH-0001 passed successfully." << std::endl;
    return 0;
}
