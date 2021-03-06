# Time:  O(m * n * log(min(m, n)))
# Space: O(m * n)

# 1292 weekly contest 167 12/14/2019

# Given a m x n matrix mat and an integer threshold. Return the maximum side-length of a square with a sum
# less than or equal to threshold or return 0 if there is no such square.

# 1 <= m, n <= 300
# 0 <= mat[i][j] <= 10000
# 0 <= threshold <= 10^5


class Solution(object):
    def maxSideLength(self, mat, threshold): # USE THIS: block sum
        """
        :type mat: List[List[int]]
        :type threshold: int
        :rtype: int
        """
        def check(k):
            return any(dp[i][j]-dp[i-k][j]-dp[i][j-k]+dp[i-k][j-k] <= threshold
                       for i in range(k, len(dp))
                       for j in range(k, len(dp[0])))
            '''
            for i in range(mid, len(dp)):
                for j in range(mid, len(dp[0])):
                    if dp[i][j] - dp[i-mid][j] - dp[i][j-mid] + dp[i-mid][j-mid] <= threshold:
                        return True
            return False
            '''

        m, n= len(mat), len(mat[0])
        dp = [[0] * (n+1) for _ in range(m+1)] # padding
        for i in range(1, m+1):
            for j in range(1, n+1):
                dp[i][j] = dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1] + mat[i-1][j-1]

        left, right = 0, min(m, n)
        while left < right:
            mid = left + (right-left+1)//2
            if not check(mid):
                right = mid-1
            else:
                left = mid
        return left

    def maxSideLength_ming(self, mat, threshold):
        def good(k):
            if not k: return True
            for j in range(n-k+1):
                s = sum(p[i][k+j]-p[i][j] for i in range(k))
                if s <= threshold: return True
                for i in range(m-k):
                    s -= p[i][k+j]-p[i][j]
                    s += p[k+i][k + j] - p[k+i][j]
                    if s <= threshold: return True
            return False

        m, n = len(mat), len(mat[0])
        p = []
        for r in mat:
            psum = [0]
            for v in r:
                psum.append(psum[-1]+v)
            p.append(psum)

        l, r = 0, min(m, n)
        while l < r:
            mid = (l+r+1) // 2
            if good(mid):
                l = mid
            else:
                r = mid - 1
        return l

print(Solution().maxSideLength([
    [1,1,3,2,4,3,2],
    [1,1,3,2,4,3,2],
    [1,1,3,2,4,3,2]], 4)) # 2
print(Solution().maxSideLength([[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]], 1)) # 0
print(Solution().maxSideLength([[18,70],[61,1],[25,85],[14,40],[11,96],[97,96],[63,45]], 40184)) # 2
