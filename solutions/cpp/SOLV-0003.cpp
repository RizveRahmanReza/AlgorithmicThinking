/**
 * SOLV-0003: Maximum Subarray Sum: From O(N^3) to O(N) Kadane's Invariant
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
#include <stdexcept>
#include <cassert>

struct SubarrayResult {
    int64_t max_sum;
    size_t left_index;
    size_t right_index;

    bool operator==(const SubarrayResult& other) const = default;
};

/**
 * Computes maximum contiguous subarray sum in O(N) time and O(1) space.
 * Conforms to ISO C++20 standard.
 */
SubarrayResult find_max_subarray_kadane(std::span<const int64_t> arr) {
    if (arr.empty()) {
        throw std::invalid_argument("Input array must be non-empty.");
    }

    int64_t current_sum = arr[0];
    size_t current_left = 0;

    SubarrayResult best{
        .max_sum = arr[0],
        .left_index = 0,
        .right_index = 0
    };

    for (size_t j = 1; j < arr.size(); ++j) {
        const int64_t val = arr[j];

        if (current_sum > 0) {
            current_sum += val;
        } else {
            current_sum = val;
            current_left = j;
        }

        if (current_sum > best.max_sum) {
            best.max_sum = current_sum;
            best.left_index = current_left;
            best.right_index = j;
        } else if (current_sum == best.max_sum) {
            size_t curr_len = j - current_left + 1;
            size_t best_len = best.right_index - best.left_index + 1;
            if (curr_len < best_len) {
                best.left_index = current_left;
                best.right_index = j;
            }
        }
    }

    return best;
}

/**
 * Quadratic Oracle for differential testing (O(N^2)).
 */
SubarrayResult find_max_subarray_oracle(std::span<const int64_t> arr) {
    if (arr.empty()) throw std::invalid_argument("Empty array.");
    
    SubarrayResult best{
        .max_sum = arr[0],
        .left_index = 0,
        .right_index = 0
    };

    for (size_t i = 0; i < arr.size(); ++i) {
        int64_t sum = 0;
        for (size_t j = i; j < arr.size(); ++j) {
            sum += arr[j];
            if (sum > best.max_sum) {
                best.max_sum = sum;
                best.left_index = i;
                best.right_index = j;
            } else if (sum == best.max_sum) {
                size_t curr_len = j - i + 1;
                size_t best_len = best.right_index - best.left_index + 1;
                if (curr_len < best_len) {
                    best.left_index = i;
                    best.right_index = j;
                }
            }
        }
    }
    return best;
}

int main() {
    // Test 1: Mixed Sequence
    std::vector<int64_t> test_arr{-2, 1, -3, 4, -1, 2, 1, -5, 4};
    auto res_kadane = find_max_subarray_kadane(test_arr);
    auto res_oracle = find_max_subarray_oracle(test_arr);

    assert(res_kadane == res_oracle);
    assert(res_kadane.max_sum == 6);
    assert(res_kadane.left_index == 3);
    assert(res_kadane.right_index == 6);

    // Test 2: All Negative
    std::vector<int64_t> neg_arr{-5, -2, -9, -3};
    auto neg_k = find_max_subarray_kadane(neg_arr);
    auto neg_o = find_max_subarray_oracle(neg_arr);
    assert(neg_k == neg_o);
    assert(neg_k.max_sum == -2);
    assert(neg_k.left_index == 1);
    assert(neg_k.right_index == 1);

    std::cout << "All C++20 differential test assertions for SOLV-0003 passed." << std::endl;
    return 0;
}
