# Time:  O(n * l) ~ O(n^2 * l^2)
# Space: O(n * l)

import collections

# Given an array of n distinct non-empty strings, you need to generate minimal possible abbreviations for every word following rules below.
# Begin with the first character and then the number of characters abbreviated, which followed by the last character.
# If there are any conflict, that is more than one words share the same abbreviation, a longer prefix is used instead of only the first character until making the map from word to abbreviation become unique. In other words, a final abbreviation cannot map to more than one original words.
# If the abbreviation doesn't make the word shorter, then keep it as original.
#
# The length of each word is greater than 1.
# The words consist of lowercase English letters only.
# The return answers should be in the same order as the original array.

class Solution(object):
    def wordsAbbreviation(self, dict):
        """
        :type dict: List[str]
        :rtype: List[str]
        """
        def isUnique(prefix, words):
            return sum(word.startswith(prefix) for word in words) == 1

        def toAbbr(prefix, word):
            abbr = prefix + str(len(word) - 1 - len(prefix)) + word[-1]
            return abbr if len(abbr) < len(word) else word

        abbr_to_word = collections.defaultdict(set)
        word_to_abbr = {}

        for word in dict:
            prefix = word[:1]
            abbr_to_word[toAbbr(prefix, word)].add(word)

        for abbr, conflicts in abbr_to_word.iteritems():
            if len(conflicts) > 1:
                for word in conflicts:
                    for i in xrange(2, len(word)):
                        prefix = word[:i]
                        if isUnique(prefix, conflicts):
                            word_to_abbr[word] = toAbbr(prefix, word)
                            break
            else:
                word_to_abbr[conflicts.pop()] = abbr

        return [word_to_abbr[word] for word in dict]
