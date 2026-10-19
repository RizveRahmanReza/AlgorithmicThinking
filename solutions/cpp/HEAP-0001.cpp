#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <stdexcept>
#include <random>

namespace heap_0001 {

class MinMaxHeap {
private:
    std::vector<int> h;

    static int parent(int i) { return (i - 1) / 2; }
    static int grandparent(int i) { return (i - 3) / 4; }

    static bool is_min_level(int i) {
        int level = 0;
        int idx = i + 1;
        while (idx > 1) {
            idx >>= 1;
            level++;
        }
        return (level % 2) == 0;
    }

    void sift_up_min(int i) {
        while (i >= 3) {
            int gp = grandparent(i);
            if (h[i] < h[gp]) {
                std::swap(h[i], h[gp]);
                i = gp;
            } else {
                break;
            }
        }
    }

    void sift_up_max(int i) {
        while (i >= 3) {
            int gp = grandparent(i);
            if (h[i] > h[gp]) {
                std::swap(h[i], h[gp]);
                i = gp;
            } else {
                break;
            }
        }
    }

    void sift_up(int i) {
        if (i == 0) return;
        int p = parent(i);
        if (is_min_level(i)) {
            if (h[i] > h[p]) {
                std::swap(h[i], h[p]);
                sift_up_max(p);
            } else {
                sift_up_min(i);
            }
        } else {
            if (h[i] < h[p]) {
                std::swap(h[i], h[p]);
                sift_up_min(p);
            } else {
                sift_up_max(i);
            }
        }
    }

    int find_min_child_or_grandchild(int i) {
        int best = 2 * i + 1;
        int n = static_cast<int>(h.size());
        for (int c = 1; c <= 2; ++c) {
            int child = 2 * i + c;
            if (child < n && h[child] < h[best]) best = child;
        }
        for (int gc = 3; gc <= 6; ++gc) {
            int gchild = 4 * i + gc;
            if (gchild < n && h[gchild] < h[best]) best = gchild;
        }
        return best;
    }

    int find_max_child_or_grandchild(int i) {
        int best = 2 * i + 1;
        int n = static_cast<int>(h.size());
        for (int c = 1; c <= 2; ++c) {
            int child = 2 * i + c;
            if (child < n && h[child] > h[best]) best = child;
        }
        for (int gc = 3; gc <= 6; ++gc) {
            int gchild = 4 * i + gc;
            if (gchild < n && h[gchild] > h[best]) best = gchild;
        }
        return best;
    }

    void sift_down_min(int i) {
        int n = static_cast<int>(h.size());
        if (2 * i + 1 >= n) return; // Leaf

        int m = find_min_child_or_grandchild(i);
        if (m >= 4 * i + 3) { // m is a grandchild
            if (h[m] < h[i]) {
                std::swap(h[m], h[i]);
                int p = parent(m);
                if (h[m] > h[p]) {
                    std::swap(h[m], h[p]);
                }
                sift_down_min(m);
            }
        } else { // m is a child
            if (h[m] < h[i]) {
                std::swap(h[m], h[i]);
            }
        }
    }

    void sift_down_max(int i) {
        int n = static_cast<int>(h.size());
        if (2 * i + 1 >= n) return; // Leaf

        int m = find_max_child_or_grandchild(i);
        if (m >= 4 * i + 3) { // m is a grandchild
            if (h[m] > h[i]) {
                std::swap(h[m], h[i]);
                int p = parent(m);
                if (h[m] < h[p]) {
                    std::swap(h[m], h[p]);
                }
                sift_down_max(m);
            }
        } else { // m is a child
            if (h[m] > h[i]) {
                std::swap(h[m], h[i]);
            }
        }
    }

    void sift_down(int i) {
        if (is_min_level(i)) {
            sift_down_min(i);
        } else {
            sift_down_max(i);
        }
    }

public:
    MinMaxHeap() = default;

    bool empty() const { return h.empty(); }
    size_t size() const { return h.size(); }

    void insert(int key) {
        h.push_back(key);
        sift_up(static_cast<int>(h.size()) - 1);
    }

    int get_min() const {
        if (h.empty()) throw std::underflow_error("Heap is empty");
        return h[0];
    }

    int get_max() const {
        if (h.empty()) throw std::underflow_error("Heap is empty");
        if (h.size() == 1) return h[0];
        if (h.size() == 2) return h[1];
        return std::max(h[1], h[2]);
    }

    int extract_min() {
        if (h.empty()) throw std::underflow_error("Heap is empty");
        int min_val = h[0];
        h[0] = h.back();
        h.pop_back();
        if (!h.empty()) sift_down(0);
        return min_val;
    }

    int extract_max() {
        if (h.empty()) throw std::underflow_error("Heap is empty");
        if (h.size() == 1) {
            int val = h[0];
            h.pop_back();
            return val;
        }
        int max_idx = 1;
        if (h.size() > 2 && h[2] > h[1]) max_idx = 2;

        int max_val = h[max_idx];
        h[max_idx] = h.back();
        h.pop_back();
        if (max_idx < static_cast<int>(h.size())) sift_down(max_idx);
        return max_val;
    }
};

} // namespace heap_0001

int main() {
    using namespace heap_0001;

    MinMaxHeap mmh;
    std::vector<int> vals = {30, 10, 50, 5, 80, 2, 90, 70};
    for (int v : vals) {
        mmh.insert(v);
    }

    assert(mmh.get_min() == 2);
    assert(mmh.get_max() == 90);

    assert(mmh.extract_min() == 2);
    assert(mmh.get_min() == 5);

    assert(mmh.extract_max() == 90);
    assert(mmh.get_max() == 80);

    assert(mmh.extract_min() == 5);
    assert(mmh.extract_max() == 80);

    std::cout << "All HEAP-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
