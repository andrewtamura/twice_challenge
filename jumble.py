#!/usr/bin/env python
"""
Twice Challenge: word jumble solver
author: Andrew Tamura
data: August 27, 2014
"""
import sys
import argparse
import collections

class PrefixDictionary(collections.Mapping):
    """
    For a given string return a tuple of boolean values. First value represnts
    if the string is a valid prefix for a longer word, second value if the
    string is a valid word.

    dict = PrefixDictionary()
    dict.get("foo") => (True, True)
    dict.get("asdf") => (False, False)
    dict.get("antelope") => (False, True)
    dict.get("ab") => (True, False)
    """

    def __init__(self, file_name):
        """
        Initialize word list from file_name, a newline delimited text file of
        valid words.
        """
        self.elements = {} #internal dictionary
        with open(file_name) as word_list:
            content = word_list.readlines()
            for line in content:
                word = line.rstrip()
                if len(word) < 2:
                    #ignore one letter words
                    continue

                #Build list of prefixes for the given word
                prefixes = []
                for index in range(1, len(word)):
                    prefixes.append(word[:index])

                #Go through all the prefixes and add them to the dictionary
                for val in prefixes:
                    try:
                        prefix, valid = self.elements[val]
                        # already present, but now it's a prefix too
                        self.elements[val] = (True, valid)
                    except KeyError:
                        #not in dictionary, so save it as a prefix
                        self.elements[val] = (True, False)

                # add the final word
                try:
                    prefix, valid = self.elements[word]
                    #Was already added, but now we know it's a complete word
                    self.elements[word] = (prefix, True)
                except KeyError:
                    #Not present, add it now
                    self.elements[word] = (False, True)

    def __getitem__(self, value):
        return self.elements.get(value)

    def __iter__(self):
        return iter(self.elements)

    def  __len__(self):
        return len(self.elements)

    def is_word(self, value):
        """
        Return boolean if given value is a word
        """
        try:
            _, valid = self.elements[value]
            return valid
        except KeyError:
            return False

    def is_prefix(self, value):
        """
        Return boolean if given value is a prefix for a word
        """
        try:
            prefix, _ = self.elements[value]
            return prefix
        except KeyError:
            return False

class NaiveSolver(object):
    """
    Naive solver that does a dictionary lookup on ALL possible permutations
    not in alphabetical order
    """

    def __init__(self, file_name):
        self.dictionary = PrefixDictionary(file_name)

    def solve(self, word):
        """Recusive algorithm that builds all permutations and in the
        process checks which permutations and subpermutations are valid anagrams

        Return value is a 3 item tuple:
            (internal_path<list>, anagrams<set>, steps<int>)

            interal_path: an intermediate list that the algorithm uses to find
            permutations
            anagarms: a set containing all the anagrams
            steps: how many words the algorithm looked at

        """
        if not word:
            return 'Please enter a string of characters'
        word = word.lower() # convert to lowercase

        anagrams = set()
        steps = 0
        results = []

        if len(word) == 1:
            return ([word], anagrams, 1)
        for index, char in enumerate(word):
            remainder = ''.join([word[:index], word[index+1:]])
            sub_words, sub_anagrams, sub_steps = self.solve(remainder)
            anagrams = anagrams.union(sub_anagrams)
            steps += sub_steps
            for sub in sub_words:
                steps += 1
                new_perm = ''.join([char, sub])
                if self.dictionary.is_word(new_perm):
                    anagrams.add(new_perm)
                results.append(new_perm)
        return (results, anagrams, steps)

class BetterSolver(object):
    """
    Smarter solver, does not compute permutation that begins with an invalid
    prefix. e.g. when solving for the word 'dog', we should not compute the
    permutation 'dgo' because the prefix 'dg' is not valid.

    Uses a similar algorithm as NaiveSolver, except it builds the permutations
    backwards (relative to NaiveSolver) so that it can prune strings based on
    if the string is a prefix of a valid dictionary word.
    """

    def __init__(self, file_name):
        self.dictionary = PrefixDictionary(file_name)

    def solve(self, word):
        """Fancier recursive algorithm to find anagrams. Builds permutations so 
        that certain permutations can be skipped over.
        """

        steps = 0
        results = []
        anagrams = set()
        if len(word) == 1:
            return ([word], anagrams, 1)
        for index, char in enumerate(word):
            remainder = ''.join([word[:index], word[index+1:]])
            sub_words, sub_anagrams, sub_steps = self.solve(remainder)
            steps += sub_steps
            anagrams = anagrams.union(sub_anagrams)
            for sub in sub_words:
                steps += 1
                # build backwards to enable pruning
                new_perm = ''.join([sub, char])
                if self.dictionary.is_prefix(new_perm):
                    results.append(new_perm)
                if self.dictionary.is_word(new_perm):
                    anagrams.add(new_perm)
        return (results, anagrams, steps)

def run():
    """
    Function to contain the argparse logic, reading word from stdin, and
    formatting the output of the jumble solvers.
    """
    parser = argparse.ArgumentParser(description='Jumble Solver')
    parser.add_argument('-b', '--better',\
        help='Use better algorithm, defaults to naive algorithm',\
        action='store_true')
    args = parser.parse_args()
    if args.better:
        jumble = BetterSolver('words.txt')
    else:
        jumble = NaiveSolver('words.txt')

    sys.stdout.write('Enter word: ')
    for line in iter(sys.stdin.readline, ''):
        word = line.strip('\n')
        _, anagrams, steps = jumble.solve(word)
        print 'Found %s anagrams in %s steps' % (len(anagrams), steps)
        print list(anagrams)
        sys.stdout.write('\nEnter word: ')

if __name__ == '__main__':
    run()
