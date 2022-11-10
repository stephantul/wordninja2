from typing import List, Union, Dict, Optional
from math import log

import numpy as np
from ahocorasick import Automaton
from wordfreq import available_languages, get_frequency_dict

WordList = Union[List[str], Dict[str, float]]


class WordNinja:

    def __init__(self, language: str, wordlist: Optional[List[str]] = None) -> None:
        self.language = language.lower()
        if self.language not in available_languages():
            raise ValueError(f"{self.language} is not available.")
        
        if wordlist:
            words = wordlist
        else:
            words = list(get_frequency_dict(self.language))
        costs = np.log(np.arange(1, len(words) + 1) * log(len(words)))
            
        self.words = words
        self.costs = costs
        self.max_cost = max(self.costs) + 1e-3

        self.automaton = Automaton()
        for index, word in enumerate(self.words):
            self.automaton.add_word(word, (self.costs[index], len(word)))
        self.automaton.make_automaton()

    def split(self, string: str) -> List[str]:
        found = self.automaton.iter(string.lower())

        out = []
        costs = np.arange(len(string)) * self.max_cost
        lengths = np.ones(len(string), dtype=np.int32)
        for end_pos, (cost, length, _) in found:
            end_pos = min(end_pos + 1, len(string) - 1)
            curr_cost = costs[end_pos]
            actual_cost = cost + costs[end_pos - length]
            if actual_cost < curr_cost:
                lengths[end_pos] = length
                costs[end_pos] = actual_cost

        i = len(string) - 1 
        while i > 0:
            length = lengths[i]
            out.append(string[i - length: i])
            i -= length

        return list(reversed(out))
