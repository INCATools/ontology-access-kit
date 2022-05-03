import logging
import unittest

from oaklib.utilities.iterator_utils import chunk

class TestChunker(unittest.TestCase):

    def test_chunker(self):
        arr = range(0, 1000)
        n = 0
        for l in chunk(arr, size=100):
            l = list(l)
            assert l[0] == n*100
            n += 1
        assert n == 10
