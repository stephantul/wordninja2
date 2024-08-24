from wordninja2.utilities import get_default_wordninja
from wordninja2.wordninja2 import MultiWordNinja, WordNinja

__all__ = ["WordNinja", "MultiWordNinja", "get_default_wordninja"]


def split(string: str) -> list[str]:
    """
    Split a string into a list of words using the default wordlist.

    :param string: The string to split.
    :return: A list of words.
    """
    return get_default_wordninja().split(string)
