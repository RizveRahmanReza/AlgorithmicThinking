#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <limits>
#include <memory>
#include <cassert>

namespace tree_0001 {

struct TreeNode {
    int val;
    std::unique_ptr<TreeNode> left;
    std::unique_ptr<TreeNode> right;

    explicit TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
};

// Validates whether a binary tree is a strict BST using 64-bit bounds
bool is_valid_bst_helper(const TreeNode* root, long long min_val, long long max_val) {
    if (!root) return true;
    if (root->val <= min_val || root->val >= max_val) {
        return false;
    }
    return is_valid_bst_helper(root->left.get(), min_val, root->val) &&
           is_valid_bst_helper(root->right.get(), root->val, max_val);
}

bool is_valid_bst(const TreeNode* root) {
    return is_valid_bst_helper(root, std::numeric_limits<long long>::min(),
                                     std::numeric_limits<long long>::max());
}

// Compact pre-order serialization (values delimited by spaces)
void serialize_preorder(const TreeNode* root, std::ostringstream& oss) {
    if (!root) return;
    oss << root->val << " ";
    serialize_preorder(root->left.get(), oss);
    serialize_preorder(root->right.get(), oss);
}

std::string serialize(const TreeNode* root) {
    std::ostringstream oss;
    serialize_preorder(root, oss);
    return oss.str();
}

// O(N) reconstruction from pre-order stream using upper-bound invariant
std::unique_ptr<TreeNode> deserialize_helper(const std::vector<int>& tokens,
                                             size_t& idx,
                                             long long upper_bound) {
    if (idx >= tokens.size() || tokens[idx] >= upper_bound) {
        return nullptr;
    }

    int val = tokens[idx++];
    auto node = std::make_unique<TreeNode>(val);
    node->left = deserialize_helper(tokens, idx, val);
    node->right = deserialize_helper(tokens, idx, upper_bound);
    return node;
}

std::unique_ptr<TreeNode> deserialize(const std::string& data) {
    if (data.empty()) return nullptr;
    std::istringstream iss(data);
    std::vector<int> tokens;
    int val;
    while (iss >> val) {
        tokens.push_back(val);
    }
    size_t idx = 0;
    return deserialize_helper(tokens, idx, std::numeric_limits<long long>::max());
}

void collect_inorder(const TreeNode* root, std::vector<int>& out) {
    if (!root) return;
    collect_inorder(root->left.get(), out);
    out.push_back(root->val);
    collect_inorder(root->right.get(), out);
}

} // namespace tree_0001

int main() {
    using namespace tree_0001;

    // Test 1: Construct a valid BST
    //        8
    //       / \
    //      3   10
    //     / \    \
    //    1   6    14
    auto root = std::make_unique<TreeNode>(8);
    root->left = std::make_unique<TreeNode>(3);
    root->right = std::make_unique<TreeNode>(10);
    root->left->left = std::make_unique<TreeNode>(1);
    root->left->right = std::make_unique<TreeNode>(6);
    root->right->right = std::make_unique<TreeNode>(14);

    assert(is_valid_bst(root.get()));

    // Test 2: Serialize and Deserialize roundtrip
    std::string serialized = serialize(root.get());
    auto reconstructed = deserialize(serialized);
    assert(is_valid_bst(reconstructed.get()));
    assert(serialize(reconstructed.get()) == serialized);

    std::vector<int> inorder;
    collect_inorder(reconstructed.get(), inorder);
    for (size_t i = 1; i < inorder.size(); ++i) {
        assert(inorder[i - 1] < inorder[i]);
    }

    // Test 3: Construct an invalid BST (ancestor violation)
    //        10
    //       /
    //      5
    //       \
    //        15  (15 > 10, invalid in left subtree of 10)
    auto bad_root = std::make_unique<TreeNode>(10);
    bad_root->left = std::make_unique<TreeNode>(5);
    bad_root->left->right = std::make_unique<TreeNode>(15);

    assert(!is_valid_bst(bad_root.get()));

    // Test 4: Duplicate key rejection
    auto dup_root = std::make_unique<TreeNode>(5);
    dup_root->left = std::make_unique<TreeNode>(5);
    assert(!is_valid_bst(dup_root.get()));

    std::cout << "All TREE-0001 C++20 invariant assertions passed successfully.\n";
    return 0;
}
