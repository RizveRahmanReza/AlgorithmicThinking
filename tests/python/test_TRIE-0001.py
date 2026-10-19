import pytest
from solutions.python.TRIE_0001 import RoutingTrie, ip_to_int

def test_trie_0001_routing():
    trie = RoutingTrie()

    trie.insert_route(ip_to_int(0, 0, 0, 0), 0, 1)
    trie.insert_route(ip_to_int(192, 168, 0, 0), 16, 2)
    trie.insert_route(ip_to_int(192, 168, 1, 0), 24, 3)
    trie.insert_route(ip_to_int(192, 168, 1, 100), 32, 4)
    trie.insert_route(ip_to_int(10, 0, 0, 0), 8, 5)

    # 1. Exact host route
    assert trie.lookup_lpm(ip_to_int(192, 168, 1, 100)) == 4

    # 2. Subnet /24
    assert trie.lookup_lpm(ip_to_int(192, 168, 1, 55)) == 3

    # 3. Subnet /16
    assert trie.lookup_lpm(ip_to_int(192, 168, 2, 1)) == 2

    # 4. Subnet /8
    assert trie.lookup_lpm(ip_to_int(10, 20, 30, 40)) == 5

    # 5. Default fallback
    assert trie.lookup_lpm(ip_to_int(8, 8, 8, 8)) == 1

def test_trie_0001_no_match():
    trie = RoutingTrie()
    trie.insert_route(ip_to_int(192, 168, 0, 0), 16, 10)
    # Different subnet, no default route
    assert trie.lookup_lpm(ip_to_int(10, 0, 0, 1)) == -1
