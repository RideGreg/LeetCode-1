# Time:  O(n^2), could be improved to O(nlogn) in cpp by ordered map (bst)
# Space: O(n)

# 699
# On an infinite number line (x-axis), we drop given squares in the order they are given.
#
# The i-th square dropped (positions[i] = (left, side_length)) is a square
# with the left-most point being positions[i][0] and sidelength positions[i][1].
#
# The square is dropped with the bottom edge parallel to the number line,
# and from a higher height than all currently landed squares.
# We wait for each square to stick before dropping the next.
#
# The squares are infinitely sticky on their bottom edge, and will remain fixed
# to any positive length surface they touch (either the number line or another square).
# Squares dropped adjacent to each other will not stick together prematurely.
#
# Return a list ans of heights. Each height ans[i] represents the current highest height
# of any square we have dropped, after dropping squares represented by positions[0], positions[1], ..., positions[i].
#
# Example 1:
# Input: [[1, 2], [2, 3], [6, 1]]
# Output: [2, 5, 5]
#
# Explanation: After the first drop of positions[0] = [1, 2]:
# _aa
# _aa
# -------
# The maximum height of any square is 2.
#
# After the second drop of positions[1] = [2, 3]:
# __aaa
# __aaa
# __aaa
# _aa__
# _aa__
# --------------
# The maximum height of any square is 5.
# The larger square stays on top of the smaller square despite where its center
# of gravity is, because squares are infinitely sticky on their bottom edge.
#
# After the third drop of positions[1] = [6, 1]:
# __aaa
# __aaa
# __aaa
# _aa
# _aa___a
# --------------
# The maximum height of any square is still 5.
#
# Thus, we return an answer of [2, 5, 5]
#
# Example 2:
# Input: [[100, 100], [200, 100]]
# Output: [100, 100]
# Explanation: Adjacent squares don't get stuck prematurely - only their bottom edge can stick to surfaces.
# Note:
#
# 1 <= positions.length <= 1000.
# 1 <= positions[0] <= 10^8, 1 <= positions[1] <= 10^6.

import bisect

