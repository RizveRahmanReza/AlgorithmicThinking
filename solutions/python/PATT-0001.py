from collections import Counter

def min_window(s: str, t: str) -> str:
    """
    Finds the shortest substring of S containing all characters of T.
    Runs in strictly O(N + M) time and O(|Sigma|) space.
    """
    n, m = len(s), len(t)
    if m == 0 or n < m:
        return ""

    target_freq = Counter(t)
    window_freq = Counter()

    required_matches = m
    matched_count = 0
    left = 0
    best_start = -1
    best_len = float('inf')

    for right in range(n):
        r_char = s[right]
        if r_char in target_freq:
            if window_freq[r_char] < target_freq[r_char]:
                matched_count += 1
            window_freq[r_char] += 1

        while matched_count == required_matches:
            current_len = right - left + 1
            if current_len < best_len:
                best_len = current_len
                best_start = left

            l_char = s[left]
            if l_char in target_freq:
                if window_freq[l_char] == target_freq[l_char]:
                    matched_count -= 1
                window_freq[l_char] -= 1
            left += 1

    if best_start == -1:
        return ""
    return s[best_start : best_start + int(best_len)]

def reference_min_window(s: str, t: str) -> str:
    """Quadratic brute-force differential oracle."""
    n, m = len(s), len(t)
    if m == 0 or n < m:
        return ""
    target_freq = Counter(t)
    best = ""
    min_len = float('inf')

    for i in range(n):
        cur = Counter()
        for j in range(i, n):
            cur[s[j]] += 1
            if all(cur[k] >= target_freq[k] for k in target_freq):
                length = j - i + 1
                if length < min_len:
                    min_len = length
                    best = s[i : j + 1]
                break
    return best
