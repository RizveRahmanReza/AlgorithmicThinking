import pytest
from solutions.python.PATT_0001 import min_window, reference_min_window

def test_patt_0001_standard():
    s = "ADOBECODEBANC"
    t = "ABC"
    assert min_window(s, t) == "BANC"
    assert min_window(s, t) == reference_min_window(s, t)

def test_patt_0001_single_char():
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""

def test_patt_0001_exact_match():
    assert min_window("xyz", "xyz") == "xyz"

def test_patt_0001_duplicates_in_target():
    s = "AAABBC"
    t = "AAB"
    assert min_window(s, t) == "AAB"
    assert min_window(s, t) == reference_min_window(s, t)

def test_patt_0001_no_match():
    assert min_window("abcdef", "xyz") == ""

def test_patt_0001_differential_fuzz():
    import random
    rng = random.Random(42)
    alphabet = "abcde"
    for _ in range(40):
        n = rng.randint(1, 40)
        m = rng.randint(1, 10)
        s = "".join(rng.choice(alphabet) for _ in range(n))
        t = "".join(rng.choice(alphabet) for _ in range(m))
        expected = reference_min_window(s, t)
        actual = min_window(s, t)
        assert len(actual) == len(expected)
