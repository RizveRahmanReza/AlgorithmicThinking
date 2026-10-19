#include <iostream>
#include <vector>
#include <cstdint>
#include <cassert>

namespace segt_0001 {

constexpr int64_t MOD = 1'000'000'007LL;

class AffineSegmentTree {
private:
    int n;
    std::vector<int64_t> tree_sum;
    std::vector<int64_t> lazy_mul;
    std::vector<int64_t> lazy_add;

    void apply_affine(int p, int l, int r, int64_t mul_val, int64_t add_val) {
        int64_t len = r - l + 1;
        tree_sum[p] = (tree_sum[p] * mul_val % MOD + add_val * len % MOD) % MOD;
        lazy_mul[p] = (lazy_mul[p] * mul_val) % MOD;
        lazy_add[p] = (lazy_add[p] * mul_val % MOD + add_val) % MOD;
    }

    void push_down(int p, int l, int r) {
        if (lazy_mul[p] == 1 && lazy_add[p] == 0) return;
        int mid = l + (r - l) / 2;
        apply_affine(2 * p, l, mid, lazy_mul[p], lazy_add[p]);
        apply_affine(2 * p + 1, mid + 1, r, lazy_mul[p], lazy_add[p]);
        lazy_mul[p] = 1;
        lazy_add[p] = 0;
    }

    void push_up(int p) {
        tree_sum[p] = (tree_sum[2 * p] + tree_sum[2 * p + 1]) % MOD;
    }

    void build(int p, int l, int r, const std::vector<int>& arr) {
        if (l == r) {
            tree_sum[p] = arr[l] % MOD;
            return;
        }
        int mid = l + (r - l) / 2;
        build(2 * p, l, mid, arr);
        build(2 * p + 1, mid + 1, r, arr);
        push_up(p);
    }

    void update_range(int p, int l, int r, int ql, int qr, int64_t mul_val, int64_t add_val) {
        if (ql <= l && r <= qr) {
            apply_affine(p, l, r, mul_val, add_val);
            return;
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        if (ql <= mid) update_range(2 * p, l, mid, ql, qr, mul_val, add_val);
        if (qr > mid) update_range(2 * p + 1, mid + 1, r, ql, qr, mul_val, add_val);
        push_up(p);
    }

    int64_t query_range(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) {
            return tree_sum[p];
        }
        push_down(p, l, r);
        int mid = l + (r - l) / 2;
        int64_t total = 0;
        if (ql <= mid) total = (total + query_range(2 * p, l, mid, ql, qr)) % MOD;
        if (qr > mid) total = (total + query_range(2 * p + 1, mid + 1, r, ql, qr)) % MOD;
        return total;
    }

public:
    explicit AffineSegmentTree(const std::vector<int>& arr)
        : n(static_cast<int>(arr.size())),
          tree_sum(4 * arr.size(), 0),
          lazy_mul(4 * arr.size(), 1),
          lazy_add(4 * arr.size(), 0) {
        if (n > 0) {
            build(1, 0, n - 1, arr);
        }
    }

    void range_add(int l, int r, int64_t val) {
        update_range(1, 0, n - 1, l, r, 1, val % MOD);
    }

    void range_multiply(int l, int r, int64_t val) {
        update_range(1, 0, n - 1, l, r, val % MOD, 0);
    }

    int64_t query_sum(int l, int r) {
        return query_range(1, 0, n - 1, l, r);
    }
};

} // namespace segt_0001

int main() {
    using namespace segt_0001;

    std::vector<int> arr = {1, 2, 3, 4, 5};
    AffineSegmentTree st(arr);

    // Initial sum: 1+2+3+4+5 = 15
    assert(st.query_sum(0, 4) == 15);
    assert(st.query_sum(1, 3) == 9);

    // Multiply [0..3] by 2 -> [2, 4, 6, 8, 5]
    st.range_multiply(0, 3, 2);
    assert(st.query_sum(0, 4) == 25);
    assert(st.query_sum(1, 3) == 18);

    // Add 3 to [2..4] -> [2, 4, 9, 11, 8]
    st.range_add(2, 4, 3);
    assert(st.query_sum(0, 4) == 34);
    assert(st.query_sum(2, 3) == 20);

    std::cout << "All SEGT-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
