#include <iostream>
#include <string>
#include <vector>
#include <string_view>
#include <array>
#include <cassert>
#include <climits>

namespace patt_0001 {

struct WindowResult {
    int start;
    int length;
};

// Finds the minimum window substring of S containing all characters of T.
// Returns WindowResult{start_index, length}. If none found, returns {-1, 0}.
WindowResult min_window(std::string_view s, std::string_view t) {
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(t.size());
    if (m == 0 || n < m) {
        return WindowResult{-1, 0};
    }

    std::array<int, 256> target_freq{};
    std::array<int, 256> window_freq{};

    for (unsigned char ch : t) {
        target_freq[ch]++;
    }

    int required_matches = m;
    int matched_count = 0;
    int left = 0;
    int best_start = -1;
    int best_len = INT_MAX;

    for (int right = 0; right < n; ++right) {
        unsigned char r_char = static_cast<unsigned char>(s[right]);
        
        if (target_freq[r_char] > 0) {
            if (window_freq[r_char] < target_freq[r_char]) {
                matched_count++;
            }
            window_freq[r_char]++;
        }

        while (matched_count == required_matches) {
            int current_len = right - left + 1;
            if (current_len < best_len) {
                best_len = current_len;
                best_start = left;
            }

            unsigned char l_char = static_cast<unsigned char>(s[left]);
            if (target_freq[l_char] > 0) {
                if (window_freq[l_char] == target_freq[l_char]) {
                    matched_count--;
                }
                window_freq[l_char]--;
            }
            left++;
        }
    }

    if (best_start == -1) {
        return WindowResult{-1, 0};
    }
    return WindowResult{best_start, best_len};
}

// Differential brute-force oracle for validation
std::string reference_min_window(std::string_view s, std::string_view t) {
    int n = static_cast<int>(s.size());
    int m = static_cast<int>(t.size());
    if (m == 0 || n < m) return "";

    std::array<int, 256> t_freq{};
    for (unsigned char ch : t) t_freq[ch]++;

    std::string best = "";
    int min_len = INT_MAX;

    for (int i = 0; i < n; ++i) {
        std::array<int, 256> cur_freq{};
        for (int j = i; j < n; ++j) {
            cur_freq[static_cast<unsigned char>(s[j])]++;
            bool valid = true;
            for (int k = 0; k < 256; ++k) {
                if (cur_freq[k] < t_freq[k]) {
                    valid = false;
                    break;
                }
            }
            if (valid) {
                int len = j - i + 1;
                if (len < min_len) {
                    min_len = len;
                    best = std::string(s.substr(i, len));
                }
                break;
            }
        }
    }
    return best;
}

} // namespace patt_0001

int main() {
    using namespace patt_0001;

    // Test 1: Standard case
    std::string s1 = "ADOBECODEBANC";
    std::string t1 = "ABC";
    auto res1 = min_window(s1, t1);
    assert(res1.start != -1);
    std::string win1 = s1.substr(res1.start, res1.length);
    assert(win1 == "BANC");
    assert(win1 == reference_min_window(s1, t1));

    // Test 2: Impossible match (M > N)
    std::string s2 = "A";
    std::string t2 = "AA";
    auto res2 = min_window(s2, t2);
    assert(res2.start == -1 && res2.length == 0);

    // Test 3: Exact match
    std::string s3 = "XYZ";
    std::string t3 = "XYZ";
    auto res3 = min_window(s3, t3);
    assert(res3.start == 0 && res3.length == 3);

    // Test 4: Pattern with duplicate characters
    std::string s4 = "AAABBC";
    std::string t4 = "AAB";
    auto res4 = min_window(s4, t4);
    assert(res4.start != -1);
    std::string win4 = s4.substr(res4.start, res4.length);
    assert(win4 == "AAB");

    std::cout << "All PATT-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
