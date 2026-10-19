import pytest
from solutions.python.TREE_0001 import TreeNode, is_valid_bst, serialize_bst, deserialize_bst, inorder_traversal

def test_tree_0001_valid_bst():
    #        8
    #       / \
    #      3   10
    #     / \    \
    #    1   6    14
    root = TreeNode(8)
    root.left = TreeNode(3)
    root.right = TreeNode(10)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(6)
    root.right.right = TreeNode(14)

    assert is_valid_bst(root)

    serialized = serialize_bst(root)
    assert serialized == "8 3 1 6 10 14"

    reconstructed = deserialize_bst(serialized)
    assert is_valid_bst(reconstructed)
    assert serialize_bst(reconstructed) == serialized

    inorder = inorder_traversal(reconstructed)
    assert inorder == [1, 3, 6, 8, 10, 14]

def test_tree_0001_invalid_ancestor_violation():
    #        10
    #       /
    #      5
    #       \
    #        15  (15 > 10, invalid in left subtree of 10)
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.left.right = TreeNode(15)

    assert not is_valid_bst(root)

def test_tree_0001_empty_tree():
    assert is_valid_bst(None)
    assert serialize_bst(None) == ""
    assert deserialize_bst("") is None

def test_tree_0001_single_node():
    root = TreeNode(42)
    assert is_valid_bst(root)
    s = serialize_bst(root)
    assert s == "42"
    r = deserialize_bst(s)
    assert is_valid_bst(r)
    assert r.val == 42

def test_tree_0001_duplicate_keys():
    root = TreeNode(10)
    root.left = TreeNode(10)
    assert not is_valid_bst(root)
