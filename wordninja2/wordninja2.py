from typing import List, Union, Dict, Optional, Tuple
from math import log

import numpy as np
from ahocorasick import Automaton
from wordfreq import available_languages, get_frequency_dict

WordList = Union[List[str], Dict[str, float]]
StringCost = Tuple[List[str], float]


class WordNinja:
    def __init__(self, language: str, wordlist: Optional[List[str]] = None) -> None:
        self.language = language.lower()
        if wordlist is None and self.language not in available_languages():
            raise ValueError(
                f"'{self.language}' is not available. Available languages are: {' '.join(set(available_languages()))}"
            )

        self.words, self.costs = self._get_words_and_cost(self.language, wordlist)
        self.max_cost = max(self.costs) + 1e-3

        self.automaton = self._make_automaton()

    def _make_automaton(self) -> Automaton:
        automaton = Automaton()
        for index, word in enumerate(self.words):
            automaton.add_word(word, (self.costs[index], len(word)))
        automaton.make_automaton()

        return automaton

    def _get_words_and_cost(
        self, language: str, wordlist: Optional[List[str]]
    ) -> Tuple[List[str], np.ndarray]:
        if wordlist:
            words = wordlist
        else:
            words = list(get_frequency_dict(language))
        costs = np.log(np.arange(1, len(words) + 1) * log(len(words)))

        return words, costs

    def split(self, string: str) -> List[str]:
        return self.split_with_cost(string)[0]

    def split_with_cost(self, string: str) -> Tuple[List[str], float]:
        found = self.automaton.iter(string.lower())

        out = []
        costs = np.arange(len(string) + 1) * self.max_cost
        lengths = np.ones(len(string) + 1, dtype=np.int32)
        str_len = len(string)
        for end_pos, (cost, length) in found:
            # Cost of the current position
            end_pos = end_pos + 1
            curr_cost = costs[end_pos]
            new_cost = cost + costs[end_pos - length]
            if new_cost < curr_cost:
                lengths[end_pos] = length
                costs[end_pos] = new_cost

        i = str_len
        while i > 0:
            length = lengths[i]
            out.append(string[i - length : i])
            i -= length

        return list(reversed(out)), costs[-1]


class CrossLingualWordNinja:
    def __init__(
        self,
        languages: List[str],
        wordlists: Optional[List[Optional[List[str]]]] = None,
    ) -> None:
        self.languages = languages

        if wordlists is None:
            wordlists = [None] * len(languages)
        self.wordlists = wordlists

        if len(self.languages) != len(self.wordlists):
            raise ValueError(
                f"Your list of languages was not the length of your list of wordlists: {len(self.languages)} vs {len(self.wordlists)}"
            )

        self.ninjas: List[WordNinja] = [
            WordNinja(language, wordlist)
            for language, wordlist in zip(languages, wordlists)
        ]

    def get_splits(self, string) -> List[StringCost]:
        return [ninja.split_with_cost(string) for ninja in self.ninjas]

    def split(self, string: str) -> List[str]:
        results = self.get_splits(string)
        best_split, best_cost = results[0]
        for split, cost in results[1:]:
            if cost < best_cost:
                best_split = split

        return best_split
