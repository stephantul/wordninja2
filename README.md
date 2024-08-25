# wordninja2

wordninja2 is a faster version of [wordninja](https://github.com/keredson/wordninja). Wordninja is a word-based unigram LM that splits strings that contain words without spaces into words, as follows:

```python
>>> from wordninja2 import split
>>> split("waldorfastorianewyork")
['waldorf', 'astoria', 'new', 'york']
>>> split("besthotelpricesyoucanfind")
['best', 'hotel', 'prices', 'you', 'can', 'find']

```

Wordninja was originally defined in [a stackoverflow thread](https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words/11642687#11642687), and then rewritten into a Python package.

As the original wordninja isn't really maintained, and contains some inconsistencies, I decided to rewrite it. See below for a comparison between wordninja and wordninja2.

# Usage

wordninja2 is packaged with a wordlist, which allows you to use it out of the box. To facilitate migrating from wordninja to wordninja2, we use the exact same wordlist.

```python
>>> from wordninja2 import split
>>> split("HelloIfoundanewhousewiththreebedroomswouldwebeabletoshareit?")
['Hello',
 'I',
 'found',
 'a',
 'new',
 'house',
 'with',
 'three',
 'bedrooms',
 'would',
 'we',
 'be',
 'able',
 'to',
 'share',
 'it',
 '?']

 ```

Using wordninja2 with your own wordlist is easy, and works regardless of punctuation in tokens or the languages of those tokens.

```python
>>> from wordninja2 import WordNinja
>>> my_words = ["dog", "cat", "房子"]
>>> wn = WordNinja(my_words)
>>> wn.split("idogcat房子house")
["i", "dog", "cat", "房子", "h", "o", "u", "s", "e"]

```

Note that any wordlist you supply should be in descending order of importance. That is, wordninja assumes that words higher in the list should get precedence in segmentation over words that are lower in the list. The example that follows shows what happens.

```python
>>> from wordninja2 import WordNinja
>>> my_words = ["dog", "s", "a", "b", "c", "d", "e", "f", "dogs"]
>>> wn = WordNinja(my_words)
>>> wn.split("dogs")
["dog", "s"]

>>> my_words = ["dogs", "dog", "s"]
>>> wn = WordNinja(my_words)
>>> wn.split("dogsdog")
["dogs", "dog"]

```

# Differences with wordninja

In this section I'll highlight some differences between `wordninja` and `wordninja2`.

## Consistency

The original `wordninja` is not self-consistent, that is, the following assert fails.

```python
string = "this,string-split it"
assert "".join(split(string)) == string

```

This is because `wordninja` removes all non-word characters from the string before processing it. This also has the consequence of `wordninja` never being able to detect words with these special characters in them.

`wordninja2` is completely self-consistent, and does not remove any special characters from a string.

## Speed

`wordninja2` is twice as fast than `wordninja`. Segmenting the entire text of Mary Shelley's Frankenstein (which you can download [here](https://www.gutenberg.org/ebooks/84)):

```python
>>> import re

>>> from wordninja2 import split
>>> from wordninja import split as old_split

# Remove all spaces.
>>> txt = re.sub(r"\s", "", open("pg84.txt").read())
>>> %timeit split(txt)
299 ms ± 4.32 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
>>> %timeit old_split(txt)
1.89 s ± 36.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

```

The original wordninja has an algorithm that backtracks up to the length of the longest word for each character in the string. Thus, if your wordlist has even a single long word, the entire algorithm will start taking a really long time. Coincidentally, the default wordlist used in `wordninja` has a really long word: `llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch`, see [here](https://www.atlasobscura.com/places/llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch) for additional background.

To avoid backtracking, `wordninja2` uses the [aho-corasick algorithm](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm). We use a fast implementation in Rust: [aho-corasick](https://github.com/BurntSushi/aho-corasick), with python bindings: [aho-corasick-rs](https://github.com/G-Research/ahocorasick_rs/).

# Dependencies

See the [pyproject.toml](pyproject.toml) file. We only rely on the aforementioned aho-corasick implementation and numpy.

# Installation

Clone the repo and run `make install`. I might put this on `pypi` later.

# Tests

`wordninja2` has 100% test coverage, run `make test` to run the tests.

# License

MIT

# Author

* Stéphan Tulkens
* The original code is by [keredson](https://github.com/keredson)
* The original algorithm was written by [Generic Human](https://stackoverflow.com/users/1515832/generic-human)
