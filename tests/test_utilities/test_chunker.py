"""Test chunker."""
import unittest

from oaklib.utilities.iterator_utils import chunk


class TestChunker(unittest.TestCase):
    """Test chunker."""

    def test_chunker(self):
        """Test chunker."""
        arr = range(0, 1000)
        n = 0
        for lst in chunk(arr, size=100):
            lst = list(lst)
            assert lst[0] == n * 100
            n += 1
        assert n == 10
