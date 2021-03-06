# Time:  O(n)
# Space: O(1)

# 413
# A sequence of number is called arithmetic if it consists of at least three elements
# and if the difference between any two consecutive elements is the same.
#
# For example, these are arithmetic sequence:
#
# 1, 3, 5, 7, 9
# 7, 7, 7, 7
# 3, -1, -5, -9
# The following sequence is not arithmetic.
#
# 1, 1, 2, 5, 7
#
# A zero-indexed array A consisting of N numbers is given. A slice of that array is any pair
# of integers (P, Q) such that 0 <= P < Q < N.
#
# A slice (P, Q) of array A is called arithmetic if the sequence:
# A[P], A[p + 1], ..., A[Q - 1], A[Q] is arithmetic. In particular, this means that P + 1 < Q.
#
# The function should return the number of arithmetic slices in the array A.
#
# Example:
#
# A = [1, 2, 3, 4]
#
# return: 3, for 3 arithmetic slices in A: [1, 2, 3], [2, 3, 4] and [1, 2, 3, 4] itself.

# Multiple solutions:
# https://leetcode.com/articles/arithmetic-slices/

class Solution(object):
    def numberOfArithmeticSlices(self, A): # USE THIS: constant space DP
        """
        :type A: List[int]
        :rtype: int
        """
        ans, cnt = 0, 0
        for i in range(2, len(A)):
            if A[i] - A[i-1] == A[i-1] - A[i-2]:
                cnt += 1
                ans += cnt
            else:
                cnt = 0
        return ans

    def numberOfArithmeticSlices_bookshadow(self, A):
        ans = cnt = 0
        delta = A[1] - A[0]
        for x in range(2, len(A)):
            if A[x] - A[x - 1] == delta:
                cnt += 1
                ans += cnt
            else:
                delta = A[x] - A[x - 1]
                cnt = 0
        return ans

    def numberOfArithmeticSlices_kamyu(self, A):
        res, i = 0, 0
        while i+2 < len(A):
            start = i
            while i+2 < len(A) and A[i+2] + A[i] == 2*A[i+1]:
                res += i - start + 1
                i += 1
            i += 1

        return res

print(Solution().numberOfArithmeticSlices([1,2,3,4])) # 3