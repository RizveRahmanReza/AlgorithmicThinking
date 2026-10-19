/**
 * MATH-0002: Inversion Counting via Divide-and-Conquer
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N log N) Time, O(N) Auxiliary Space
 * Companion: Contains Quadratic Oracle O(N^2) for differential verification
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <stdexcept>
#include <cassert>

namespace internal {

int64_t merge_and_count(
    std::span<int64_t> arr, 
    std::vector<int64_t>& temp, 
    size_t left, 
    size_t mid, 
    size_t right
) {
    size_t p = left;      // Pointer for left sorted half
    size_t q = mid + 1;   // Pointer for right sorted half
    size_t k = left;      // Pointer for temp merged buffer
    int64_t split_inversions = 0;

    while (p <= mid && q <= right) {
        if (arr[p] <= arr[q]) {
            temp[k++] = arr[p++];
        } else {
            temp[k++] = arr[q++];
            // Invariant: arr[p] > arr[q], meaning all elements arr[p ... mid] are > arr[q]
            split_inversions += static_cast<int64_t>(mid - p + 1);
        }
    }

    while (p <= mid) {
        temp[k++] = arr[p++];
    }
    while (q <= right) {
        temp[k++] = arr[q++];
    }

    for (size_t idx = left; idx <= right; ++idx) {
        arr[idx] = temp[idx];
    }

    return split_inversions;
}

int64_t sort_and_count(
    std::span<int64_t> arr, 
    std::vector<int64_t>& temp, 
    size_t left, 
    size_t right
) {
    if (left >= right) {
        return 0;
    }

    size_t mid = left + (right - left) / 2;
    int64_t inv_count = 0;

    inv_count += sort_and_count(arr, temp, left, mid);
    inv_count += sort_and_count(arr, temp, mid + 1, right);
    inv_count += merge_and_count(arr, temp, left, mid, right);

    return inv_count;
}

} // namespace internal

/**
 * Counts total inversions in O(N log N) time and O(N) space.
 * Conforms to ISO C++20 standard.
 */
int64_t count_inversions(std::span<const int64_t> input) {
    if (input.size() <= 1) {
        return 0;
    }

    std::vector<int64_t> arr(input.begin(), input.end());
    std::vector<int64_t> temp(arr.size());

    return internal::sort_and_count(arr, temp, 0, arr.size() - 1);
}

// Differential Oracle (O(N^2))
int64_t count_inversions_oracle(std::span<const int64_t> arr) {
    int64_t count = 0;
    for (size_t i = 0; i < arr.size(); ++i) {
        for (size_t j = i + 1; j < arr.size(); ++j) {
            if (arr[i] > arr[j]) {
                ++count;
            }
        }
    }
    return count;
}

int main() {
    std::vector<int64_t> sample{8, 4, 2, 1};
    assert(count_inversions(sample) == 6);
    assert(count_inversions_oracle(sample) == 6);

    std::vector<int64_t> mixed{2, 4, 1, 3, 5};
    assert(count_inversions(mixed) == 3);
    assert(count_inversions_oracle(mixed) == 3);

    std::vector<int64_t> sorted{1, 2, 3, 4, 5};
    assert(count_inversions(sorted) == 0);

    std::cout << "All C++20 test assertions for MATH-0002 passed successfully." << std::endl;
    return 0;
}
