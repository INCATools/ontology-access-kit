import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional

import requests_cache

from oaklib.datamodels import obograph
from oaklib.datamodels.association import Association
from oaklib.interfaces import OboGraphInterface, SearchInterface
from oaklib.interfaces.association_provider_interface import (
    AssociationProviderInterface,
)
from oaklib.interfaces.basic_ontology_interface import (
    LANGUAGE_TAG,
    RELATIONSHIP,
)
from oaklib.interfaces.usages_interface import UsagesInterface
from oaklib.types import CURIE, PRED_CURIE

logger = logging.getLogger(__name__)


QUICKGO_REQUESTS_CACHE = ".quickgo_requests_cache"


BASE_URL = "https://www.ebi.ac.uk/QuickGO/services"


@dataclass
class QuickGOImplementation(
    OboGraphInterface,
    AssociationProviderInterface,
    SearchInterface,
    UsagesInterface,
):
    _requests_session: requests_cache.CachedSession = None

    _source: str = None

    def __post_init__(self):
        self._source = self.resource.slug

    def requests_session(self):
        if self._requests_session is None:
            self._requests_session = requests_cache.CachedSession(QUICKGO_REQUESTS_CACHE)
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
        session = self.requests_session()
        if subjects and not isinstance(subjects, list):
            subjects = list(subjects)
        if objects and not isinstance(objects, list):
            objects = list(objects)
        url = f"{BASE_URL}/annotation/search"

        params = {"includeFields": "goName,name"}
        # QuickGO also allows querying miRNA, for now limit searches to gene-centric subsets
        params["proteome"] = "gcrpCan"
        params["geneProductType"] = "protein"
        if subjects:
            subjects = [x.replace("UniProtKB:", "") for x in subjects]
            params["geneProductId"] = ",".join(subjects)
        if objects:
            params["goId"] = ",".join(objects)
            if object_closure_predicates:
                params["goUsage"] = "descendants"
            else:
                params["goUsage"] = "exact"
        if predicates:
            params["goUsageRelationships"] = ",".join(predicates)
        if self._source:
            params["taxonId"] = self._source.replace("NCBITaxon:", "")

        def _xrefs(x: Any) -> Iterator[str]:
            if x is None:
                return
            if isinstance(x, list):
                for y in x:
                    yield from _xrefs(y)
            elif "connectedXrefs" in x:
                yield from _xrefs(x["connectedXrefs"])
            else:
                yield f"{x['db']}:{x['id']}"

        def gen_assoc(result: dict) -> Association:
            qualifier = result.get("qualifier", None)
            if "goId" not in result:
                raise ValueError(f"Missing goId in {result}")
            with_from = list(_xrefs(result["withFrom"]))
            return Association(
                subject=result["geneProductId"],
                subject_label=result["symbol"],
                predicate=f"biolink:{qualifier}",
                object=result["goId"],
                object_label=result["goName"],
                evidence_type=result["evidenceCode"],
                publications=[result["reference"]],
                supporting_objects=with_from,
            )

        page = 0
        while True:
            page += 1
            params["page"] = page
            response = session.get(url, params=params)

            response.raise_for_status()
            obj = response.json()
            results = obj["results"]

            for result in results:
                yield gen_assoc(result)

            page_info = obj["pageInfo"]
            num_rows = page_info["resultsPerPage"] * page
            if num_rows >= page_info["total"]:
                break
            else:
                time.sleep(0.1)

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> obograph.Node:
        session = self.requests_session()
        q = curie.replace("UniProtKB:", "")
        url = f"{BASE_URL}/geneproduct/{q}"
        response = session.get(url)
        if response.status_code == 500 and not strict:
            return obograph.Node(id=curie)
        response.raise_for_status()
        obj = response.json()
        results = obj["results"]
        if not results:
            return obograph.Node(id=curie)
        result = results[0]
        node = obograph.Node(
            id=curie,
            lbl=result["symbol"],
            meta=None,
        )
        return node

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if curie.startswith("biolink:"):
            return None
        try:
            node = self.node(curie)
            if node:
                return node.lbl
        except ValueError:
            return None

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
        for x in []:
            yield x
        return

    def sssom_mappings(self, *args, **kwargs) -> Iterable[Mapping]:
        for x in []:
            yield x
        return
