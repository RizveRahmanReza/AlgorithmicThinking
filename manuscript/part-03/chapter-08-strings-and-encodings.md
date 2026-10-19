# CHAPTER 8: STRINGS, ENCODINGS, AND IN-PLACE SEQUENCE MANIPULATION

> *"A string is not merely an array of characters. It is an encoded linguistic stream where byte length, code point count, and grapheme cluster boundaries diverge."*

---

## 8.1 The Anatomy of Text: ASCII, Unicode, Code Points, and UTF-8

To an algorithmic theorist, a string is a sequence drawn from an alphabet $\Sigma$: $S \in \Sigma^*$. 
To a software systems engineer, text is a serialized sequence of physical bytes subject to encoding standards. Conflating these two perspectives is one of the most prolific sources of security vulnerabilities, buffer overflows, and performance bugs in modern software.

### The Evolution of Character Representations

```
+--------------------------------------------------------------------------------+
| Standard | Character Domain | Storage Width | Key Architectural Property       |
+--------------------------------------------------------------------------------+
| ASCII    | 128 characters   | 7 bits (1 byte)| 1 Byte = 1 Character (Trivial)  |
| Latin-1  | 256 characters   | 8 bits (1 byte)| Extended European alphabets      |
| UCS-2    | 65,536 characters| 16 bits (fixed)| Obsolete; failed global scripts |
| UTF-32   | 1,114,112 code pt| 32 bits (fixed)| O(1) indexing; extreme bloat    |
| UTF-8    | 1,114,112 code pt| 1 - 4 bytes    | Variable-length; ASCII backwards|
+--------------------------------------------------------------------------------+
```

### The Three Layers of Unicode
When working with modern text, an engineer must distinguish three entirely different concepts of "length":

1. **Byte Length**: The number of 8-bit bytes occupied in physical memory.
2. **Code Point Count (Scalar Values)**: The number of individual Unicode numerical identifiers (written `U+XXXX`).
3. **Grapheme Clusters (User-Perceived Characters)**: What a human reader sees as a single visual character (which may combine a base letter with multiple accent marks, skin-tone modifiers, or zero-width joiners).

*Example*: The family emoji `👨‍👩‍👧‍👦` is:
- **1 Grapheme Cluster** (visually rendered as one family glyph).
- **7 Unicode Code Points** (`Man` + `ZWJ` + `Woman` + `ZWJ` + `Girl` + `ZWJ` + `Boy`).
- **25 Bytes** in UTF-8 encoding!

```
Physical Bytes (UTF-8): [ F0 9F 91 A8 E2 80 8D ... ]  (25 bytes)
                                  |
Unicode Code Points:    [ U+1F468 | U+200D | U+1F469 | ... ] (7 points)
                                  |
User Grapheme Cluster:  [ 👨‍👩‍👧‍👦 ]                         (1 visual glyph)
```

### The Inherent Pitfall of String Indexing
In languages like Python, `len("hello")` returns code points, while in C++, `std::string::size()` returns the number of physical bytes (`char`).
In UTF-8, **random access by character index is $\mathcal{O}(N)$, not $\mathcal{O}(1)$**, because one must parse variable-length byte headers (e.g., leading `110xxxxx` indicates a 2-byte sequence; `1110xxxx` indicates 3 bytes; `11110xxx` indicates 4 bytes).

When designing high-performance string algorithms, we must explicitly distinguish **byte-level operations** (ASCII / sanitized alphanumeric tokens) from **linguistic grapheme operations**.

---

## 8.2 In-Place Buffer Transformations and Space Invariants

When manipulating long text streams in memory (e.g., lexical analyzers, URL decoders, markdown parsers), creating intermediate string allocations triggers frequent heap allocations, memory fragmentation, and garbage collection pressure.

A fundamental algorithmic pattern for zero-allocation text manipulation is the **Two-Pointer Read/Write Filter**:
- A **Read Pointer ($R$)** scans forward through the input buffer, inspecting incoming characters.
- A **Write Pointer ($W \le R$)** writes valid, normalized, or filtered characters back into the *same* buffer.

Because $W \le R$ at all times, the write pointer never overwrites unprocessed input data, guaranteeing safety without allocating a single additional byte of memory ($\mathcal{O}(1)$ auxiliary space).

---

## 8.3 Worked Problem: STR-0001 — Valid Palindrome Invariant with Dual-Pointer In-Place Filtering

