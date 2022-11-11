import unittest

from wordfreq import available_languages, get_frequency_dict

from wordninja2.wordninja2 import WordNinja


class TestWordNinja(unittest.TestCase):

    def test_language(self) -> None:
        languages = list(available_languages())
        for language in languages[:5]:
            WordNinja(language)
        
        with self.assertRaises(ValueError):
            WordNinja("wroughwruog")

    def test_own_wordlist(self) -> None:
        wordlist = ["dog", "cat", "mouse"]
        wn = WordNinja("en", wordlist)

        self.assertEqual(len(wn.automaton), 3)
        self.assertEqual(wn.words, wordlist)
        self.assertEqual(wn.language, "en")

    def test_wordfreq_wordlist(self) -> None:
        wn = WordNinja("en")

        wordlist_wordfreq = list(get_frequency_dict("en"))
        self.assertEqual(len(wordlist_wordfreq), len(wn.automaton))
        self.assertEqual(wn.words, wordlist_wordfreq)