#include <iostream>
#include <vector>
#include <queue>
#include <cassert>

namespace dag_0001 {

// Computes the lexicographically smallest topological sort of a DAG.
// Returns empty vector if the graph contains a directed cycle.
std::vector<int> lexicographical_toposort(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> in_deg(n, 0);
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            in_deg[v]++;
        }
    }

    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
    for (int i = 0; i < n; ++i) {
        if (in_deg[i] == 0) {
            pq.push(i);
        }
    }

    std::vector<int> topo_order;
    topo_order.reserve(n);

    while (!pq.empty()) {
        int u = pq.top();
        pq.pop();
        topo_order.push_back(u);

        for (int v : adj[u]) {
            in_deg[v]--;
            if (in_deg[v] == 0) {
                pq.push(v);
            }
        }
    }

    if (static_cast<int>(topo_order.size()) != n) {
        return {}; // Cycle detected
    }
    return topo_order;
}

void verify_toposort(int n, const std::vector<std::vector<int>>& adj, const std::vector<int>& order) {
    assert(static_cast<int>(order.size()) == n);
    std::vector<int> pos(n);
    for (int i = 0; i < n; ++i) {
        pos[order[i]] = i;
    }
    for (int u = 0; u < n; ++u) {
        for (int v : adj[u]) {
            assert(pos[u] < pos[v]);
        }
    }
}

} // namespace dag_0001

int main() {
    using namespace dag_0001;

    // Test 1: Diamond DAG with tie-breaking
    // 1 -> 0, 2 -> 0, 1 -> 3
    int n1 = 4;
    std::vector<std::vector<int>> adj1(n1);
    adj1[1].push_back(0);
    adj1[2].push_back(0);
    adj1[1].push_back(3);

    auto res1 = lexicographical_toposort(n1, adj1);
    assert(!res1.empty());
    // Lexicographically smallest must be: [1, 2, 0, 3]
    std::vector<int> expected1 = {1, 2, 0, 3};
    assert(res1 == expected1);
    verify_toposort(n1, adj1, res1);

    // Test 2: Graph with cycle
    int n2 = 3;
    std::vector<std::vector<int>> adj2(n2);
    adj2[0].push_back(1);
    adj2[1].push_back(2);
    adj2[2].push_back(0);

    auto res2 = lexicographical_toposort(n2, adj2);
    assert(res2.empty());

    // Test 3: Completely disconnected vertices
    int n3 = 3;
    std::vector<std::vector<int>> adj3(n3);
    auto res3 = lexicographical_toposort(n3, adj3);
    std::vector<int> expected3 = {0, 1, 2};
    assert(res3 == expected3);

    std::cout << "All DAG-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
