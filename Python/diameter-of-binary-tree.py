# Time:  O(n)
# Space: O(h)

# Given a binary tree, you need to compute the length of the diameter of the tree.
# The diameter of a binary tree is the length of the longest path between
# any two nodes in a tree. This path may or may not pass through the root.
#
# Example:
# Given a binary tree 
#           1
#          / \
#         2   3
#       / \     
#       4   5    
# Return 3, which is the length of the path [4,2,1,3] or [5,2,1,3].
#
# Note: The length of path between two nodes is represented by the number of edges between them.

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):
    def diameterOfBinaryTree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        def depth(root, diameter):
            if not root: return 0, diameter
            left, diameter = depth(root.left, diameter)
            right, diameter = depth(root.right, diameter)
            return 1 + max(left, right), max(diameter, left + right)
            
        return depth(root, 0)[1]

# leverage the classical way to calculate tree depth
class Solution2(object):
    def diameterOfBinaryTree(self, root):
        self.ans = 1
        def depth(node):
            if not node: return 0
            L = depth(node.left)
            R = depth(node.right)
            self.ans = max(self.ans, L+R)
            return max(L, R) + 1

        depth(root)
        return self.ans