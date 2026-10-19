from typing import List
import heapq

def lexicographical_toposort(n: int, adj: List[List[int]]) -> List[int]:
    """
    Computes the lexicographically smallest topological sort of a DAG.
    Returns empty list if a cycle is detected.
    Runs in strictly O((N + M) log N) time and O(N + M) space.
    """
    in_deg = [0] * n
    for u in range(n):
        for v in adj[u]:
            in_deg[v] += 1

    pq: List[int] = [i for i in range(n) if in_deg[i] == 0]
    heapq.heapify(pq)

    topo_order: List[int] = []

    while pq:
        u = heapq.heappop(pq)
        topo_order.append(u)

        for v in adj[u]:
            in_deg[v] -= 1
            if in_deg[v] == 0:
                heapq.heappush(pq, v)

    if len(topo_order) != n:
        return []  # Cycle detected
    return topo_order
