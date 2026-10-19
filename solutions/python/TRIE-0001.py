from typing import Optional, List

class TrieNode:
    def __init__(self):
        self.next_hop: int = -1
        self.child: List[Optional['TrieNode']] = [None, None]

class RoutingTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert_route(self, ip: int, prefix_len: int, next_hop: int) -> None:
        """Inserts an IPv4 routing prefix into the bitwise trie."""
        curr = self.root
        for i in range(prefix_len):
            bit = (ip >> (31 - i)) & 1
            if curr.child[bit] is None:
                curr.child[bit] = TrieNode()
            curr = curr.child[bit]
        curr.next_hop = next_hop

    def lookup_lpm(self, ip: int) -> int:
        """Performs Longest Prefix Match lookup for a 32-bit IP address."""
        curr = self.root
        best_next_hop = curr.next_hop

        for i in range(32):
            bit = (ip >> (31 - i)) & 1
            if curr.child[bit] is None:
                break
            curr = curr.child[bit]
            if curr.next_hop != -1:
                best_next_hop = curr.next_hop

        return best_next_hop

def ip_to_int(a: int, b: int, c: int, d: int) -> int:
    return (a << 24) | (b << 16) | (c << 8) | d
