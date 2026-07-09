"""Constants for use across OAK."""

import os

import pystow

from oaklib.utilities.caching import FileCache

__all__ = [
    "OAKLIB_MODULE",
    "FILE_CACHE",
    "SEMSQL_SQLITE_URL_BASE",
    "SEMSQL_SQLITE_DOWNLOAD_KWARGS",
]

OAKLIB_MODULE = pystow.module("oaklib")
FILE_CACHE = FileCache(OAKLIB_MODULE)
TIMEOUT_SECONDS = 30

# Base URL for pre-built semantic-sql SQLite databases (used by the ``sqlite:obo:`` selector).
# This points at a vendor-neutral CloudFront/Cloudflare-fronted location rather than the raw
# S3 bucket (https://s3.amazonaws.com/bbop-sqlite), reducing S3 egress charges. See
# https://github.com/INCATools/ontology-access-kit/issues/897 and
# https://github.com/INCATools/semantic-sql/issues/110. Override with the environment
# variable OAKLIB_SEMSQL_SQLITE_URL_BASE if you need a different provider or mirror.
# Note: this is read once, when the module is first imported, so the environment variable
# must be set before ``oaklib.constants`` is imported for the override to take effect.
SEMSQL_SQLITE_URL_BASE = os.environ.get(
    "OAKLIB_SEMSQL_SQLITE_URL_BASE", "https://semanticsql.berkeleybop.io"
)

# The semantic-sql CDN is fronted by Cloudflare, which rejects requests sent with the default
# ``Python-urllib/x.y`` User-Agent (HTTP 403). pystow's default download backend is urllib and
# cannot set request headers, so we download these databases via the ``requests`` backend with an
# explicit User-Agent. See https://github.com/INCATools/ontology-access-kit/issues/897.
SEMSQL_SQLITE_DOWNLOAD_KWARGS = {
    "backend": "requests",
    "headers": {"User-Agent": "oaklib"},
}
