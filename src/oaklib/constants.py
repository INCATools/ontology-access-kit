"""Constants for use across OAK."""

import pystow

from oaklib.utilities.caching import FileCache

__all__ = [
    "OAKLIB_MODULE",
    "FILE_CACHE",
]

OAKLIB_MODULE = pystow.module("oaklib")
FILE_CACHE = FileCache(OAKLIB_MODULE)
TIMEOUT_SECONDS = 30
