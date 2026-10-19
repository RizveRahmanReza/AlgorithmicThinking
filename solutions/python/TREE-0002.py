from typing import Optional

class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.height: int = 0
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None

class AVLTree:
    def __init__(self):
        self.root: Optional[AVLNode] = None

    @staticmethod
    def _get_height(node: Optional[AVLNode]) -> int:
        return node.height if node else -1

    @staticmethod
    def _get_balance(node: Optional[AVLNode]) -> int:
        return AVLTree._get_height(node.left) - AVLTree._get_height(node.right) if node else 0

    @staticmethod
    def _update_height(node: AVLNode) -> None:
        node.height = 1 + max(AVLTree._get_height(node.left), AVLTree._get_height(node.right))

    @staticmethod
    def _rotate_right(y: AVLNode) -> AVLNode:
        x = y.left
        assert x is not None
        t2 = x.right

        x.right = y
        y.left = t2

        AVLTree._update_height(y)
        AVLTree._update_height(x)
        return x

    @staticmethod
    def _rotate_left(x: AVLNode) -> AVLNode:
        y = x.right
        assert y is not None
        t2 = y.left

        y.left = x
        x.right = t2

        AVLTree._update_height(x)
        AVLTree._update_height(y)
        return y

    @staticmethod
    def _rebalance(node: AVLNode) -> AVLNode:
        AVLTree._update_height(node)
        balance = AVLTree._get_balance(node)

        # Left-Heavy
        if balance > 1:
            assert node.left is not None
            if AVLTree._get_balance(node.left) < 0:
                node.left = AVLTree._rotate_left(node.left)
            return AVLTree._rotate_right(node)

        # Right-Heavy
        if balance < -1:
            assert node.right is not None
            if AVLTree._get_balance(node.right) > 0:
                node.right = AVLTree._rotate_right(node.right)
            return AVLTree._rotate_left(node)

        return node

    def insert(self, key: int) -> None:
        def _insert(node: Optional[AVLNode], k: int) -> AVLNode:
            if not node:
                return AVLNode(k)
            if k < node.key:
                node.left = _insert(node.left, k)
            elif k > node.key:
                node.right = _insert(node.right, k)
            else:
                return node
            return AVLTree._rebalance(node)

        self.root = _insert(self.root, key)

    def remove(self, key: int) -> None:
        def _min_value_node(node: AVLNode) -> AVLNode:
            current = node
            while current.left:
                current = current.left
            return current

        def _remove(node: Optional[AVLNode], k: int) -> Optional[AVLNode]:
            if not node:
                return None
            if k < node.key:
                node.left = _remove(node.left, k)
            elif k > node.key:
                node.right = _remove(node.right, k)
            else:
                if not node.left or not node.right:
                    temp = node.left if node.left else node.right
                    return temp
                else:
                    succ = _min_value_node(node.right)
                    node.key = succ.key
                    node.right = _remove(node.right, succ.key)

            return AVLTree._rebalance(node)

        self.root = _remove(self.root, key)

    def contains(self, key: int) -> bool:
        curr = self.root
        while curr:
            if key == curr.key:
                return True
            curr = curr.left if key < curr.key else curr.right
        return False

    def height(self) -> int:
        return self._get_height(self.root)

    def is_balanced(self) -> bool:
        def _check(node: Optional[AVLNode]) -> bool:
            if not node:
                return True
            bf = self._get_balance(node)
            if abs(bf) > 1:
                return False
            return _check(node.left) and _check(node.right)

        return _check(self.root)
