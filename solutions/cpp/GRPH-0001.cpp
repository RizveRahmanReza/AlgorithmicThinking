#include <iostream>
#include <vector>
#include <queue>
#include <cassert>

namespace grph_0001 {

struct BipartiteResult {
    bool is_bipartite;
    std::vector<int> colors;
};

// Verifies if an undirected graph is bipartite and computes a valid 2-coloring
BipartiteResult check_bipartite(int n, const std::vector<std::vector<int>>& adj) {
    std::vector<int> color(n, -1);
    std::queue<int> q;

    for (int i = 0; i < n; ++i) {
        if (color[i] != -1) continue;

        color[i] = 0;
        q.push(i);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    q.push(v);
                } else if (color[v] == color[u]) {
                    // Odd cycle detected: adjacent vertices have identical color
                    return BipartiteResult{false, {}};
                }
            }
        }
    }

    return BipartiteResult{true, color};
}

void verify_coloring(int n, const std::vector<std::vector<int>>& adj, const std::vector<int>& color) {
    for (int u = 0; u < n; ++u) {
        assert(color[u] == 0 || color[u] == 1);
        for (int v : adj[u]) {
            assert(color[u] != color[v]);
        }
    }
}

} // namespace grph_0001

int main() {
    using namespace grph_0001;

    // Test 1: Even cycle (C4) - Bipartite
    int n1 = 4;
    std::vector<std::vector<int>> adj1(n1);
    adj1[0] = {1, 3};
    adj1[1] = {0, 2};
    adj1[2] = {1, 3};
    adj1[3] = {0, 2};

    auto res1 = check_bipartite(n1, adj1);
    assert(res1.is_bipartite);
    verify_coloring(n1, adj1, res1.colors);

    // Test 2: Odd cycle (C3 Triangle) - Not Bipartite
    int n2 = 3;
    std::vector<std::vector<int>> adj2(n2);
    adj2[0] = {1, 2};
    adj2[1] = {0, 2};
    adj2[2] = {0, 1};

    auto res2 = check_bipartite(n2, adj2);
    assert(!res2.is_bipartite);

    // Test 3: Disconnected graph with an isolated odd cycle in component 2
    int n3 = 6;
    std::vector<std::vector<int>> adj3(n3);
    // Comp 1: 0-1-2-3 (Path, bipartite)
    adj3[0] = {1};
    adj3[1] = {0, 2};
    adj3[2] = {1, 3};
    adj3[3] = {2};
    // Comp 2: 4-5 with self-conflict / triangle with self
    adj3[4] = {5};
    adj3[5] = {4, 5}; // Self-loop!

    auto res3 = check_bipartite(n3, adj3);
    assert(!res3.is_bipartite);

    std::cout << "All GRPH-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
