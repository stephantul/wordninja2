from gzip import open as gzip_open
from tempfile import TemporaryDirectory
from unittest.mock import patch

from wordninja2.utilities import _DEFAULT_PATH, _get_default_wordlist, get_default_wordninja


def test_get_default_wordninja() -> None:
    """Test that the default wordninja gets the right words.."""
    with patch("wordninja2.utilities._get_default_wordlist", return_value=["cat", "dog"]):
        w = get_default_wordninja()
        assert w.split("catdog") == ["cat", "dog"]
        assert list(w.word_cost) == ["cat", "dog"]


def test_default_path_exists() -> None:
    """Tests if the default wordlist is accessible."""
    assert _DEFAULT_PATH.exists()


def test_get_default_wordlist() -> None:
    """Tests the default wordlist."""
    with TemporaryDirectory() as tempdir:
        path = f"{tempdir}/wordninja_words.txt.gz"
        with gzip_open(path, "w") as f:
            f.write("cat\ndog\n".encode("utf-8"))
        with patch("wordninja2.utilities._DEFAULT_PATH", path):
            assert _get_default_wordlist() == ["cat", "dog"]
