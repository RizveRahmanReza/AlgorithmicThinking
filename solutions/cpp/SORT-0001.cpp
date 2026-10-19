#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cassert>
#include <random>

namespace sort_0001 {

struct PartitionResult {
    int low;
    int high;
};

// In-place Dutch National Flag 3-way partitioning around a pivot value.
// Post-condition:
// [0, low - 1]     : elements < pivot
// [low, high]      : elements == pivot
// [high + 1, N - 1]: elements > pivot
PartitionResult three_way_partition(std::vector<int>& arr, int pivot) {
    int low = 0;
    int mid = 0;
    int high = static_cast<int>(arr.size()) - 1;

    while (mid <= high) {
        if (arr[mid] < pivot) {
            std::swap(arr[low], arr[mid]);
            low++;
            mid++;
        } else if (arr[mid] == pivot) {
            mid++;
        } else { // arr[mid] > pivot
            std::swap(arr[mid], arr[high]);
            high--;
            // Do not increment mid! arr[mid] has unexamined value from arr[high].
        }
    }
    return PartitionResult{low, high};
}

// Differential reference oracle
std::vector<int> reference_partition(const std::vector<int>& input, int pivot) {
    std::vector<int> lt, eq, gt;
    for (int x : input) {
        if (x < pivot) lt.push_back(x);
        else if (x == pivot) eq.push_back(x);
        else gt.push_back(x);
    }
    std::vector<int> res;
    res.insert(res.end(), lt.begin(), lt.end());
    res.insert(res.end(), eq.begin(), eq.end());
    res.insert(res.end(), gt.begin(), gt.end());
    return res;
}

void verify_invariants(const std::vector<int>& arr, int pivot, PartitionResult res) {
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < res.low; ++i) {
        assert(arr[i] < pivot);
    }
    for (int i = res.low; i <= res.high; ++i) {
        assert(arr[i] == pivot);
    }
    for (int i = res.high + 1; i < n; ++i) {
        assert(arr[i] > pivot);
    }
}

} // namespace sort_0001

int main() {
    using namespace sort_0001;

    // Test 1: Standard mixed array
    std::vector<int> a1 = {2, 0, 2, 1, 1, 0};
    auto r1 = three_way_partition(a1, 1);
    verify_invariants(a1, 1, r1);

    // Test 2: Empty array
    std::vector<int> a2 = {};
    auto r2 = three_way_partition(a2, 5);
    assert(r2.low == 0 && r2.high == -1);

    // Test 3: All identical equal to pivot
    std::vector<int> a3 = {7, 7, 7, 7, 7};
    auto r3 = three_way_partition(a3, 7);
    verify_invariants(a3, 7, r3);
    assert(r3.low == 0 && r3.high == 4);

    // Test 4: All less than pivot
    std::vector<int> a4 = {1, 2, 3, 2, 1};
    auto r4 = three_way_partition(a4, 10);
    verify_invariants(a4, 10, r4);
    assert(r4.low == 5 && r4.high == 4);

    // Test 5: All greater than pivot
    std::vector<int> a5 = {5, 8, 9, 6};
    auto r5 = three_way_partition(a5, 2);
    verify_invariants(a5, 2, r5);
    assert(r5.low == 0 && r5.high == -1);

    std::cout << "All SORT-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
