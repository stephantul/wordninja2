from functools import lru_cache
from gzip import open as gzip_open
from pathlib import Path

from wordninja2.wordninja2 import WordNinja

_DEFAULT_PATH = Path(__file__).parent / "resources" / "wordninja_words.txt.gz"


def _get_default_wordlist() -> list[str]:
    """
    Get the default wordlist.

    NOTE: this wordlist was included with the original wordninja.

    :return: The default wordlist.
    """
    with gzip_open(_DEFAULT_PATH, "r") as f:
        return f.read().decode().splitlines()


@lru_cache()
def get_default_wordninja() -> WordNinja:
    """
    Get the default WordNinja object.

    :return: A WordNinja object.
    """
    return WordNinja(_get_default_wordlist())
