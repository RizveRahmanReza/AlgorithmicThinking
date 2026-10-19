#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cassert>

namespace fenw_0001 {

class FenwickTree {
private:
    int n;
    std::vector<int64_t> tree;

public:
    explicit FenwickTree(int size) : n(size), tree(size + 1, 0) {}

    // Adds delta to 1-based index i: O(log N)
    void update(int i, int64_t delta) {
        for (; i <= n; i += (i & -i)) {
            tree[i] += delta;
        }
    }

    // Computes prefix sum [1..i]: O(log N)
    int64_t query(int i) const {
        int64_t sum = 0;
        for (; i > 0; i -= (i & -i)) {
            sum += tree[i];
        }
        return sum;
    }

    // Computes range sum [l..r]: O(log N)
    int64_t query_range(int l, int r) const {
        if (l > r) return 0;
        return query(r) - query(l - 1);
    }
};

// Computes total inversions in an arbitrary sequence using coordinate compression and Fenwick Tree
int64_t count_inversions(const std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    if (n <= 1) return 0;

    // 1. Coordinate compression
    std::vector<int> sorted_unique = arr;
    std::sort(sorted_unique.begin(), sorted_unique.end());
    sorted_unique.erase(std::unique(sorted_unique.begin(), sorted_unique.end()), sorted_unique.end());

    int u = static_cast<int>(sorted_unique.size());
    FenwickTree bit(u);

    int64_t total_inversions = 0;

    // 2. Process stream
    for (int i = 0; i < n; ++i) {
        auto it = std::lower_bound(sorted_unique.begin(), sorted_unique.end(), arr[i]);
        int rank = static_cast<int>(std::distance(sorted_unique.begin(), it)) + 1;

        int64_t greater_count = i - bit.query(rank);
        total_inversions += greater_count;

        bit.update(rank, 1);
    }

    return total_inversions;
}

int64_t reference_count_inversions(const std::vector<int>& arr) {
    int64_t inv = 0;
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] > arr[j]) {
                inv++;
            }
        }
    }
    return inv;
}

} // namespace fenw_0001

int main() {
    using namespace fenw_0001;

    // Test 1: Reverse sorted array
    std::vector<int> a1 = {8, 4, 2, 1};
    assert(count_inversions(a1) == 6);
    assert(count_inversions(a1) == reference_count_inversions(a1));

    // Test 2: Already sorted
    std::vector<int> a2 = {1, 2, 3, 4, 5};
    assert(count_inversions(a2) == 0);

    // Test 3: Array with duplicate values
    std::vector<int> a3 = {2, 4, 1, 3, 2};
    assert(count_inversions(a3) == 4);
    assert(count_inversions(a3) == reference_count_inversions(a3));

    // Test 4: Single element and empty
    assert(count_inversions({42}) == 0);
    assert(count_inversions({}) == 0);

    std::cout << "All FENW-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
