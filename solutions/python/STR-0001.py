"""
STR-0001: Valid Palindrome Invariant with Dual-Pointer In-Place Filtering
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Dual-Pointer Inward Algorithm and Allocation Baseline Oracle.
"""


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
