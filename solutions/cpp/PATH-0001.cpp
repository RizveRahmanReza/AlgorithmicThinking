#include <iostream>
#include <vector>
#include <queue>
#include <tuple>
#include <cstdint>
#include <cassert>

namespace path_0001 {

constexpr int64_t INF = 1e18;

struct Edge {
    int to;
    int64_t weight;
};

struct State {
    int64_t dist;
    int u;
    int k;

    bool operator>(const State& other) const {
        return dist > other.dist;
    }
};

// Computes shortest path from s to t allowing up to K edges to be free (weight 0)
int64_t shortest_path_k_passes(int n, const std::vector<std::vector<Edge>>& adj, int s, int t, int k_max) {
    std::vector<std::vector<int64_t>> dist(n, std::vector<int64_t>(k_max + 1, INF));
    std::priority_queue<State, std::vector<State>, std::greater<State>> pq;

    dist[s][k_max] = 0;
    pq.push({0, s, k_max});

    while (!pq.empty()) {
        auto [d, u, k] = pq.top();
        pq.pop();

        if (d > dist[u][k]) continue;
        if (u == t) return d;

        for (const auto& edge : adj[u]) {
            int v = edge.to;
            int64_t w = edge.weight;

            // Option 1: Normal traversal
            if (dist[u][k] + w < dist[v][k]) {
                dist[v][k] = dist[u][k] + w;
                pq.push({dist[v][k], v, k});
            }

            // Option 2: Use free pass
            if (k > 0 && dist[u][k] < dist[v][k - 1]) {
                dist[v][k - 1] = dist[u][k];
                pq.push({dist[v][k - 1], v, k - 1});
            }
        }
    }

    int64_t ans = INF;
    for (int k = 0; k <= k_max; ++k) {
        ans = std::min(ans, dist[t][k]);
    }
    return (ans == INF) ? -1 : ans;
}

} // namespace path_0001

int main() {
    using namespace path_0001;

    // Test graph:
    // 0 -> 1 (w=10), 1 -> 2 (w=20)
    // 0 -> 2 (w=100)
    int n = 3;
    std::vector<std::vector<Edge>> adj(n);
    adj[0].push_back({1, 10});
    adj[1].push_back({2, 20});
    adj[0].push_back({2, 100});

    // Case 1: K = 0 (Normal path: 10 + 20 = 30)
    assert(shortest_path_k_passes(n, adj, 0, 2, 0) == 30);

    // Case 2: K = 1 (Discount edge 1->2: 10 + 0 = 10)
    assert(shortest_path_k_passes(n, adj, 0, 2, 1) == 10);

    // Case 3: K = 2 (Discount both edges: 0 + 0 = 0)
    assert(shortest_path_k_passes(n, adj, 0, 2, 2) == 0);

    // Case 4: Unreachable vertex
    int n2 = 4;
    std::vector<std::vector<Edge>> adj2(n2);
    adj2[0].push_back({1, 5});
    assert(shortest_path_k_passes(n2, adj2, 0, 3, 1) == -1);

    std::cout << "All PATH-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
