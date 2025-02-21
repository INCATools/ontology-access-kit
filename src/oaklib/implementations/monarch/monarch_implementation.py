import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional

import requests_cache

from oaklib.datamodels import obograph
from oaklib.datamodels.association import Association
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import IN_TAXON
from oaklib.interfaces import OboGraphInterface, SearchInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import LANGUAGE_TAG, RELATIONSHIP
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)


GENE_REQUESTS_CACHE = ".gene_requests_cache"


BASE_URL = "http://api-v3.monarchinitiative.org/v3/api"


@dataclass
class MonarchImplementation(
    OboGraphInterface,
    AssociationProviderInterface,
    SearchInterface,
):
    _requests_session: requests_cache.CachedSession = None

    def requests_session(self):
        if self._requests_session is None:
            self._requests_session = requests_cache.CachedSession(GENE_REQUESTS_CACHE)
        return self._requests_session

    def associations(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        property_filter: Dict[PRED_CURIE, Any] = None,
        subject_closure_predicates: Optional[List[PRED_CURIE]] = None,
        predicate_closure_predicates: Optional[List[PRED_CURIE]] = None,
        object_closure_predicates: Optional[List[PRED_CURIE]] = None,
        include_modified: bool = False,
        **kwargs,
    ) -> Iterator[Association]:
        if subjects and not isinstance(subjects, list):
            subjects = list(subjects)
        if objects and not isinstance(objects, list):
            objects = list(objects)
        if subjects and objects:
            if len(subjects) != 1 and len(objects) != 1:
                raise ValueError("Monarch API only supports one subject and one object")
            url = f"{BASE_URL}/association/all?subject={subjects[0]}&object={objects[0]}"
        elif subjects:
            # TODO: check to vs from
            url = f"{BASE_URL}/association/all?subject={subjects[0]}"
        elif objects:
            url = f"{BASE_URL}/association/all?object={objects[0]}"
        else:
            raise ValueError("Must specify subjects or objects")
        yield from self._associations_from_url(url)

    def _associations_from_url(self, url, offset=1, limit=20) -> Iterator[Association]:
        logger.info(f"Fetching {url} offset={offset} limit={limit}")
        session = self.requests_session()
        response = session.get(url, params={"offset": offset, "limit": limit})
        if response.status_code != 200:
            raise ValueError(f"Error fetching issues: {response.status_code} // {response.text}")
        obj = response.json()
        total = obj["total"]
        logger.debug(f"Got {len(obj['items'])} of {total}")
        keys = [
            "subject",
            "subject_label",
            "predicate",
            "object",
            "object_label",
            "aggregator_knowledge_source",
            "primary_knowledge_source",
        ]
        for item in obj["items"]:

            def _get(k, item=item):
                v = item.get(k, None)
                if isinstance(v, list):
                    return v[0]
                return v

            yield Association(**{k: _get(k) for k in keys})
        if offset + limit < total:
            time.sleep(1)
            yield from self._associations_from_url(url, offset=offset + limit, limit=limit)

    def ontologies(self) -> Iterable[CURIE]:
        yield "infores:monarch"

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[obograph.Node]:
        session = self.requests_session()
        url = f"{BASE_URL}/entity/{curie }"
        response = session.get(url)
        if response.status_code == 500 and not strict:
            return obograph.Node(id=curie)
        if response.status_code != 200:
            return None
            # raise ValueError(
            #    f"Error fetching issues: {response.status_code} from {url} // {response.text}"
            # )
        obj = response.json()
        meta = obograph.Meta()
        defn = obj.get("description", None)
        if defn:
            meta.definition = obograph.DefinitionPropertyValue(val=defn)
        meta.xrefs = [obograph.XrefPropertyValue(val=x) for x in obj.get("xrefs", [])]
        return obograph.Node(id=curie, lbl=obj.get("symbol", None), type="CLASS", meta=meta)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        node = self.node(curie)
        if node:
            return node.lbl

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        node = self.node(curie)
        if node and node.meta and node.meta.definition:
            return node.meta.definition.val

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        **kwargs,
    ) -> Iterator[RELATIONSHIP]:
        for a in self.associations(subjects=subjects, predicates=predicates, objects=objects):
            yield a.subject, a.predicate, a.object
        if not subjects:
            return
        session = self.requests_session()
        for curie in subjects:
            url = f"{BASE_URL}/entity/{curie}"
            response = session.get(url)
            if response.status_code != 200:
                raise ValueError(
                    f"Error fetching issues: {response.status_code} from {url} // {response.text}"
                )
            obj = response.json()
            if "in_taxon" in obj:
                yield curie, IN_TAXON, obj["in_taxon"]

    def basic_search(self, search_term: str, config: SearchConfiguration = None) -> Iterable[CURIE]:
        url = f"{BASE_URL}/search"
        yield from self._search_from_url(url, search_term)

    def _search_from_url(self, url, search_term, offset=1, limit=20) -> Iterator[CURIE]:
        logger.info(f"Fetching {url} offset={offset} limit={limit}")
        session = self.requests_session()
        response = session.get(url, params={"q": search_term, "offset": offset, "limit": limit})
        if response.status_code != 200:
            raise ValueError(f"Error fetching issues: {response.status_code} // {response.text}")
        obj = response.json()
        total = obj["total"]
        logger.debug(f"Got {len(obj['items'])} of {total}")
        for item in obj["items"]:
            yield item["id"]
        if offset + limit < total:
            time.sleep(1)
            yield from self._search_from_url(url, search_term, offset=offset + limit, limit=limit)
