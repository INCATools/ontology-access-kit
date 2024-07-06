import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple

import requests_cache

from oaklib.datamodels import obograph
from oaklib.datamodels.association import Association
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.vocabulary import IN_TAXON, IS_A
from oaklib.interfaces import OboGraphInterface, SearchInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    LANGUAGE_TAG,
    RELATIONSHIP,
)
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)


GENE_REQUESTS_CACHE = ".gene_requests_cache"


BASE_URL = "https://www.alliancegenome.org/api"


@dataclass
class AGRKBImplementation(
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
        if subjects:
            for subject in subjects:
                yield from self._interactions(subject)
                yield from self._diseases(subject)

    def _interactions(
        self,
        subject: CURIE = None,
    ) -> Iterator[Association]:
        for join_type, predicate in [
            ("genetic_interaction", "biolink:genetically_interacts_with"),
            ("molecular_interaction", "biolink:directly_physically_interacts_with"),
        ]:
            url = f"{BASE_URL}/gene/{subject}/interactions?filter.joinType={join_type}"

            def gen_assoc(obj: dict, predicate=predicate) -> Association:
                return Association(
                    subject=subject,
                    predicate=predicate,
                    object=obj["geneB"]["id"],
                )

            yield from self._associations_from_url(url, gen_assoc)

    def _diseases(
        self,
        subject: CURIE = None,
    ) -> Iterator[Association]:
        url = f"{BASE_URL}/gene/{subject}/disease"

        def gen_assoc(obj: dict) -> Association:
            return Association(
                subject=subject,
                predicate="biolink:has_phenotype",
                object=obj["disease"]["id"],
            )

        yield from self._associations_from_url(url, gen_assoc)

    def _associations_from_url(
        self, url, gen_assoc: Callable, offset=1, limit=20
    ) -> Iterator[Association]:
        logger.info(f"Fetching {url} offset={offset} limit={limit}")
        session = self.requests_session()
        response = session.get(url, params={"offset": offset, "limit": limit})
        if response.status_code != 200:
            raise ValueError(f"Error fetching issues: {response.status_code} // {response.text}")
        obj = response.json()
        total = obj["total"]
        logger.debug(f"Got {len(obj['results'])} of {total}")
        for item in obj["results"]:
            yield gen_assoc(item)
        if offset + limit < total:
            time.sleep(1)
            yield from self._associations_from_url(
                url, gen_assoc, offset=offset + limit, limit=limit
            )

    def ontologies(self) -> Iterable[CURIE]:
        yield "infores:monarch"

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> obograph.Node:
        """
        Get a node by CURIE.

        Currently the only node type supported is a gene.

        :param curie:
        :param strict:
        :param include_metadata:
        :param expand_curies:
        :return:
        """

        session = self.requests_session()
        url = f"{BASE_URL}/gene/{curie}"
        response = session.get(url)
        if response.status_code == 500 and not strict:
            return obograph.Node(id=curie)
        if response.status_code != 200:
            return obograph.Node(id=curie)
        obj = response.json()
        meta = obograph.Meta()
        defn = obj.get("geneSynopsis", None)
        if defn:
            meta.definition = obograph.DefinitionPropertyValue(val=defn)
        meta.xrefs = [obograph.XrefPropertyValue(val=x) for x in obj.get("secondaryIds", [])]
        for _k, vs in obj.get("crossReferenceMap", {}).items():
            if not isinstance(vs, list):
                vs = [vs]

            def fix(obj) -> Optional[str]:
                v = obj["name"]
                if v.startswith("NCBI_"):
                    v = v.replace("NCBI_", "NCBI")
                if ":" not in v:
                    return None
                return v

            vs = [fix(v) for v in vs]
            meta.xrefs.extend([obograph.XrefPropertyValue(val=v) for v in vs if v])
        meta.synonyms = [
            obograph.SynonymPropertyValue(val=x, pred="hasRelatedSynonym")
            for x in obj.get("synonyms", [])
        ]
        return obograph.Node(id=curie, lbl=obj.get("symbol", None), type="CLASS", meta=meta)

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        try:
            node = self.node(curie)
            if node:
                return node.lbl
        except ValueError:
            return None

    def simple_mappings_by_curie(self, curie: CURIE) -> Iterable[Tuple[PRED_CURIE, CURIE]]:
        node = self.node(curie)
        if node and node.meta and node.meta.xrefs:
            for xref in node.meta.xrefs:
                yield xref.val, curie

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        node = self.node(curie)
        if node and node.meta and node.meta.synonyms:
            m = {}
            for s in node.meta.synonyms:
                if s.pred not in m:
                    m[s.pred] = []
                m[s.pred].append(s.val)
            return m

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
    ) -> Iterator[RELATIONSHIP]:
        # for a in self.associations(subjects=subjects, predicates=predicates, objects=objects):
        #    yield a.subject, a.predicate, a.object
        if not subjects:
            return
        session = self.requests_session()
        for curie in subjects:
            url = f"{BASE_URL}/gene/{curie}"
            response = session.get(url)
            if response.status_code != 200:
                raise ValueError(
                    f"Error fetching issues: {response.status_code} from {url} // {response.text}"
                )
            obj = response.json()
            if "in_taxon" in obj:
                yield curie, IN_TAXON, obj["species"]["taxonId"]
            yield curie, IS_A, obj["soTerm"]["id"]

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
        logger.debug(f"Got {len(obj['results'])} of {total}")
        for item in obj["results"]:
            yield item["id"]
        if offset + limit < total:
            time.sleep(1)
            yield from self._search_from_url(url, search_term, offset=offset + limit, limit=limit)
