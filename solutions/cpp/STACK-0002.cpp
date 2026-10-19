/**
 * STACK-0002: Next Greater Element with Circular Invariant
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(N) Auxiliary Space
 * Companion: Contains Quadratic Baseline Oracle for differential testing
 */

#include <iostream>
#include <vector>
#include <cstdint>
#include <span>
#include <cassert>

namespace alg {

/**
 * Finds next greater element in a circular array using a Monotonic Stack.
 * Complexity: O(N) Time, O(N) Auxiliary Space.
 * Conforms to ISO C++20 standard.
 */
std::vector<int64_t> next_greater_elements(std::span<const int64_t> arr) {
    const size_t n = arr.size();
    if (n == 0) {
        return {};
    }

    std::vector<int64_t> result(n, -1);
    std::vector<size_t> stack; // Stores indices
    stack.reserve(n);

    const size_t virtual_length = 2 * n;

    for (size_t i = 0; i < virtual_length; ++i) {
        const size_t curr_idx = i % n;
        const int64_t current_val = arr[curr_idx];

        // Maintain strictly decreasing value invariant from bottom to top
        while (!stack.empty() && arr[stack.back()] < current_val) {
            size_t resolved_idx = stack.back();
            stack.pop_back();
            result[resolved_idx] = current_val;
        }

        // Only push indices during the first circular pass
        if (i < n) {
            stack.push_back(curr_idx);
        }
    }

    return result;
}

} // namespace alg

// Differential Quadratic Oracle
std::vector<int64_t> next_greater_oracle(std::span<const int64_t> arr) {
    const size_t n = arr.size();
    if (n == 0) return {};
    std::vector<int64_t> result(n, -1);

    for (size_t i = 0; i < n; ++i) {
        for (size_t step = 1; step < n; ++step) {
            size_t j = (i + step) % n;
            if (arr[j] > arr[i]) {
                result[i] = arr[j];
                break;
            }
        }
    }
    return result;
}

int main() {
    std::vector<int64_t> t1{1, 2, 1};
    auto r1 = alg::next_greater_elements(t1);
    auto o1 = next_greater_oracle(t1);
    assert(r1 == o1);
    std::vector<int64_t> exp1{2, -1, 2};
    assert(r1 == exp1);

    std::vector<int64_t> t2{1, 2, 3, 4, 3};
    auto r2 = alg::next_greater_elements(t2);
    auto o2 = next_greater_oracle(t2);
    assert(r2 == o2);
    std::vector<int64_t> exp2{2, 3, 4, -1, 4};
    assert(r2 == exp2);

    // Single element
    std::vector<int64_t> t3{42};
    auto r3 = alg::next_greater_elements(t3);
    assert(r3 == std::vector<int64_t>{-1});

    std::cout << "All C++20 assertions for STACK-0002 passed successfully." << std::endl;
    return 0;
}
