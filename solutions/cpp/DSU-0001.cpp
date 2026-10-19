#include <iostream>
#include <vector>
#include <numeric>
#include <utility>
#include <cassert>
#include <stdexcept>

namespace dsu_0001 {

struct OperationRecord {
    int child;
    int parent;
    int prev_parent_size;
    bool was_merged;
};

class RollbackDSU {
private:
    std::vector<int> parent;
    std::vector<int> sz;
    std::vector<OperationRecord> history;
    int num_components;

public:
    explicit RollbackDSU(int n) : parent(n), sz(n, 1), num_components(n) {
        std::iota(parent.begin(), parent.end(), 0);
    }

    // Read-only find without path compression: O(log N) worst case
    int find(int u) const {
        while (u != parent[u]) {
            u = parent[u];
        }
        return u;
    }

    bool connected(int u, int v) const {
        return find(u) == find(v);
    }

    int component_size(int u) const {
        return sz[find(u)];
    }

    int count_components() const {
        return num_components;
    }

    // Merges components using Union by Size: O(log N)
    bool unite(int u, int v) {
        int root_u = find(u);
        int root_v = find(v);

        if (root_u == root_v) {
            history.push_back({-1, -1, 0, false});
            return false;
        }

        // Union by size: attach smaller root under larger root
        if (sz[root_u] < sz[root_v]) {
            std::swap(root_u, root_v);
        }

        history.push_back({root_v, root_u, sz[root_u], true});

        parent[root_v] = root_u;
        sz[root_u] += sz[root_v];
        num_components--;
        return true;
    }

    // Rollback the single most recent unite: O(1)
    void rollback() {
        if (history.empty()) {
            throw std::underflow_error("History stack underflow during rollback");
        }

        OperationRecord rec = history.back();
        history.pop_back();

        if (!rec.was_merged) {
            return; // No-op union rolled back
        }

        parent[rec.child] = rec.child;
        sz[rec.parent] = rec.prev_parent_size;
        num_components++;
    }

    // Transaction snapshot checkpoint
    size_t checkpoint() const {
        return history.size();
    }

    // Rollback to a specific snapshot
    void rollback_to(size_t cp) {
        if (cp > history.size()) {
            throw std::invalid_argument("Invalid checkpoint ID");
        }
        while (history.size() > cp) {
            rollback();
        }
    }
};

} // namespace dsu_0001

int main() {
    using namespace dsu_0001;

    RollbackDSU dsu(6);
    assert(dsu.count_components() == 6);

    // Merge 0-1 and 2-3
    assert(dsu.unite(0, 1));
    assert(dsu.unite(2, 3));
    assert(dsu.count_components() == 4);
    assert(dsu.component_size(0) == 2);
    assert(dsu.component_size(2) == 2);

    size_t snap = dsu.checkpoint();

    // Speculatively unite 1 and 2
    assert(dsu.unite(1, 2));
    assert(dsu.connected(0, 3));
    assert(dsu.count_components() == 3);
    assert(dsu.component_size(0) == 4);

    // Rollback speculation
    dsu.rollback_to(snap);
    assert(!dsu.connected(0, 3));
    assert(dsu.count_components() == 4);
    assert(dsu.component_size(0) == 2);

    // Redundant union
    assert(!dsu.unite(0, 1)); // Already connected
    dsu.rollback(); // Rollback redundant union
    assert(dsu.connected(0, 1));

    std::cout << "All DSU-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
