import itertools
from typing import Iterable, List

DEFAULT_CHUNK = 100


def chunk(iterable: Iterable, size=DEFAULT_CHUNK) -> Iterable[List]:
    """
    Get first N results of iterable

    https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
    """
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, size)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


def chunk_to_lists(iterable: Iterable, size=DEFAULT_CHUNK) -> Iterable[List]:
    """
    Get first N results of iterable

    https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python
    """
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, size)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield list(itertools.chain((first_el,), chunk_it))
