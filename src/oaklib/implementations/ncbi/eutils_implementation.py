"""Abstract Base Class Adapter for EUtils."""

import logging
import os
import time
from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Iterable, Iterator, List, Optional, Tuple
from xml.etree.ElementTree import Element  # noqa S405

import requests
import requests_cache
from defusedxml.ElementTree import fromstring

__all__ = [
    "EUtilsImplementation",
]

from oaklib.constants import TIMEOUT_SECONDS
from oaklib.datamodels.vocabulary import RDF_TYPE
from oaklib.interfaces import OboGraphInterface
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    LANGUAGE_TAG,
    RELATIONSHIP,
)
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)

NCBI_REQUESTS_CACHE = ".ncbi_requests_cache"

EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ELINK_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

NCBI_API_KEY_ENV = "NCBI_API_KEY"
# NCBI allows 3 requests/second without an API key, 10 with one
REQUEST_INTERVAL = 0.34
REQUEST_INTERVAL_WITH_KEY = 0.1


@dataclass
class EUtilsImplementation(OboGraphInterface, ABC):
    """
    Wraps Eutils endpoint.
    """

    database: ClassVar[Optional[str]] = None
    entity_type: ClassVar[Optional[str]] = None

    _requests_session: requests_cache.CachedSession = None
    _last_request_time: float = 0.0

    @property
    def requests_session(self):
        if self._requests_session is None:
            self._requests_session = requests_cache.CachedSession(NCBI_REQUESTS_CACHE)
        return self._requests_session

    def _efetch(self, ids: List[str]) -> Element:
        """
        Fetch records for ids from this adapter's Entrez database.

        Uses the cached session; uncached requests are throttled to NCBI's rate limit.
        Set the NCBI_API_KEY environment variable to use an API key.
        """
        params = {"db": self.database, "id": ",".join(ids), "retmode": "xml"}
        api_key = os.environ.get(NCBI_API_KEY_ENV)
        if api_key:
            params["api_key"] = api_key
        interval = REQUEST_INTERVAL_WITH_KEY if api_key else REQUEST_INTERVAL
        wait = self._last_request_time + interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        response = self.requests_session.get(EFETCH_URL, params=params, timeout=TIMEOUT_SECONDS)
        if not getattr(response, "from_cache", False):
            self._last_request_time = time.monotonic()
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if not api_key:
                raise
            # the request URL in the message includes the API key
            redacted = str(e).replace(api_key, "******")
            raise requests.HTTPError(redacted, response=response) from None
        return fromstring(response.content)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang is not None:
            raise NotImplementedError("lang not implemented for eutils")
        n = self.node(curie)
        if n is not None:
            return n.lbl

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
    ) -> Iterator[RELATIONSHIP]:
        if not subjects:
            raise NotImplementedError("subjects must be provided")
        for s in subjects:
            yield s, RDF_TYPE, self.entity_type

    def ontologies(self) -> Iterable[CURIE]:
        yield f"infores:{self.database}"

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang is not None:
            raise NotImplementedError("lang not implemented for eutils")
        n = self.node(curie)
        if n is not None and n.meta is not None and n.meta.definition is not None:
            return n.meta.definition.val
        return None

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        yield from []

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        return {}
