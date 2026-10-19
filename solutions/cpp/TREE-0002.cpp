#include <iostream>
#include <algorithm>
#include <cassert>
#include <vector>
#include <cmath>

namespace tree_0002 {

struct AVLNode {
    int key;
    int height;
    AVLNode* left;
    AVLNode* right;

    explicit AVLNode(int k) : key(k), height(0), left(nullptr), right(nullptr) {}
};

class AVLTree {
private:
    AVLNode* root = nullptr;

    static int get_height(const AVLNode* node) {
        return node ? node->height : -1;
    }

    static int get_balance(const AVLNode* node) {
        return node ? get_height(node->left) - get_height(node->right) : 0;
    }

    static void update_height(AVLNode* node) {
        if (node) {
            node->height = 1 + std::max(get_height(node->left), get_height(node->right));
        }
    }

    static AVLNode* rotate_right(AVLNode* y) {
        AVLNode* x = y->left;
        AVLNode* T2 = x->right;

        x->right = y;
        y->left = T2;

        update_height(y);
        update_height(x);

        return x;
    }

    static AVLNode* rotate_left(AVLNode* x) {
        AVLNode* y = x->right;
        AVLNode* T2 = y->left;

        y->left = x;
        x->right = T2;

        update_height(x);
        update_height(y);

        return y;
    }

    static AVLNode* rebalance(AVLNode* node) {
        update_height(node);
        int balance = get_balance(node);

        // Left-Heavy
        if (balance > 1) {
            if (get_balance(node->left) < 0) {
                node->left = rotate_left(node->left); // Left-Right (LR)
            }
            return rotate_right(node); // Left-Left (LL)
        }

        // Right-Heavy
        if (balance < -1) {
            if (get_balance(node->right) > 0) {
                node->right = rotate_right(node->right); // Right-Left (RL)
            }
            return rotate_left(node); // Right-Right (RR)
        }

        return node;
    }

    AVLNode* insert_helper(AVLNode* node, int key) {
        if (!node) return new AVLNode(key);

        if (key < node->key) {
            node->left = insert_helper(node->left, key);
        } else if (key > node->key) {
            node->right = insert_helper(node->right, key);
        } else {
            return node; // Duplicate keys not inserted
        }

        return rebalance(node);
    }

    static AVLNode* find_min(AVLNode* node) {
        while (node && node->left) {
            node = node->left;
        }
        return node;
    }

    AVLNode* remove_helper(AVLNode* node, int key) {
        if (!node) return nullptr;

        if (key < node->key) {
            node->left = remove_helper(node->left, key);
        } else if (key > node->key) {
            node->right = remove_helper(node->right, key);
        } else {
            // Node to delete found
            if (!node->left || !node->right) {
                AVLNode* temp = node->left ? node->left : node->right;
                if (!temp) {
                    delete node;
                    return nullptr;
                } else {
                    *node = *temp;
                    delete temp;
                }
            } else {
                // Two children: get in-order successor
                AVLNode* temp = find_min(node->right);
                node->key = temp->key;
                node->right = remove_helper(node->right, temp->key);
            }
        }

        return rebalance(node);
    }

    static bool verify_node_balance(const AVLNode* node) {
        if (!node) return true;
        int bf = get_balance(node);
        if (bf < -1 || bf > 1) return false;
        return verify_node_balance(node->left) && verify_node_balance(node->right);
    }

    static void destroy_tree(AVLNode* node) {
        if (!node) return;
        destroy_tree(node->left);
        destroy_tree(node->right);
        delete node;
    }

public:
    AVLTree() = default;
    ~AVLTree() { destroy_tree(root); }

    void insert(int key) { root = insert_helper(root, key); }
    void remove(int key) { root = remove_helper(root, key); }

    bool contains(int key) const {
        const AVLNode* curr = root;
        while (curr) {
            if (key == curr->key) return true;
            curr = (key < curr->key) ? curr->left : curr->right;
        }
        return false;
    }

    int height() const { return get_height(root); }
    bool is_balanced() const { return verify_node_balance(root); }
};

} // namespace tree_0002

int main() {
    using namespace tree_0002;

    AVLTree tree;

    // Test 1: Sequential insertion (adversarial for naive BST)
    for (int i = 1; i <= 100; ++i) {
        tree.insert(i);
        assert(tree.is_balanced());
    }

    // Height of AVL tree with 100 nodes must be strictly <= 1.44 * log2(102) ~ 9.6
    assert(tree.height() <= 9);

    for (int i = 1; i <= 100; ++i) {
        assert(tree.contains(i));
    }
    assert(!tree.contains(101));

    // Test 2: Deletion with rebalancing
    for (int i = 1; i <= 50; ++i) {
        tree.remove(i);
        assert(tree.is_balanced());
        assert(!tree.contains(i));
    }

    for (int i = 51; i <= 100; ++i) {
        assert(tree.contains(i));
    }

    std::cout << "All TREE-0002 C++20 invariant assertions passed successfully.\n";
    return 0;
}