We now apply the **Mandatory 20-Step Problem Solving Sequence** to analyze, prove, implement, and verify a foundational string problem: **In-Place Palindromic Verification under Non-Alphanumeric Filtering**.

---

### Step 1: Real-World Motivation
In search engines, genomics search buffers, and natural language processing (NLP) tokenizers, strings must be normalized and verified for symmetry. Palindromic sequences appear in DNA restriction enzyme recognition sites, cryptographic hash verification, and linguistic compression. 

In low-latency API gateways, validating whether an incoming payload is symmetric under normalization (ignoring whitespace, punctuation, and case sensitivity) must execute in a single streaming pass without allocating secondary strings on the heap.

### Step 2: Problem Identification
Given a string of characters, determine whether it is a **palindrome**, considering only alphanumeric characters and ignoring letter casing, executing in strictly $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ auxiliary space.

### Step 3: Formal Problem Statement
Let $S = [s_0, s_1, \dots, s_{n-1}]$ be a string of length $n$ consisting of printable ASCII characters.
Define the normalization function $f(c)$:
$$f(c) = \begin{cases} \text{tolower}(c) & \text{if } c \text{ is ASCII alphanumeric ('A'-'Z', 'a'-'z', '0'-'9')} \\ \epsilon & \text{otherwise (empty / ignored)} \end{cases}$$

Let $S_{\text{norm}} = f(s_0) \circ f(s_1) \circ \dots \circ f(s_{n-1})$ be the concatenated normalized sequence of length $m \le n$.
The string $S$ is a **Valid Palindrome** if and only if $S_{\text{norm}}$ is symmetric under reversal:
$$\forall k \in [0, \lfloor m / 2 \rfloor], \quad S_{\text{norm}}[k] = S_{\text{norm}}[m - 1 - k]$$

#### Constraints:
- Length: $0 \le n \le 10^7$
- Characters: Standard ASCII printable characters (codes 32 to 126).
- Time budget: Strictly $\mathcal{O}(n)$
- Auxiliary memory budget: Strictly $\mathcal{O}(1)$ (Zero dynamic allocations; no intermediate string copies).

### Step 4: Thinking Before Coding
1. **The Allocation Trap**: A naive approach creates a new string `filtered = [c.lower() for c in s if c.isalnum()]` and compares `filtered == filtered[::-1]`. 
   *Why this fails systems standards*: If $N = 10^7$, creating `filtered` allocates $10 \text{ MB}$ of memory, and `filtered[::-1]` allocates another $10 \text{ MB}$. This induces cache thrashing and memory allocator lock contention.
2. **The Dual Inward Pointer Invariant**: Can we verify symmetry *without creating the filtered string at all*?
   Yes! Place pointer $L$ at index $0$ and pointer $R$ at index $n-1$. Advance $L$ until it points to an alphanumeric character; decrement $R$ until it points to an alphanumeric character. Compare the two normalized characters. If they match, advance both. If they differ, terminate with `False` immediately.
3. **Empty / Non-Alphanumeric Input**: A string containing no alphanumeric characters (e.g., `", , ;"` or `""`) normalizes to an empty sequence $\epsilon$. By definition, an empty sequence is symmetrically identical to its reversal, so it must evaluate to `True`.

### Step 5: First-Principles Reasoning & Oracles
A string is symmetric if and only if every pair of characters equidistant from the normalized boundaries are identical. 
By searching from both outer boundaries inwards simultaneously:
- Any character that is not alphanumeric has zero impact on the validity of the palindrome and can be skipped immediately.
- The first discrepancy found between $L$ and $R$ immediately disproves symmetry, allowing **early termination** without inspecting the rest of the string.

### Step 6: Brute-Force Implementation (The Allocation Oracle)

```python
# Reference Baseline: Allocates normalized intermediate copy
def is_palindrome_oracle(s: str) -> bool:
    filtered = [ch.lower() for ch in s if ch.isalnum()]
    return filtered == filtered[::-1]
```

### Step 7: Bottleneck Analysis
- The baseline oracle requires $\Theta(n)$ auxiliary memory to store `filtered` and another $\Theta(n)$ memory for `filtered[::-1]`.
- For $n = 10^7$, this triggers two large heap allocations ($\approx 20 \text{ MB}$) and iterates over the data three separate times (filtering pass, reversal pass, comparison pass).
- The inward two-pointer approach eliminates all memory allocations and terminates in at most $n/2$ comparisons, processing the string in a single streaming pass.

### Step 8: Candidate Solution Comparison

