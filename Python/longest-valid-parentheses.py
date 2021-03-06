# Time:  O(n)
# Space: O(1)
#
# Given a string containing just the characters '(' and ')',
# find the length of the longest valid (well-formed) parentheses substring.
#
# For "(()", the longest valid parentheses substring is "()", which has length = 2.
#
# Another example is ")()())", where the longest valid parentheses substring is "()()", which has length = 4.
#

class Solution(object):
    # double scan, maintain counter
    # has to do double scan. Bug if just do one scan:
    # - if update ans only when close==open: get wrong ans 0 for "(()"
    # - if update ans = 2*close when close<=open: get wrong ans 4 for "(()(()"
    def longestValidParentheses(self, s): # USE THIS: double scan, better than stack
        """
        :type s: str
        :rtype: int
        """
        ans = 0
        # forward scan
        open = close = 0
        for c in s:
            if c == '(':
                open += 1
            else:
                close += 1
                if close == open:
                    ans = max(ans, 2 * open)
                elif close > open:
                    open = close = 0

        # backward scan
        open = close = 0
        for c in reversed(s):
            if c == ')':
                close += 1
            else:
                open += 1
                if open == close:
                    ans = max(ans, 2 * open)
                elif open > close:
                    open = close = 0
        return ans


    def longestValidParentheses_doubleScan2(self, s): # prefer not to use fancy code
        def length(start, openChar, reverse):
            it = range(len(s))
            if reverse: it = reversed(it)
            depth, ans = 0, 0
            for i in it:
                if s[i] == openChar:
                    depth += 1
                else:
                    depth -= 1
                    if depth < 0:
                        start, depth = i, 0 # reset
                    elif depth == 0:
                        longest = max(ans, abs(i - start))
            return ans

        return max(length(-1, '(', False), length(len(s), ')', True))


# Time:  O(n)
# Space: O(n), store left boundary, then followed by the indices of opening chars
class Solution2: # stack
    def longestValidParentheses(self, s):
        ans, stack = 0, [-1]  # default left boundary
        for i in range(len(s)):
            if s[i] == '(':
                stack.append(i)
            else:
                stack.pop() # pop a '(' for matching or the beginning left boundary
                if stack:
                    ans = max(ans, i - stack[-1]) # has left boundary, parentheses matched
                else:
                    stack.append(i)   # no left boundary means too many ')', update left boundary
        return ans

# solution 3: O(n^2) DP also works

if __name__ == "__main__":
    print(Solution().longestValidParentheses("(()")) # 2
    print(Solution().longestValidParentheses("(()))")) # 4
    print(Solution().longestValidParentheses(")()())")) # 4
