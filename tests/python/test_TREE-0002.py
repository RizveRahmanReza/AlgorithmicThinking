import pytest
import math
from solutions.python.TREE_0002 import AVLTree

def test_tree_0002_sequential_insertion():
    tree = AVLTree()
    for i in range(1, 101):
        tree.insert(i)
        assert tree.is_balanced()

    # Height for 100 keys must be strictly <= 1.44 * log2(102) ~ 9.6
    assert tree.height() <= 9

    for i in range(1, 101):
        assert tree.contains(i)
    assert not tree.contains(101)

def test_tree_0002_deletion_rebalancing():
    tree = AVLTree()
    keys = [20, 10, 30, 5, 15, 25, 35, 3, 7]
    for k in keys:
        tree.insert(k)
        assert tree.is_balanced()

    for k in keys:
        assert tree.contains(k)

    # Delete leaves and internal nodes
    to_delete = [3, 20, 30]
    for k in to_delete:
        tree.remove(k)
        assert tree.is_balanced()
        assert not tree.contains(k)

    # Remaining keys intact
    for k in [10, 5, 15, 25, 35, 7]:
        assert tree.contains(k)

def test_tree_0002_random_fuzz():
    import random
    rng = random.Random(42)
    tree = AVLTree()
    active_keys = set()

    for _ in range(300):
        action = rng.choice(["insert", "insert", "remove"])
        val = rng.randint(1, 100)
        if action == "insert":
            tree.insert(val)
            active_keys.add(val)
        else:
            tree.remove(val)
            active_keys.discard(val)

        assert tree.is_balanced()

    for k in range(1, 101):
        assert tree.contains(k) == (k in active_keys)
