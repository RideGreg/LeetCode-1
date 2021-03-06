# Time:  O(n)
# Space: O(1), used space is size of the alphabet, which is constant

 # 316
# Given a string which contains only lowercase letters,
# remove duplicate letters so that every letter appear
# once and only once. You must make sure your result is
# the smallest in lexicographical order among all
# possible results.
#
# Example:
# Given "bcabc"
# Return "abc"
#
# Given "cbacdcbc"
# Return "acdb"

from collections import Counter


class Solution(object):
    def removeDuplicateLetters(self, s):
        """
        :type s: str
        :rtype: str
        """
        remaining = Counter(s)

        used, stk = set(), []
        for c in s:
            if c not in used:
                while stk and stk[-1] > c and remaining[stk[-1]]:
                    used.remove(stk.pop())
                stk.append(c)
                used.add(c)
            remaining[c] -= 1
        return "".join(stk)

print(Solution().removeDuplicateLetters("cbacdcbc")) # "acdb"
