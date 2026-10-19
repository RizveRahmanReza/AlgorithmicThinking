from typing import List, Tuple
import heapq

INF = float('inf')

def shortest_path_k_passes(n: int, adj: List[List[Tuple[int, int]]], s: int, t: int, k_max: int) -> int:
    """
    Computes shortest path from s to t with at most k_max free edge passes.
    Runs in strictly O((N*K + M*K) log(N*K)) time.
    """
    dist = [[INF] * (k_max + 1) for _ in range(n)]
    dist[s][k_max] = 0

    pq = [(0, s, k_max)]

    while pq:
        d, u, k = heapq.heappop(pq)

        if d > dist[u][k]:
            continue
        if u == t:
            return d

        for v, w in adj[u]:
            # Option 1: Normal traversal
            if dist[u][k] + w < dist[v][k]:
                dist[v][k] = dist[u][k] + w
                heapq.heappush(pq, (dist[v][k], v, k))

            # Option 2: Use a free pass
            if k > 0 and dist[u][k] < dist[v][k - 1]:
                dist[v][k - 1] = dist[u][k]
                heapq.heappush(pq, (dist[v][k - 1], v, k - 1))

    ans = min(dist[t])
    return -1 if ans == INF else ans
