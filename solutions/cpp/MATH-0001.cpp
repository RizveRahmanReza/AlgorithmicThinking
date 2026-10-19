/**
 * MATH-0001: Strict Two-Sum Uniqueness and Invariant Verification
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(1) Auxiliary Space
 * Companion: Contains Quadratic Oracle O(N^2) for differential verification
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <optional>
#include <utility>
#include <cassert>

struct PairIndices {
    size_t left;
    size_t right;

    bool operator==(const PairIndices& other) const = default;
};

/**
 * Finds two distinct indices in a sorted sequence summing to target.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 * Standard: ISO C++20.
 */
std::optional<PairIndices> find_sorted_two_sum(
    std::span<const int64_t> arr, 
    int64_t target
) {
    if (arr.size() < 2) {
        return std::nullopt;
    }

    size_t left = 0;
    size_t right = arr.size() - 1;

    while (left < right) {
        const int64_t current_sum = arr[left] + arr[right];

        if (current_sum == target) {
            return PairIndices{.left = left, .right = right};
        } else if (current_sum > target) {
            --right;
        } else {
            ++left;
        }
    }

    return std::nullopt;
}

/**
 * Quadratic Oracle for differential testing (O(N^2)).
 */
std::optional<PairIndices> find_sorted_two_sum_oracle(
    std::span<const int64_t> arr,
    int64_t target
) {
    for (size_t i = 0; i < arr.size(); ++i) {
        for (size_t j = i + 1; j < arr.size(); ++j) {
            if (arr[i] + arr[j] == target) {
                return PairIndices{.left = i, .right = j};
            }
        }
    }
    return std::nullopt;
}

int main() {
    std::vector<int64_t> test_arr{1, 3, 5, 8, 12, 15, 19};
    auto res = find_sorted_two_sum(test_arr, 17);
    auto oracle_res = find_sorted_two_sum_oracle(test_arr, 17);

    assert(res.has_value() && oracle_res.has_value());
    assert(res.value() == oracle_res.value());
    assert(res.value().left == 2 && res.value().right == 4);

    // Negative case
    auto not_found = find_sorted_two_sum(test_arr, 100);
    assert(!not_found.has_value());

    std::cout << "All C++20 test assertions for MATH-0001 passed successfully." << std::endl;
    return 0;
}
