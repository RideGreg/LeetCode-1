# Time:  O(n) ~ O(2^n)
# Space: O(1) ~ O(2^n)

# 1239 weekly contest 160 10/26/2019
# Given an array of strings arr. String s is a concatenation of a sub-sequence of arr which have unique characters.
#
# Return the maximum possible length of s.

# Constraints:
# 1 <= arr.length <= 16
# 1 <= arr[i].length <= 26
# arr[i] contains only lower case English letters.

class Solution:
    def maxLength(self, arr):  # USE THIS: dfs + bit op to detect conflict
        import functools, operator
        def bitset(s):
            return functools.reduce(operator.__or__,
                                    [1<<(ord(c)-ord('a')) for c in s])
            '''ans = 0
            for c in s:
                x = ord(c) - ord('a')
                ans |= 1 << xs
            return ans'''

        def number_of_one(n):
            ans = 0
            while n:
                n &= n - 1 # remove the right-most 1
                ans += 1
            return ans

        def dfs(i, cur):
            if i == N:
                self.ans = max(self.ans, number_of_one(cur))
                return

            dfs(i + 1, cur)
            if bits[i] & cur == 0:
                dfs(i + 1, cur | bits[i])
                '''cur |= bits[i]
                dfs(i + 1, cur)
                cur ^= bits[i]'''

            '''aonther dfs
            for j in range(i, N):
                if bits[j] & cur == 0:
                    dfs(j+1, cur | bits[j])
                else:
                    dfs(j+1, cur)
            '''

        for i in range(len(arr) - 1, -1, -1): # filter string with duplicate char
            if len(arr[i]) != len(set(arr[i])):
                arr.pop(i)
        N = len(arr)
        bits = [bitset(x) for x in arr]
        self.ans = 0
        dfs(0, 0)
        return self.ans

    def maxLength_awice(self, A): # dfs + char counter to detect conflict
        # filter out words w/ duplicate letters
        for i in range(len(A) - 1, -1, -1):
            if len(set(A[i])) != len(A[i]):
                A.pop(i)
        N = len(A)

        # get each word's letter counts, traverse each word only once
        def getBits(s):
            ct = [0] * 26
            for c in s:
                ct[ord(c) - ord('a')] += 1
            return ct
        B = [getBits(w) for w in A]

        self.ans = 0
        count = [0] * 26 # concatenated string's letter counts, also used to skip conflict word

        # usually dfs params are current index + current val (this is omitted as count list can provide)
        def dfs(i):
            if i == N:
                self.ans = max(self.ans, sum(count))
                return

            for letter, ct in enumerate(B[i]):
                if ct and count[letter]:# conflict: cannot use this word
                    dfs(i + 1)
                    break
            else:
                dfs(i + 1) # choose not use this word
                # use this word
                for letter, ct in enumerate(B[i]):
                    if ct:
                        count[letter] += 1
                dfs(i + 1)
                for letter, ct in enumerate(B[i]):
                    if ct:
                        count[letter] -= 1
        dfs(0)
        return self.ans

# global var used by 2 kamyu solution: power[k] = 2^k or 1<<k, log2[n] = log2(n)
power = [1]
log2 = {1:0}
for i in range(1, 26):
    power.append(power[-1]<<1)
    log2[power[i]] = i


class Solution_kamyu(object):
    def maxLength(self, arr):  # dp (store all candidates) + bit op to detect conflict
        """
        :type arr: List[str]
        :rtype: int
        """
        def bitset(s):
            result = 0
            for c in s:
                k = ord(c)-ord('a')
                if result & (1<<k): # duplicate char
                    return 0
                result |= 1<<k
            return result
        
        def number_of_one(n):
            result = 0
            while n:
                n &= n-1
                result += 1
            return result

        dp = [0]
        for x in arr:
            x_set = bitset(x)
            if not x_set:
                continue
            orig_len = len(dp)   # edit in iteration
            for i in range(orig_len):
                if dp[i] & x_set == 0:
                    dp.append(dp[i] | x_set)
        return max(number_of_one(s_set) for s_set in dp)


# Time:  O(2^n)
# Space: O(1)
class Solution_kamyu2(object):  # hard to understand
    def maxLength(self, arr):
        """
        :type arr: List[str]
        :rtype: int
        """ 
        def bitset(s):
            result = 0
            for c in s:
                if result & power[ord(c)-ord('a')]:
                    return 0
                result |= power[ord(c)-ord('a')]
            return result
    
        bits = [bitset(x) for x in arr]
        result = 0
        for i in range(power[len(arr)]):
            curr_bitset, curr_len = 0, 0
            while i:
                j = i & -i  # rightmost bit
                i ^= j
                j = log2[j]  # log2(j)
                if not bits[j] or (curr_bitset & bits[j]):
                    break
                curr_bitset |= bits[j]
                curr_len += len(arr[j])
            else:
                result = max(result, curr_len)
        return result

print(Solution().maxLength(["unz","iq","ue"])) # 5
print(Solution().maxLength(["un","iq","uez"])) # 5
print(Solution().maxLength(["cha","r","act","ers"])) # 6 "chaers" or "acters"
print(Solution().maxLength(["abcdefghijklmnopqrstuvwxyz"])) # 26
print(Solution().maxLength(["a","b","c","d","a","b","c"])) # 4