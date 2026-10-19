"""
STACK-0001: Valid Parentheses String Parsing and LIFO Invariants
Book: The Art of Algorithmic Thinking

Standard: Python 3.12+ (Type-Annotated, Idiomatic)
Contains Linear LIFO Stack Parser and Quadratic Replacement Baseline Oracle.
"""


def is_valid_parentheses(s: str) -> bool:
    """
    Validates bracket syntax using a LIFO stack invariant.
    Target: Python 3.12+ (O(N) Time, O(N) Auxiliary Space).
    """
    if len(s) % 2 != 0:
        return False

    stack: list[str] = []
    mapping = {'(': ')', '[': ']', '{': '}'}

    for char in s:
        if char in mapping:
            # Push expected closing bracket
            stack.append(mapping[char])
        elif not stack or stack.pop() != char:
            return False

    return len(stack) == 0


def is_valid_parentheses_oracle(s: str) -> bool:
    """Quadratic baseline oracle for differential testing."""
    if len(s) % 2 != 0:
        return False
    prev_len = -1
    while len(s) != prev_len:
        prev_len = len(s)
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return len(s) == 0


if __name__ == "__main__":
    t1 = "()[]{}"
    assert is_valid_parentheses(t1) is True
    assert is_valid_parentheses_oracle(t1) is True

    t2 = "([)]"
    assert is_valid_parentheses(t2) is False
    assert is_valid_parentheses_oracle(t2) is False

    t3 = "{[]}"
    assert is_valid_parentheses(t3) is True

    t4 = "]"
    assert is_valid_parentheses(t4) is False

    t5 = ""
    assert is_valid_parentheses(t5) is True

    print("All Python 3 self-tests for STACK-0001 passed successfully.")
