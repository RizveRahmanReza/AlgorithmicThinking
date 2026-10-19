#include <iostream>
#include <vector>
#include <memory>
#include <cstdint>
#include <cassert>

namespace trie_0001 {

struct TrieNode {
    int next_hop; // -1 if non-terminal
    std::unique_ptr<TrieNode> child[2];

    TrieNode() : next_hop(-1) {
        child[0] = nullptr;
        child[1] = nullptr;
    }
};

class RoutingTrie {
private:
    std::unique_ptr<TrieNode> root;

public:
    RoutingTrie() : root(std::make_unique<TrieNode>()) {}

    // Inserts a CIDR prefix route: ip/prefix_len -> next_hop
    void insert_route(uint32_t ip, int prefix_len, int next_hop) {
        assert(prefix_len >= 0 && prefix_len <= 32);
        TrieNode* curr = root.get();

        for (int i = 0; i < prefix_len; ++i) {
            int bit = (ip >> (31 - i)) & 1;
            if (!curr->child[bit]) {
                curr->child[bit] = std::make_unique<TrieNode>();
            }
            curr = curr->child[bit].get();
        }
        curr->next_hop = next_hop;
    }

    // Returns the next_hop of the longest matching prefix for the given destination IP
    int lookup_lpm(uint32_t ip) const {
        const TrieNode* curr = root.get();
        int best_next_hop = curr->next_hop;

        for (int i = 0; i < 32; ++i) {
            int bit = (ip >> (31 - i)) & 1;
            if (!curr->child[bit]) {
                break;
            }
            curr = curr->child[bit].get();
            if (curr->next_hop != -1) {
                best_next_hop = curr->next_hop;
            }
        }
        return best_next_hop;
    }
};

uint32_t ip_to_int(uint8_t a, uint8_t b, uint8_t c, uint8_t d) {
    return (static_cast<uint32_t>(a) << 24) |
           (static_cast<uint32_t>(b) << 16) |
           (static_cast<uint32_t>(c) << 8)  |
           static_cast<uint32_t>(d);
}

} // namespace trie_0001

int main() {
    using namespace trie_0001;

    RoutingTrie trie;

    // Rules:
    // 0.0.0.0/0 -> NextHop 1 (Default fallback)
    // 192.168.0.0/16 -> NextHop 2
    // 192.168.1.0/24 -> NextHop 3
    // 192.168.1.100/32 -> NextHop 4 (Host route)
    // 10.0.0.0/8 -> NextHop 5

    trie.insert_route(ip_to_int(0, 0, 0, 0), 0, 1);
    trie.insert_route(ip_to_int(192, 168, 0, 0), 16, 2);
    trie.insert_route(ip_to_int(192, 168, 1, 0), 24, 3);
    trie.insert_route(ip_to_int(192, 168, 1, 100), 32, 4);
    trie.insert_route(ip_to_int(10, 0, 0, 0), 8, 5);

    // Test 1: Match host route
    assert(trie.lookup_lpm(ip_to_int(192, 168, 1, 100)) == 4);

    // Test 2: Match /24 subnet route
    assert(trie.lookup_lpm(ip_to_int(192, 168, 1, 55)) == 3);

    // Test 3: Match /16 subnet route
    assert(trie.lookup_lpm(ip_to_int(192, 168, 2, 1)) == 2);

    // Test 4: Match /8 subnet route
    assert(trie.lookup_lpm(ip_to_int(10, 20, 30, 40)) == 5);

    // Test 5: Fallback to default /0 route
    assert(trie.lookup_lpm(ip_to_int(8, 8, 8, 8)) == 1);

    std::cout << "All TRIE-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
