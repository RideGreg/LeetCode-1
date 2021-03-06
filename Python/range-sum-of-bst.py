# Time:  O(n)
# Space: O(h)

# 938
# Given the root node of a binary search tree, return the sum of values of all nodes with value between L and R (inclusive).
# The binary search tree is guaranteed to have unique values.

# The number of nodes in the tree is at most 10000.
# The final answer is guaranteed to be less than 2^31.
#
# Example 1:
# Input: root = [10,5,15,3,7,null,18], L = 7, R = 15
# Output: 32

# Example 2:
# Input: root = [10,5,15,3,7,13,18,1,null,6], L = 6, R = 10
# Output: 23

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def rangeSumBST(self, root, L, R): # also work for non-unique valued BST
        """
        :type root: TreeNode
        :type L: int
        :type R: int
        :rtype: int
        """
        if not root: return 0
        if L<=root.val<=R:
            return root.val + self.rangeSumBST(root.left, L, root.val) + self.rangeSumBST(root.right, root.val, R)
        elif root.val < L:
            return self.rangeSumBST(root.right, L, R)
        else:
            return self.rangeSumBST(root.left, L, R)


    # return wrong result 36 for testcase. Reason is we changed range (low or high) using root.val.
    # Should add if low > high: return 0
    def rangeSumBST_wrong(self, root, low, high):
        if not root:
            return 0

        if low <= root.val <= high:
            return root.val + self.rangeSumBST(root.left, low, root.val-1) + self.rangeSumBST(root.right, root.val+1, high)
        elif root.val < low:
            return self.rangeSumBST(root.right, root.val+1, high)
        else:
            return self.rangeSumBST(root.left, low, root.val-1)


    # iterative, work for both non-unique and unique valued BST. If unique-valued BST, can simplify <= to < in the last 2 if.
    def rangeSumBST_iterative(self, root, L, R):
        result = 0
        s = [root]
        while s:
            node = s.pop()
            if node:
                if L <= node.val <= R:
                    result += node.val
                if L <= node.val:
                    s.append(node.left)
                if node.val <= R:
                    s.append(node.right)
        return result

#        10
#     5      15
#       7  13
#     6
root = TreeNode(10)
root.left, root.right = TreeNode(5), TreeNode(15)
root.left.right = TreeNode(7)
root.left.right.left = TreeNode(6)
root.right.left = TreeNode(13)

print(Solution().rangeSumBST(root, 6, 10)) # 23
