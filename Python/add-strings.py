# Time:  O(n)
# Space: O(1)

# 415

# Given two non-negative numbers num1 and num2 represented as string,
# return the sum of num1 and num2.
#
# Note:
#
# The length of both num1 and num2 is < 5100.
# Both num1 and num2 contains only digits 0-9.
# Both num1 and num2 does not contain any leading zero.
# You must not use any built-in BigInteger library or
# convert the inputs to integer directly.

# FOLLOW UP: modify the code to handle decimal number input.
# 1. Find the index of decimal in both strings
# 2. Balance out the one which has lesser decimal values by adding 0 at the end;
# 3. Perform generic algorithm start from both the ends

class Solution(object):
    def addStrings(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        def getDecimCnt(x):
            return len(x) - 1 - x.index('.') if '.' in x else 0
        def fillZero(s, less, more):
            if less == 0:
                s += '.'
            return s + '0' * (more - less)

        decim1, decim2 = getDecimCnt(num1), getDecimCnt(num2)
        if decim1 < decim2:
            num1 = fillZero(num1, decim1, decim2)
        elif decim1 > decim2:
            num2 = fillZero(num2, decim2, decim1)

        result = []
        i, j, carry = len(num1) - 1, len(num2) - 1, 0

        while i >= 0 or j >= 0 or carry:
            if num1[i] == num2[j] == '.':
                result.append('.')
                i -= 1
                j -= 1
                continue

            if i >= 0:
                carry += ord(num1[i]) - ord('0')
                i -= 1
            if j >= 0:
                carry += ord(num2[j]) - ord('0')
                j -= 1
            carry, v = divmod(carry, 10)
            result.append(str(v))
            # result.append(str(carry % 10))
            # carry //= 10  BETTER USE divmod, easy to make a mistake by using /=
        result.reverse()

        return "".join(result).rstrip('0').rstrip('.')

    def addStrings2(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        length = max(len(num1), len(num2))
        num1 = num1.zfill(length)[::-1]
        num2 = num2.zfill(length)[::-1]
        res, plus = '', 0
        for index, num in enumerate(num1):
            tmp = str(int(num) + int(num2[index]) + plus)
            res += tmp[-1]
            if int(tmp) > 9:
                plus = 1
            else:
                plus = 0
        if plus:
            res += '1'
        return res[::-1]

print(Solution().addStrings("123.523", "11.6")) # "135.123"
print(Solution().addStrings("110.75", "9.35")) # "120.1"
print(Solution().addStrings("110.75", "9.25")) # "120"
print(Solution().addStrings("110.75", "9")) # "119.75"