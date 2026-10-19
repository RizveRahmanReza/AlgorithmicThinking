/**
 * ARR-0001: In-Place Array Rotation and Cache Line Alignment
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(1) Auxiliary Space
 * Companion: Contains Quadratic Oracle O(N * k) for differential verification
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <utility>
#include <cassert>

namespace alg {

/**
 * Reverses a contiguous subsegment [left, right] in place.
 * Preserves high spatial locality.
 */
void reverse_range(std::span<int64_t> arr, size_t left, size_t right) {
    while (left < right) {
        std::swap(arr[left], arr[right]);
        ++left;
        --right;
    }
}

/**
 * Rotates an array in-place cyclically to the right by k positions.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
void rotate_right_in_place(std::span<int64_t> arr, uint64_t k) {
    const size_t n = arr.size();
    if (n <= 1) {
        return;
    }

    const size_t effective_k = static_cast<size_t>(k % n);
    if (effective_k == 0) {
        return;
    }

    const size_t split_point = n - effective_k;

    // Step 1: Reverse prefix [0 ... split_point - 1]
    reverse_range(arr, 0, split_point - 1);

    // Step 2: Reverse suffix [split_point ... n - 1]
    reverse_range(arr, split_point, n - 1);

    // Step 3: Reverse entire array [0 ... n - 1]
    reverse_range(arr, 0, n - 1);
}

} // namespace alg

// Differential Quadratic Baseline Oracle
void rotate_right_oracle(std::vector<int64_t>& arr, uint64_t k) {
    if (arr.size() <= 1) return;
    size_t n = arr.size();
    size_t eff_k = static_cast<size_t>(k % n);
    for (size_t s = 0; s < eff_k; ++s) {
        int64_t last = arr.back();
        for (size_t i = n - 1; i > 0; --i) {
            arr[i] = arr[i - 1];
        }
        arr[0] = last;
    }
}

int main() {
    std::vector<int64_t> test_arr{1, 2, 3, 4, 5, 6, 7};
    std::vector<int64_t> oracle_arr = test_arr;

    alg::rotate_right_in_place(test_arr, 3);
    rotate_right_oracle(oracle_arr, 3);

    assert(test_arr == oracle_arr);
    std::vector<int64_t> expected{5, 6, 7, 1, 2, 3, 4};
    assert(test_arr == expected);

    // Edge Case: k > n
    std::vector<int64_t> arr2{10, 20, 30, 40};
    alg::rotate_right_in_place(arr2, 10); // 10 % 4 = 2
    std::vector<int64_t> expected2{30, 40, 10, 20};
    assert(arr2 == expected2);

    std::cout << "All C++20 assertions for ARR-0001 passed successfully." << std::endl;
    return 0;
}
