# Time:  O(n) for one pass
# Space: O(n) for stack in the worst cases

# 1130
# Given an array arr of positive integers, consider all binary trees such that:
# - Each node has either 0 or 2 children;
# - The values of arr correspond to the values of each leaf in an in-order traversal of the tree.
# - The value of each non-leaf node is equal to the product of the largest leaf value
# in its left and right subtree respectively.

# Among all possible binary trees considered, return the smallest possible sum of the
# values of each non-leaf node.  It is guaranteed this sum fits into a 32-bit integer.
#
# 2 <= arr.length <= 40
# 1 <= arr[i] <= 15
#
# Example 1:
# Input: arr = [6,2,4]
# Output: 32
# Explanation:
# There are two possible trees: one has non-leaf node sum 36, the second has non-leaf node sum 32.
#
#     24            24
#    /  \          /  \
#   12   4        6    8
#  /  \               / \
# 6    2             2   4


# 解法：最上面一层一定是最大的两个数在相乘；越是底部的叶子节点，被用来做乘法的次数越多。如果想让 mct 值最小，值较小的叶子节点
# 要尽量放到底部，值较大的叶子节点尽量放靠上部分。所以需要不断找出一个极小值。乘以它左边和右边两数中较小的一个。
# 通过维护一个单调递减栈可以找到各极小值，
class Solution(object):
    # we decompose a hard problem into reasonable easy one:
    # find a local min, remove it, add the product of this local min with the lesser of its left and right
    # greater neighbors. Use a decreasing mono stack to find local mins, refer to LC 503. Next Greater Element II
    def mctFromLeafValues(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """
        result = 0
        stk = [float("inf")]
        for x in arr:
            while stk[-1] <= x:
                result += stk.pop() * min(stk[-1], x) # stk.pop() local min, stk[-1] is next greater on the left,
                                                      # x is next greater or equal on the right
            stk.append(x)
        while len(stk) > 2:                # each time go up to reach a parent node
            result += stk.pop() * stk[-1]
        return result

    # Time O(N^2) Space O(N) Remove the elements form the smallest to bigger，Similar idea to solution 1.
    #
    # When we build a node in the tree with two children numbers a and b.
    # the smaller one won't be used it anymore, and the bigger one may be used to calculate an ancestor's value.
    #
    # The problem can translated as following:
    # Given an array A, for each pair of neighbors a and b,
    # we can remove the smaller one min(a,b) and the cost is a * b.
    # What is the minimum cost to remove the whole array until only one left?
    #
    # We can remove the element form the smallest to bigger, and b will be the min of the left and the right neighbor.
    # The cost to remove a is a * min(left, right).
    def mctFromLeafValues2(self, arr):
        ans = 0
        while len(arr) > 1:
            i = arr.index(min(arr))
            nei = float('inf')
            if i > 0: nei = min(nei, arr[i-1])
            if i < len(arr)-1: nei = min(nei, arr[i+1])
            ans += nei * arr.pop(i)
        return ans

    # DP Time O(n^3) Space O(n^2)
    # dp solution test all ways to build up the tree,
    # including many unnecessary tries.
    # It's brute force testing, with memorization.
    def mctFromLeafValues_dp(self, arr):
        N = len(arr)
        dp = [[0]*N for _ in range(N)]
        for i in range(N-2, -1, -1):
            for j in range(i+1, N):
                dp[i][j] = min(dp[i][k]+dp[k+1][j]+max(arr[i:k+1])*max(arr[k+1:j+1])
                               for k in range(i, j))
        return dp[0][-1]


print(Solution().mctFromLeafValues([5, 3, 3, 1])) # 27
print(Solution().mctFromLeafValues([6, 2, 4])) # 32