import pytest

from wordninja2.wordninja2 import WordNinja


def test_wordninja() -> None:
    """Test that words are split correctly."""
    w = WordNinja(["cat", "dog"])
    assert w.split("catdog") == ["cat", "dog"]

    w = WordNinja(["cat", "cats", "s"])
    assert w.split("cats") == ["cats"]

    w = WordNinja(["cat", "s", "a", "b", "c", "d", "cats"])
    assert w.split("cats") == ["cat", "s"]


def test_wordninja_crash_empty() -> None:
    """Test that empty wordlist crashes."""
    with pytest.raises(ValueError):
        WordNinja([])


def test_wordninja_crash_duplicate() -> None:
    """Test that duplicates wordlist crashes."""
    with pytest.raises(ValueError):
        WordNinja(["cat", "cat"])


def test_wordninja_lowercase_flag() -> None:
    """Test that words are split correctly."""
    w = WordNinja(["cat", "dog"])
    assert w.should_lowercase

    w = WordNinja(["cat", "Dog"])
    assert not w.should_lowercase


def test_wordninja_lowercases() -> None:
    """Test that the wordninja actually lowercases."""
    w = WordNinja(["cat", "dog"])
    assert w.split("CATDOG") == ["cat", "dog"]

    w = WordNinja(["cat", "DOG"])
    assert w.split("CATDOG") == ["C", "A", "T", "DOG"]
