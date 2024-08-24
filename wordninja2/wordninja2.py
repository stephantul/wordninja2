from collections import Counter

import numpy as np
from ahocorasick_rs import AhoCorasick

from wordninja2.dataclasses import Segmentation


class WordNinja:
    """
    WordNinja is a class that can be used to split a string of words into a list of words.

    The WordNinja class uses a dynamic programming algorithm to infer the location of spaces in a string without spaces.

    Attributes
    ----------
    word_cost : dict[str, float]
        A dictionary that maps words to their costs.
    max_cost : float
        The maximum cost.
    automaton : AhoCorasick
        An Aho-Corasick automaton that is used to find matches in the wordlist.

    """

    def __init__(self, wordlist: list[str]) -> None:
        """
        Initialize a new WordNinja object.

        :param wordlist: list of words. These should be sorted in descending order of frequency.
        """
        if len(set(wordlist)) != len(wordlist):
            counts = Counter(wordlist)
            duplicates = [word for word, count in counts.items() if count > 1]
            raise ValueError(f"The wordlist contains duplicates: {duplicates}")

        costs = np.log(np.arange(1, len(wordlist) + 1) * np.log(len(wordlist)))

        self.word_cost = dict(zip(wordlist, costs))
        self.max_cost = max(costs) + 1e-3

        self.automaton = AhoCorasick(wordlist)
        # Use any because then we can short-circuit the evaluation.
        # Looks dumb, but it's not.
        self.should_lowercase = not any(not word == word.lower() for word in wordlist)

    def split(self, string: str) -> list[str]:
        """
        Split a string into a list of words.

        :param string: The string to split.
        :return: A list of words. Not all words may be in the wordlist.
        """
        return self.split_with_cost(string).tokens

    def split_with_cost(self, string: str) -> Segmentation:
        """
        Split a string into a list of words and return the cost of the segmentation.

        :param string: The string to split.
        :return: A Segmentation object containing the list of words and the cost of the segmentation.
        """
        out = []
        # The cost is initialized to the worst possible scenario.
        # Each character is a word that is not in the wordlist.
        costs = np.arange(len(string) + 1) * self.max_cost
        # All backpointers are initialized to 1.
        # This is again the worst case scenario: every character is a word.
        backpointers = np.ones(len(string) + 1, dtype=np.int32)

        if self.should_lowercase:
            string = string.lower()

        # We iterate over all matches in the string.
        for _, start_pos, end_pos in self.automaton.find_matches_as_indexes(string, overlapping=True):
            # Find the word in the string.
            form = string[start_pos:end_pos]
            # Determine the cost of the word.
            cost = self.word_cost[form]
            # Find the length of the word.
            jump = end_pos - start_pos

            # The current cost of the end position.
            curr_cost = costs[end_pos]
            # The new cost of the end position.
            new_cost = cost + costs[start_pos]
            # If the new cost of the end position is lower than
            # a previously calculated cost, we update the cost.
            if new_cost < curr_cost:
                # Update the backpointer.
                backpointers[end_pos] = jump
                costs[end_pos] = new_cost

        i = len(string)
        while i > 0:
            jump = backpointers[i]
            new_i = i - jump
            out.append(string[new_i:i])
            i = new_i

        # We now have all words in reverse order.
        tokens = list(reversed(out))

        return Segmentation(tokens=tokens, score=costs[-1])


class MultiWordNinja:
    """
    MultiWordNinja is a class that can be used to split a string of words into a list of words using multiple wordlists.

    It splits the string using all wordlists, and keeps the one with the lowest score.

    Attributes
    ----------
    word_ninjas : list[WordNinja]
        A list of WordNinja objects.

    """

    def __init__(self, wordlists: list[list[str]]) -> None:
        """
        Initialize a new MultiWordNinja object.

        :param wordlists: A list of lists of words. Each list should be sorted in descending order of frequency.
        """
        self.word_ninjas = [WordNinja(wordlist) for wordlist in wordlists]

    def split(self, string: str) -> list[str]:
        """
        Split a string into a list of words.

        :param string: The string to split.
        :return: A list of words. Not all words may be in the wordlists.
        """
        return self.split_with_cost(string).tokens

    def split_with_cost(self, string: str) -> Segmentation:
        """
        Split a string into a list of words and return the cost of the segmentation.

        :param string: The string to split.
        :return: A Segmentation object containing the list of words and the cost of the segmentation.
        """
        best_segmentation = self.word_ninjas[0].split_with_cost(string)

        for word_ninja in self.word_ninjas[1:]:
            new_segmentation = word_ninja.split_with_cost(string)
            if new_segmentation.score < best_segmentation.score:
                best_segmentation = new_segmentation

        return best_segmentation
