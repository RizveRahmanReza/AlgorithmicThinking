from typing import Optional, List
import math

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """Validates whether a binary tree is a strict BST using recursive bounds."""
    def helper(node: Optional[TreeNode], low: float, high: float) -> bool:
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return helper(node.left, low, node.val) and helper(node.right, node.val, high)

    return helper(root, -math.inf, math.inf)

def serialize_bst(root: Optional[TreeNode]) -> str:
    """Serializes a BST to a compact space-delimited pre-order string."""
    preorder: List[str] = []
    def dfs(node: Optional[TreeNode]) -> None:
        if not node:
            return
        preorder.append(str(node.val))
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return " ".join(preorder)

def deserialize_bst(data: str) -> Optional[TreeNode]:
    """Reconstructs the BST from pre-order tokens in strictly O(N) time."""
    if not data:
        return None
    tokens = [int(x) for x in data.split()]
    idx = 0

    def build(upper_bound: float) -> Optional[TreeNode]:
        nonlocal idx
        if idx >= len(tokens) or tokens[idx] >= upper_bound:
            return None
        val = tokens[idx]
        idx += 1
        node = TreeNode(val)
        node.left = build(val)
        node.right = build(upper_bound)
        return node

    return build(math.inf)

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Returns the in-order traversal of the tree."""
    res = []
    def dfs(node: Optional[TreeNode]):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res
