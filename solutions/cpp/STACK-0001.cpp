/**
 * STACK-0001: Valid Parentheses String Parsing and LIFO Invariants
 * Book: The Art of Algorithmic Thinking
 * 
 * Standard: ISO C++20
 * Complexity: O(N) Time, O(N) Auxiliary Space
 * Companion: Contains Quadratic Replacement Baseline Oracle
 */

#include <iostream>
#include <string_view>
#include <string>
#include <vector>
#include <cassert>

namespace alg {

/**
 * Validates bracket syntax using a LIFO stack invariant.
 * Complexity: O(N) Time, O(N) Auxiliary Space.
 * Conforms to ISO C++20 standard using std::string_view.
 */
bool is_valid_parentheses(std::string_view s) noexcept {
    // Parity optimization: odd length strings can never be balanced
    if (s.size() % 2 != 0) {
        return false;
    }

    // Vector used as flat cache-friendly contiguous stack
    std::vector<char> stack;
    stack.reserve(s.size() / 2); // Reserve expected average nesting depth

    for (char c : s) {
        switch (c) {
            case '(':
                stack.push_back(')');
                break;
            case '[':
                stack.push_back(']');
                break;
            case '{':
                stack.push_back('}');
                break;
            case ')':
            case ']':
            case '}':
                if (stack.empty() || stack.back() != c) {
                    return false;
                }
                stack.pop_back();
                break;
            default:
                // Treat unexpected characters as invalid per spec
                return false;
        }
    }

    return stack.empty();
}

} // namespace alg

// Differential Oracle (Repeated Substring Replacement)
bool is_valid_parentheses_oracle(std::string s) {
    if (s.size() % 2 != 0) return false;
    size_t prev_len = 0;
    while (s.size() != prev_len) {
        prev_len = s.size();
        auto pos = s.find("()");
        if (pos != std::string::npos) s.erase(pos, 2);
        pos = s.find("[]");
        if (pos != std::string::npos) s.erase(pos, 2);
        pos = s.find("{}");
        if (pos != std::string::npos) s.erase(pos, 2);
    }
    return s.empty();
}

int main() {
    std::string_view t1 = "()[]{}";
    assert(alg::is_valid_parentheses(t1) == true);
    assert(is_valid_parentheses_oracle(std::string(t1)) == true);

    std::string_view t2 = "([)]";
    assert(alg::is_valid_parentheses(t2) == false);
    assert(is_valid_parentheses_oracle(std::string(t2)) == false);

    std::string_view t3 = "{[]}";
    assert(alg::is_valid_parentheses(t3) == true);
    assert(is_valid_parentheses_oracle(std::string(t3)) == true);

    std::string_view t4 = "]";
    assert(alg::is_valid_parentheses(t4) == false);

    std::string_view t5 = "";
    assert(alg::is_valid_parentheses(t5) == true);

    std::cout << "All C++20 assertions for STACK-0001 passed successfully." << std::endl;
    return 0;
}
