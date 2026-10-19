from typing import List, Tuple
from collections import deque

def check_bipartite(n: int, adj: List[List[int]]) -> Tuple[bool, List[int]]:
    """
    Checks if an undirected graph is bipartite using BFS 2-coloring.
    Returns (is_bipartite, colors) where colors[u] in {0, 1}.
    Runs in strictly O(N + M) time and O(N) space.
    """
    color = [-1] * n
    q = deque()

    for i in range(n):
        if color[i] != -1:
            continue

        color[i] = 0
        q.append(i)

        while q:
            u = q.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    return False, []

    return True, color