# Time:  O(nlogn), 1800 ms
# Space: O(n)
# Segment Tree solution (range max query).
class SegmentTree(object):
    def __init__(self, n):
        # this segment tree cannot be pre-built. It stores max height for each
        # interval and is dynamically updated when a new square falls.
        self.n = n
        self.tree = [0] * 2*n

    def update(self, i, val):
        i += self.n
        if val != self.tree[i]:
            self.tree[i] = val
            while i > 1:
                sibling = i - 1 if i % 2 else i + 1
                self.tree[i // 2] = max(self.tree[i], self.tree[sibling])
                i //= 2

    def query(self, i, j):
        i, j, maxv = i + self.n, j + self.n, 0
        while i <= j:
            if i % 2:
                maxv = max(maxv, self.tree[i])
                i += 1
            if j % 2 == 0:
                maxv = max(maxv, self.tree[j])
                j -= 1
            i //= 2
            j //= 2
        return maxv

class Solution(object):       # USE THIS
    def fallingSquares(self, positions):
        # 使用左右两端位置，极大地减少了segment tree的size。不然整条数轴每个点的高度都要记录，太多；
        # 一条边只记两次很聪明。右端位置减一，不然查询时，相邻接触的square会误认为stack在上面。
        index = set()
        for left, size in positions:
            index.add(left)
            index.add(left+size-1)
        index = sorted(list(index))
        tree = SegmentTree(len(index))

        max_height = 0
        result = []
        for left, size in positions:
            # determine the interval
            L, R = bisect.bisect_left(index, left), bisect.bisect_left(index, left+size-1)
            h = tree.query(L, R) + size
            for i in range(L, R+1):
                tree.update(i, h)
            max_height = max(max_height, h)
            result.append(max_height)
        return result
'''
class SegmentTree1(object):
    def __init__(self, N,
                 query_fn=min,
                 update_fn=lambda x, y: y,
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = [default_val] * (2 * N)
        self.lazy = [float('-inf')] * N   # not clear what is stored in 'lazy'

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):
        def pull(x): # pull up: update parents using values from children
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2 + 1])
                if self.lazy[x] != float('-inf'):
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:
                self.__apply(R, h)
                R -= 1
            L, R = L // 2, R // 2
        pull(L0)
        pull(R0)

    def query(self, L, R):
        def push(x): # push down: update children using values from parents
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] != float('-inf'):
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = float('-inf')
                n //= 2

        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        push(L)
        push(R)
        while L <= R:
            if L & 1:
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L, R = L // 2, R // 2
        return result
    
    def data(self):
        showList = []
        for i in range(self.N):
            showList.append(self.query(i, i))
        return showList

class SegmentTree2(object):
    def __init__(self, nums,
                 query_fn=min,
                 update_fn=lambda x, y: y,
                 default_val=float("inf")):
        """
        :type nums: List[int]
        """
        N = len(nums)
        self.__original_length = N
        self.__tree_length = 2**(N.bit_length() + (N&(N-1) != 0))-1
        self.__query_fn = query_fn
        self.__update_fn = update_fn
        self.__default_val = default_val
        self.__tree = [default_val for _ in range(self.__tree_length)]
        self.__lazy = [float('-inf') for _ in range(self.__tree_length)]
        self.__constructTree(nums, 0, self.__original_length-1, 0)

    def update(self, i, j, val):
        self.__updateTree(val, i, j, 0, self.__original_length-1, 0)

    def query(self, i, j):
        return self.__queryRange(i, j, 0, self.__original_length-1, 0)

    def __constructTree(self, nums, left, right, idx):
        if left > right:
             return
        if left == right:
            self.__tree[idx] = self.__update_fn(self.__tree[idx], nums[left])
            return 
        mid = left + (right-left)//2
        self.__constructTree(nums, left, mid, idx*2 + 1)
        self.__constructTree(nums, mid+1, right, idx*2 + 2)
        self.__tree[idx] = self.__query_fn(self.__tree[idx*2 + 1], self.__tree[idx*2 + 2])

    def __apply(self, left, right, idx, val):
        self.__tree[idx] = self.__update_fn(self.__tree[idx], val)
        if left != right:
            self.__lazy[idx*2 + 1] = self.__update_fn(self.__lazy[idx*2 + 1], val)
            self.__lazy[idx*2 + 2] = self.__update_fn(self.__lazy[idx*2 + 2], val)

    def __updateTree(self, val, range_left, range_right, left, right, idx):
        if left > right:
            return
        if self.__lazy[idx] != float('-inf'):
            self.__apply(left, right, idx, self.__lazy[idx])
            self.__lazy[idx] = float('-inf')
        if range_left > right or range_right < left:
            return
        if range_left <= left and right <= range_right:
            self.__apply(left, right, idx, val)
            return
        mid = left + (right-left)//2
        self.__updateTree(val, range_left, range_right, left, mid, idx*2 + 1)
        self.__updateTree(val, range_left, range_right, mid+1, right, idx*2 + 2)
        self.__tree[idx] = self.__query_fn(self.__tree[idx*2 + 1],
                                           self.__tree[idx*2 + 2])

    def __queryRange(self, range_left, range_right, left, right, idx):
        if left > right:
            return self.__default_val
        if self.__lazy[idx] != float('-inf'):
            self.__apply(left, right, idx, self.__lazy[idx])
            self.__lazy[idx] = float('-inf')
        if right < range_left or left > range_right:
            return self.__default_val
        if range_left <= left and right <= range_right:
            return self.__tree[idx]
        mid = left + (right-left)//2
        return self.__query_fn(self.__queryRange(range_left, range_right, left, mid, idx*2 + 1), 
                               self.__queryRange(range_left, range_right, mid + 1, right, idx*2 + 2))


# Time:  O(nlogn)
# Space: O(n)
# Segment Tree solution.
class Solution_kamyu_segmentTree(object):  # DONT USE: the segment tree implementation is tedious
    def fallingSquares(self, positions):
        index = set()
        for left, size in positions:
            index.add(left)
            index.add(left+size-1)
        index = sorted(list(index))
        tree = SegmentTree1(len(index), max, max, 0)
        # tree = SegmentTree2([0]*len(index), max, max, 0)

        max_height， result = 0, []
        for left, size in positions:
            L, R = bisect.bisect_left(index, left), bisect.bisect_left(index, left+size-1)
            h = tree.query(L, R) + size
            tree.update(L, R, h)
            max_height = max(max_height, h)
            result.append(max_height)
        return result
'''

# list slice assignment: maintain 2 lists: pos, heights for each change of contour height.
# Time:  O(nlogn) ~ O(n^2), 120 ms
# Space: O(n)
class Solution2(object):
    def fallingSquares(self, positions):
        # two helper lists
        pos = [-1] # x index for each new height
        heights = [0]
        maxH, result = 0, []
        for left, side in positions:
            # BISECT to determine the interval to be affected by new square. Index r is excluded.
            l = bisect.bisect_right(pos, left)   # cannot be bisect_left: [[100,100],[200,100]] => [100, 100]
            r = bisect.bisect_left(pos, left+side) # cannot be bisect_right: [[200,100], [100,100]] => [100, 100]
            high = max(heights[l-1:r]) + side
            # update. list slice assignment, previous indices in the interval were replaced
            # https://stackoverflow.com/questions/10623302/how-assignment-works-with-python-list-slice
            pos[l:r] = [left, left+side]         # Time: O(n)
            heights[l:r] = [high, heights[r-1]]  # Time: O(n)
            maxH = max(maxH, high)
            result.append(maxH)
        return result

# Time:  O(n * sqrt(n))
# Space: O(n)
class Solution3(object):
    def fallingSquares(self, positions):
        def query(heights, left, right, B, blocks, blocks_read):
            result = 0
            while left % B and left <= right:
                result = max(result, heights[left], blocks[left//B])
                left += 1
            while right % B != B-1 and left <= right:
                result = max(result, heights[right], blocks[right//B])
                right -= 1
            while left <= right:
                result = max(result, blocks[left//B], blocks_read[left//B])
                left += B
            return result

        def update(heights, left, right, B, blocks, blocks_read, h):
            while left % B and left <= right:
                heights[left] = max(heights[left], h)
                blocks_read[left//B] = max(blocks_read[left//B], h)
                left += 1
            while right % B != B-1 and left <= right:
                heights[right] = max(heights[right], h)
                blocks_read[right//B] = max(blocks_read[right//B], h)
                right -= 1
            while left <= right:
                blocks[left//B] = max(blocks[left//B], h)
                left += B

        index = set()
        for left, size in positions:
            index.add(left)
            index.add(left+size-1)
        index = sorted(list(index))
        W = len(index)
        B = int(W**.5)
        heights = [0] * W
        blocks = [0] * (B+2)
        blocks_read = [0] * (B+2)

        max_height = 0
        result = []
        for left, size in positions:
            L, R = bisect.bisect_left(index, left), bisect.bisect_left(index, left+size-1)
            h = query(heights, L, R, B, blocks, blocks_read) + size
            update(heights, L, R, B, blocks, blocks_read, h)
            max_height = max(max_height, h)
            result.append(max_height)
        return result


# Time:  O(n^2)
# Space: O(n)
class Solution4(object):
    def fallingSquares(self, positions):
        """
        :type positions: List[List[int]]
        :rtype: List[int]
        """
        heights = [0] * len(positions)
        for i in range(len(positions)):
            left_i, size_i = positions[i]
            right_i = left_i + size_i
            heights[i] += size_i
            for j in range(i+1, len(positions)):
                left_j, size_j = positions[j]
                right_j = left_j + size_j
                if left_j < right_i and left_i < right_j:  # intersect
                    heights[j] = max(heights[j], heights[i])

        result = []
        for height in heights:
            result.append(max(result[-1], height) if result else height)
        return result

# Time:  O(n^2)
# Space: O(n)
class Solution_voyageck(object):
    def fallingSquares(self, p):
        n = len(p)
        h = [0] * n    # height of each square
        h[0] = p[0][1]
        maxH = h[0]
        res = [maxH]
        for i in range(1,n):
            # max height of all touchable prev squares or 0
            h[i] = max(h[j] for j in range(i+1) \
                       if (p[i][0] < p[j][0]+p[j][1] \
                          and p[j][0] < p[i][0]+p[i][1]))
            h[i] += p[i][1]            # height of current square i
            maxH = max(maxH, h[i])
            res.append(maxH)
        return res

print(Solution().fallingSquares([[200,100], [100,100]])) # [100, 100]
print(Solution().fallingSquares([[1,2], [2,3], [6,1]])) # [2, 5, 5]
print(Solution().fallingSquares([[1,3], [2,3], [6,1]])) # [3, 6, 6]
