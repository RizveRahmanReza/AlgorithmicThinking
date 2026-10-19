#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cassert>

namespace qry_0001 {

class SparseTable {
private:
    int n;
    int max_log;
    std::vector<int> log_table;
    std::vector<std::vector<int>> st;
    const std::vector<int>* raw_data;

    int min_index(int idx1, int idx2) const {
        return ((*raw_data)[idx1] <= (*raw_data)[idx2]) ? idx1 : idx2;
    }

public:
    explicit SparseTable(const std::vector<int>& arr)
        : n(static_cast<int>(arr.size())),
          raw_data(&arr) {
        if (n == 0) return;

        log_table.resize(n + 1, 0);
        for (int i = 2; i <= n; ++i) {
            log_table[i] = log_table[i / 2] + 1;
        }
        max_log = log_table[n] + 1;

        st.assign(max_log, std::vector<int>(n));
        for (int i = 0; i < n; ++i) {
            st[0][i] = i;
        }

        for (int k = 1; k < max_log; ++k) {
            int len = 1 << (k - 1);
            for (int i = 0; i + (1 << k) <= n; ++i) {
                st[k][i] = min_index(st[k - 1][i], st[k - 1][i + len]);
            }
        }
    }

    int query_min_index(int l, int r) const {
        assert(l <= r && l >= 0 && r < n);
        int len = r - l + 1;
        int k = log_table[len];
        return min_index(st[k][l], st[k][r - (1 << k) + 1]);
    }

    int query_min(int l, int r) const {
        return (*raw_data)[query_min_index(l, r)];
    }
};

} // namespace qry_0001

int main() {
    using namespace qry_0001;

    std::vector<int> arr = {31, 41, 59, 26, 53, 58, 97};
    SparseTable st(arr);

    assert(st.query_min(0, 6) == 26);
    assert(st.query_min_index(0, 6) == 3);

    assert(st.query_min(0, 2) == 31);
    assert(st.query_min(4, 6) == 53);
    assert(st.query_min(1, 5) == 26);

    // Single element
    assert(st.query_min(2, 2) == 59);

    std::cout << "All QRY-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
