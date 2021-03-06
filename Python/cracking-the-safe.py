# Time:  O(k^n)
# Space: O(k^n)

# There is a box protected by a password.
# The password is n digits, where each letter can be one of the first k digits 0, 1, ..., k-1.
#
# You can keep inputting the password,
# the password will automatically be matched against the last n digits entered.
#
# For example, assuming the password is "345",
# I can open it when I type "012345", but I enter a total of 6 digits.
#
# Please return any string of minimum length that is guaranteed to open the box after the entire string is inputted.
#
# Example 1:
# Input: n = 1, k = 2
# Output: "01"
# Note: "10" will be accepted too.
#
# Example 2:
# Input: n = 2, k = 2
# Output: "00110"
# Note: "01100", "10011", "11001" will be accepted too.
#
# Note:
# - n will be in the range [1, 4].
# - k will be in the range [1, 10].
# - k^n will be at most 4096.

# https://en.wikipedia.org/wiki/De_Bruijn_sequence
# https://en.wikipedia.org/wiki/Lyndon_word
class Solution(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        M = k**(n-1)
        P = [q*k+i for i in xrange(k) for q in xrange(M)]  # rotate: i*k^(n-1) + q => q*k + i
        result = [str(k-1)]*(n-1)
        for i in xrange(k**n):
            j = i
            # concatenation in lexicographic order of Lyndon words
            while P[j] >= 0:
                result.append(str(j//M))
                P[j], j = -1, P[j]
        return "".join(result)


# Time:  O(k^n)
# Space: O(k^n)
class Solution2(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        total = k**n
        M = total//k
        unique_rolling_hash = 0
        result = [str(0)]*(n-1)
        lookup = set()
        while len(lookup) < total:
            for i in reversed(xrange(k)):  # preorder like traversal relative to initial result to avoid getting stuck, i.e. don't use 0 until there is no other choice
                new_unique_rolling_hash = unique_rolling_hash*k + i
                if new_unique_rolling_hash not in lookup:
                    lookup.add(new_unique_rolling_hash)
                    result.append(str(i))
                    unique_rolling_hash = new_unique_rolling_hash%M
                    break
        return "".join(result)


# Time:  O(k^n)
# Space: O(k^n)
class Solution3(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        M = k**(n-1)
        def dfs(k, unique_rolling_hash, lookup, result):
            for i in reversed(xrange(k)):  # preorder like traversal relative to initial result to avoid getting stuck, i.e. don't use 0 until there is no other choice
                new_unique_rolling_hash = unique_rolling_hash*k + i
                if new_unique_rolling_hash not in lookup:
                    lookup.add(new_unique_rolling_hash)
                    result.append(str(i))
                    dfs(k, new_unique_rolling_hash%M, lookup, result)
                    break

        unique_rolling_hash = 0
        result = [str(0)]*(n-1)
        lookup = set()
        dfs(k, unique_rolling_hash, lookup, result)
        return "".join(result)


# Time:  O(n * k^n)
# Space: O(n * k^n)
class Solution4(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        result = [str(k-1)]*(n-1)
        lookup = set()
        total = k**n
        while len(lookup) < total:
            node = result[len(result)-n+1:]
            for i in xrange(k):  # preorder like traversal relative to initial result to avoid getting stuck, i.e. don't use k-1 until there is no other choice
                neighbor = "".join(node) + str(i)
                if neighbor not in lookup:
                    lookup.add(neighbor)
                    result.append(str(i))
                    break
        return "".join(result)


# Time:  O(n * k^n)
# Space: O(n * k^n)
class Solution5(object):
    def crackSafe(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: str
        """
        def dfs(k, node, lookup, result):
            for i in xrange(k):  # preorder like traversal relative to initial result to avoid getting stuck, i.e. don't use k-1 until there is no other choice
                neighbor = node + str(i)
                if neighbor not in lookup:
                    lookup.add(neighbor)
                    result.append(str(i))
                    dfs(k, neighbor[1:], lookup, result)
                    break

        result = [str(k-1)]*(n-1)
        lookup = set()
        dfs(k, "".join(result), lookup, result)
        return "".join(result)