| Strategy | Time Complexity | Auxiliary Space | Passes Over Data | Allocation Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Filtered Copy & Reverse** | $\Theta(n)$ | $\Theta(n)$ | 3 passes | High (Multiple dynamic string copies) |
| **In-Place Write Filter First** | $\Theta(n)$ | $\mathcal{O}(1)$ | 2 passes | Mutates original string in place |
| **Dual-Pointer Inward Scan** | $\mathcal{O}(n)$ | $\mathcal{O}(1)$ | **1 pass (Early exit)** | **Zero allocation; read-only** |

### Step 9: Derivation of the Dual-Pointer Inward Algorithm
1. Initialize $L = 0$ and $R = n - 1$.
2. While $L < R$:
   - While $L < R$ and $S[L]$ is not alphanumeric: increment $L$.
   - While $L < R$ and $S[R]$ is not alphanumeric: decrement $R$.
   - Normalize: $c_L = \text{tolower}(S[L])$, $c_R = \text{tolower}(S[R])$.
   - If $c_L \ne c_R$: return `False` immediately.
   - Increment $L$; decrement $R$.
3. If $L \ge R$: return `True`.

### Step 10: Correctness Proof via Invariant

#### Loop Invariant:
At the start of each step of the outer `while (L < R)` loop:
> **Invariant**: All valid alphanumeric characters in the prefix $S[0 \dots L-1]$ have been verified to match symmetrically with the corresponding alphanumeric characters in the suffix $S[R+1 \dots n-1]$.

#### Base Case (Initialization):
Before the loop begins, $L = 0$ and $R = n-1$. The checked prefix is empty, and the checked suffix is empty. The invariant holds vacuously.

#### Maintenance (Inductive Step):
Assume the invariant holds for boundaries $L$ and $R$.
1. The inner loops skip non-alphanumeric characters. Since non-alphanumeric characters are mapped to $\epsilon$ under $f$, skipping them preserves the sequence of valid normalized elements.
2. If $L < R$, $S[L]$ is the next leftmost normalized character, and $S[R]$ is the next rightmost normalized character.
3. If $\text{tolower}(S[L]) \ne \text{tolower}(S[R])$, a discrepancy exists at equidistant positions; the string cannot be a palindrome, and returning `False` is correct.
4. If $\text{tolower}(S[L]) == \text{tolower}(S[R])$, the matched pair is added to the verified set. Incrementing $L$ and decrementing $R$ preserves the invariant for the next iteration.

#### Termination:
The loop terminates either on character mismatch (correctly returning `False`) or when $L \ge R$.
If $L \ge R$, all alphanumeric characters in the string have been paired and verified. No unpaired characters remain except possibly a single center character (when $L = R$), which is trivially symmetric with itself. Returning `True` is unconditionally correct. $\blacksquare$

### Step 11: Step-by-Step Dry Run
Input: `S = "A man, a plan, a canal: Panama"`

```
Initial Pointers:
[ A  _  m  a  n  ,  _  a  _  p  l  a  n  ,  _  a  _  c  a  n  a  l  :  _  P  a  n  a  m  a ]
  ^                                                                                        ^
  L                                                                                        R
```

| Step | $L$ char | $R$ char | Action | Matches? | New $L, R$ |
| :---: | :---: | :---: | :--- | :---: | :---: |
| 1 | `'A'` | `'a'` | Compare: `'a' == 'a'` | Yes | $L \to 1, R \to 28$ |
| 2 | `' '` (skip) | `'m'` | Skip space: $L \to 2$ (`'m'`) | — | $L \to 2, R \to 28$ |
| 3 | `'m'` | `'m'` | Compare: `'m' == 'm'` | Yes | $L \to 3, R \to 27$ |
| 4 | `'a'` | `'a'` | Compare: `'a' == 'a'` | Yes | $L \to 4, R \to 26$ |
| 5 | `'n'` | `'n'` | Compare: `'n' == 'n'` | Yes | $L \to 5, R \to 25$ |
| 6 | `','` (skip) | `'a'` | Skip comma, space: $L \to 7$ (`'a'`) | — | $L \to 7, R \to 25$ |
| 7 | `'a'` | `'a'` | Compare: `'a' == 'a'` | Yes | $L \to 8, R \to 24$ |
| ... | ... | ... | Pointers stride inwards until meeting at center `'p'`. | Yes | $L \ge R$ |

**Final Result**: `True` (Valid Palindrome verified in 15 comparisons with zero allocations).

### Step 12: Full C++20 Implementation

