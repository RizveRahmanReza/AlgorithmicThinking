/**
 * STR-0001: Valid Palindrome Invariant with Dual-Pointer In-Place Filtering
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(1) Auxiliary Space
 * Companion: Contains Allocation-Based Oracle for differential verification
 */

#include <iostream>
#include <string_view>
#include <string>
#include <cctype>
#include <cassert>

namespace alg {

/**
 * Checks if a character is ASCII alphanumeric without locale overhead.
 */
constexpr bool is_ascii_alphanumeric(char c) noexcept {
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
           (c >= '0' && c <= '9');
}

/**
 * Normalizes ASCII characters to lowercase in constant time.
 */
constexpr char to_ascii_lower(char c) noexcept {
    if (c >= 'A' && c <= 'Z') {
        return static_cast<char>(c + ('a' - 'A'));
    }
    return c;
}

/**
 * Determines whether a string is a valid palindrome, ignoring non-alphanumeric characters.
 * Complexity: O(N) Time, O(1) Auxiliary Space.
 * Conforms to ISO C++20 standard using std::string_view.
 */
bool is_valid_palindrome(std::string_view s) noexcept {
    if (s.empty()) {
        return true;
    }

    size_t left = 0;
    size_t right = s.size() - 1;

    while (left < right) {
        while (left < right && !is_ascii_alphanumeric(s[left])) {
            ++left;
        }
        while (left < right && !is_ascii_alphanumeric(s[right])) {
            --right;
        }

        if (left < right) {
            if (to_ascii_lower(s[left]) != to_ascii_lower(s[right])) {
                return false;
            }
            ++left;
            if (right == 0) break; // Underflow protection
            --right;
        }
    }

    return true;
}

} // namespace alg

// Differential Oracle (allocates intermediate filtered string)
bool is_valid_palindrome_oracle(std::string_view s) {
    std::string filtered;
    for (char c : s) {
        if (alg::is_ascii_alphanumeric(c)) {
            filtered += alg::to_ascii_lower(c);
        }
    }
    size_t n = filtered.size();
    for (size_t i = 0; i < n / 2; ++i) {
        if (filtered[i] != filtered[n - 1 - i]) {
            return false;
        }
    }
    return true;
}

int main() {
    std::string_view t1 = "A man, a plan, a canal: Panama";
    assert(alg::is_valid_palindrome(t1) == true);
    assert(is_valid_palindrome_oracle(t1) == true);

    std::string_view t2 = "race a car";
    assert(alg::is_valid_palindrome(t2) == false);
    assert(is_valid_palindrome_oracle(t2) == false);

    std::string_view t3 = " ";
    assert(alg::is_valid_palindrome(t3) == true);
    assert(is_valid_palindrome_oracle(t3) == true);

    std::string_view t4 = "0P";
    assert(alg::is_valid_palindrome(t4) == false);
    assert(is_valid_palindrome_oracle(t4) == false);

    std::cout << "All C++20 assertions for STR-0001 passed successfully." << std::endl;
    return 0;
}
