// Problem ID: MST-0001
// Title: Minimax Path and Dynamic Kruskal MST under Bottleneck Edge Weights
// Language: Standard ISO C++20
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>
#include <cassert>
#include <queue>

struct Edge {
    int u;
    int v;
    int64_t weight;
    int id;

    bool operator<(const Edge& other) const {
        return weight < other.weight;
    }
};

class DisjointSetUnion {
private:
    std::vector<int> parent;
    std::vector<int> rank;

public:
    explicit DisjointSetUnion(int n) : parent(n), rank(n, 0) {
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    int find(int i) {
        if (parent[i] == i)
            return i;
        return parent[i] = find(parent[i]);
    }

    bool unite(int i, int j) {
        int root_i = find(i);
        int root_j = find(j);
        if (root_i == root_j)
            return false;
        if (rank[root_i] < rank[root_j])
            std::swap(root_i, root_j);
        parent[root_j] = root_i;
        if (rank[root_i] == rank[root_j])
            rank[root_i]++;
        return true;
    }
};

class MinimaxMSTSolver {
private:
    int n;
    int log_n;
    int64_t total_mst_weight;
    std::vector<std::vector<std::pair<int, int64_t>>> adj;
    std::vector<std::vector<int>> up;
    std::vector<std::vector<int64_t>> max_w;
    std::vector<int> depth;

    void build_tree(int root) {
        depth.assign(n, -1);
        std::queue<int> q;
        depth[root] = 0;
        up[root][0] = root;
        max_w[root][0] = 0;
        q.push(root);

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (const auto& [v, w] : adj[u]) {
                if (depth[v] == -1) {
                    depth[v] = depth[u] + 1;
                    up[v][0] = u;
                    max_w[v][0] = w;
                    q.push(v);
                }
            }
        }

        for (int k = 1; k < log_n; ++k) {
            for (int u = 0; u < n; ++u) {
                int mid = up[u][k - 1];
                up[u][k] = up[mid][k - 1];
                max_w[u][k] = std::max(max_w[u][k - 1], max_w[mid][k - 1]);
            }
        }
    }

public:
    MinimaxMSTSolver(int n_val, std::vector<Edge>& edges) 
        : n(n_val), total_mst_weight(0) {
        log_n = 1;
        while ((1 << log_n) <= n) {
            log_n++;
        }
        log_n += 1;

        adj.resize(n);
        up.assign(n, std::vector<int>(log_n, 0));
        max_w.assign(n, std::vector<int64_t>(log_n, 0));

        std::sort(edges.begin(), edges.end());
        DisjointSetUnion dsu(n);
        int edges_added = 0;

        for (const auto& edge : edges) {
            if (dsu.unite(edge.u, edge.v)) {
                adj[edge.u].emplace_back(edge.v, edge.weight);
                adj[edge.v].emplace_back(edge.u, edge.weight);
                total_mst_weight += edge.weight;
                edges_added++;
                if (edges_added == n - 1)
                    break;
            }
        }

        build_tree(0);
    }

    int64_t get_total_mst_weight() const {
        return total_mst_weight;
    }

    int64_t query_minimax(int u, int v) const {
        if (u == v)
            return 0;

        int64_t ans = 0;
        if (depth[u] < depth[v])
            std::swap(u, v);

        for (int k = log_n - 1; k >= 0; --k) {
            if (depth[u] - (1 << k) >= depth[v]) {
                ans = std::max(ans, max_w[u][k]);
                u = up[u][k];
            }
        }

        if (u == v)
            return ans;

        for (int k = log_n - 1; k >= 0; --k) {
            if (up[u][k] != up[v][k]) {
                ans = std::max({ans, max_w[u][k], max_w[v][k]});
                u = up[u][k];
                v = up[v][k];
            }
        }

        ans = std::max({ans, max_w[u][0], max_w[v][0]});
        return ans;
    }

    bool query_edge_in_mst(int u, int v, int64_t w) const {
        return w <= query_minimax(u, v);
    }
};

// Standalone self-test harness
int main() {
    int n = 5;
    std::vector<Edge> edges = {
        {0, 1, 4, 0},
        {0, 2, 3, 1},
        {1, 2, 2, 2},
        {1, 3, 5, 3},
        {2, 3, 1, 4},
        {3, 4, 7, 5}
    };

    MinimaxMSTSolver solver(n, edges);
    assert(solver.get_total_mst_weight() == 13);
    assert(solver.query_minimax(0, 4) == 7);
    assert(solver.query_minimax(1, 3) == 2);
    assert(solver.query_minimax(0, 0) == 0);
    assert(solver.query_edge_in_mst(0, 4, 6) == true);
    assert(solver.query_edge_in_mst(0, 4, 8) == false);

    std::cout << "MST-0001 (C++20) assertions passed successfully.\n";
    return 0;
}