```cpp
// solutions/cpp/STR-0001.cpp
#include <iostream>
#include <string_view>
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
            if (right == 0) break; // Underflow guard
            --right;
        }
    }

    return true;
}

} // namespace alg

// Differential Oracle
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
```

### Step 13: Full Python Implementation

```python
# solutions/python/STR-0001.py
from typing import Sequence


def is_valid_palindrome(s: str) -> bool:
    """
    Validates if string is a palindrome considering only alphanumeric characters.
    Target: Python 3.12+ (O(N) Time, O(1) Auxiliary Space).
    """
    left: int = 0
    right: int = len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if left < right:
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1

    return True


def is_valid_palindrome_oracle(s: str) -> bool:
    """Allocation-based baseline oracle for differential testing."""
    filtered = [ch.lower() for ch in s if ch.isalnum()]
    return filtered == filtered[::-1]


if __name__ == "__main__":
    t1 = "A man, a plan, a canal: Panama"
    assert is_valid_palindrome(t1) is True
    assert is_valid_palindrome_oracle(t1) is True

    t2 = "race a car"
    assert is_valid_palindrome(t2) is False
    assert is_valid_palindrome_oracle(t2) is False

    t3 = " , , ; "
    assert is_valid_palindrome(t3) is True

    t4 = "0P"
    assert is_valid_palindrome(t4) is False

    print("All Python 3 self-tests for STR-0001 passed successfully.")
```

### Step 14: Complexity Analysis
- **Time Complexity**: $\mathcal{O}(n)$
  - Pointers $L$ and $R$ start at opposite ends and move toward each other.
  - In each step of the inner or outer loops, either $L$ increases or $R$ decreases.
  - No character is visited more than twice. Total operations $\le 2n \implies \mathcal{O}(n)$.
  - **Early Exit**: If the first and last characters mismatch, the algorithm terminates in $\mathcal{O}(1)$ time.
- **Space Complexity**: $\Theta(1)$ auxiliary space
  - The C++ implementation takes `std::string_view` (non-owning pointer + length; 16 bytes).
  - Memory consumption is strictly limited to two integer indices. Zero heap allocations.

### Step 15: Edge Cases and Failure Modes
- **All Non-Alphanumeric**: `", , ;"` $\to$ Loop terminates with $L \ge R$, returning `True`.
- **Single Character**: `"a"` $\to$ Returns `True`.
- **Digits vs. Letters**: `"0P"` $\to$ Digits must not match letters (`'0'` $\ne$ `'p'`).
- **Underflow on `size_t`**: In C++, decrementing `right` when `right == 0` causes underflow to `SIZE_MAX`. Our underflow guard (`if (right == 0) break;`) prevents out-of-bounds memory access.

### Step 16: Test Cases & Validation Suite
- Standard palindromes with mixed punctuation.
- Asymmetric strings with early mismatches.
- Numeric palindromes (`"12321"`).
- Empty and whitespace-only strings.

### Step 17: Real-World Engineering Application
- Network API firewall query sanitization.
- Fast lexicographical validation in search query compilers.
- Bioinformatic DNA restriction enzyme palindromic cleavage site detection.

### Step 18: Further Optimization
- In systems processing millions of small strings, skipping locale-dependent `std::isalnum` in favor of bitwise lookup tables (`lookup_table[static_cast<uint8_t>(c)] & ALNUM_FLAG`) eliminates branching entirely.

### Step 19: Related Patterns
- **Palindrome Pairs**: Finding pairs of words that concatenate into a palindrome using a Trie.
- **Longest Palindromic Substring**: Expanding around centers or using Manacher's Algorithm ($\mathcal{O}(N)$).

### Step 20: Reader Challenges
1. **Challenge 8.1 (Valid Palindrome II)**: Determine whether a string can become a palindrome after deleting *at most one* character. Derive an $\mathcal{O}(N)$ time and $\mathcal{O}(1)$ space solution.
2. **Challenge 8.2 (In-Place String Compression)**: Given an array of characters, compress it in-place such that groups of consecutive identical characters are replaced by the character followed by the group count. Prove the read/write pointer invariant $W \le R$.

---

## 8.4 Chapter Synthesis
Strings are not abstract arrays; they are encoded byte streams with physical representation trade-offs. By replacing allocation-heavy string operations with dual-pointer in-place streaming invariants, you achieve order-of-magnitude performance gains and eliminate memory pressure.

In **Chapter 9**, we explore **Pointer-Based Structures and Linked Lists**, investigating node allocations, pointer indirection, cycle detection, and in-place list reversals.
