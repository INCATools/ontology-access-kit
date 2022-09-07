import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Tuple, Union
from urllib.parse import quote

import requests
from ontoportal_client.api import PreconfiguredOntoPortalClient
from prefixmaps.io.parser import load_multi_context
from sssom_schema import Mapping

from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.datamodels.vocabulary import SEMAPV
from oaklib.interfaces import (
    MappingProviderInterface,
    SearchInterface,
    TextAnnotatorInterface,
)
from oaklib.interfaces.basic_ontology_interface import METADATA_MAP, PREFIX_MAP
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, URI
from oaklib.utilities.apikey_manager import get_apikey_value
from oaklib.utilities.rate_limiter import check_limit

SEARCH_CONFIG = SearchConfiguration()

# See:
#   https://www.bioontology.org/wiki/BioPortal_Mappings
#   https://github.com/agroportal/project-management/wiki/Mappings
SOURCE_TO_PREDICATE = {
    "CUI": "skos:closeMatch",
    "LOOM": "skos:closeMatch",
    "REST": "skos:relatedMatch",  # maybe??
    "SAME_URI": "skos:exactMatch",
}


@dataclass
class OntoPortalImplementationBase(
    TextAnnotatorInterface, OboGraphInterface, SearchInterface, MappingProviderInterface, ABC
):

    ontoportal_client_class: ClassVar[type[PreconfiguredOntoPortalClient]] = None
    api_key: Union[str, None] = None

    label_cache: Dict[CURIE, str] = field(default_factory=lambda: {})
    ontology_cache: Dict[URI, str] = field(default_factory=lambda: {})
    focus_ontology: str = None

    def __post_init__(self):
        if self.focus_ontology is None:
            if self.resource:
                self.focus_ontology = self.resource.slug
        if not self.ontoportal_client_class:
            raise NotImplementedError("ontoportal_client_class not specified")
        if not self.api_key:
            self.api_key = get_apikey_value(self.ontoportal_client_class.name)
        self.client = self.ontoportal_client_class(api_key=self.api_key)

    def prefix_map(self) -> PREFIX_MAP:
        context = load_multi_context(["obo", "bioportal"])
        return context.as_dict()

    def _get_response(self, *args, **kwargs):
        check_limit()
        return self.client.get_response(*args, **kwargs)

    def _get_json(self, *args, **kwargs):
        response = self._get_response(*args, **kwargs)
        return response.json()

    def ontologies(self) -> Iterable[CURIE]:
        include = []
        include_str = ",".join(include)
        params = {"include": include_str}
        results = self._get_json("/ontologies", params=params)
        for result in results:
            logging.debug(result)
            yield result["acronym"]

    def ontology_versions(self, ontology: CURIE) -> Iterable[CURIE]:
        results = self._get_json(f"/ontologies/{ontology.upper()}/submissions")
        for result in results:
            logging.debug(result)
            yield result["version"]

    def ontology_metadata(self, ontology: CURIE) -> METADATA_MAP:
        # TODO: normalize metadata
        results = self._get_json(f"/ontologies/{ontology.upper()}/latest_submission")
        m = {}
        submission_url = None
        for k, v in results.items():
            if k == "@id":
                k = "submission_uri"
                submission_url = v
            if k == "@type":
                k = "type"
            if isinstance(v, dict) or isinstance(v, list):
                if k == "ontology":
                    if isinstance(v, dict):
                        m["id"] = v["acronym"]
                        m["title"] = v["name"]
            else:
                m[k] = v
        if submission_url:
            logging.info(submission_url)
            results = self._get_json(f"{submission_url}/metrics")
            for k, v in results.items():
                if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
                    if not k.startswith("@"):
                        m[k] = v
        return m

    def labels(self, curies: Iterable[CURIE], allow_none=True) -> Iterable[Tuple[CURIE, str]]:
        label_cache = self.label_cache
        for curie in curies:
            logging.debug(f"LOOKUP: {curie}")
            if curie in label_cache:
                yield curie, label_cache[curie]
            else:
                label = self.label(curie)
                label_cache[curie] = label
                yield curie, label

    def annotate_text(
        self, text: str, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        if configuration is None:
            configuration = TextAnnotationConfiguration()
        logging.info(f"Annotating text: {text}")
        # include =['prefLabel', 'synonym', 'definition', 'semanticType', 'cui']
        include = ["prefLabel", "semanticType", "cui"]
        require_exact_match = True
        include_str = ",".join(include)
        params = {"include": include_str, "require_exact_match": require_exact_match, "text": text}
        if self.resource and self.resource.slug:
            params["ontologies"] = self.resource.slug.upper()
        results = self._get_json("/annotator", params=params)
        return self._annotator_json_to_results(results, text, configuration)

    def _annotator_json_to_results(
        self, json_list: List[Any], text: str, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        seen = {}
        for obj in json_list:
            ac_obj = obj["annotatedClass"]
            for x in obj["annotations"]:
                try:
                    object_id = self.uri_to_curie(ac_obj["@id"], strict=False)
                    if object_id is None:
                        object_id = ac_obj["@id"]
                    ann = TextAnnotation(
                        subject_start=x["from"],
                        subject_end=x["to"],
                        subject_label=x["text"],
                        object_id=object_id,
                        object_label=ac_obj["prefLabel"],
                        object_source=ac_obj["links"]["ontology"],
                        match_type=x["matchType"],
                        # info=str(obj)
                    )
                    if len(text) == ann.subject_end and ann.subject_start == 1:
                        ann.matches_whole_text = True
                    if (
                        configuration
                        and configuration.matches_whole_text
                        and not ann.matches_whole_text
                    ):
                        continue
                    uid = ann.subject_start, ann.subject_end, ann.object_id
                    if uid in seen:
                        logging.debug(f"Skipping duplicative annotation to {ann.object_source}")
                        continue
                    seen[uid] = True
                    yield ann
                except KeyError:
                    # TODO: we should never catch exceptions in this way;
                    # this is temporary until we figure out why sometimes BP payloads
                    # lack some keys such as prefLabel
                    logging.error(f"Missing keys in annotation: {x} in {obj} when parsing {text}")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: SearchInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def basic_search(
        self, search_term: str, config: SearchConfiguration = SEARCH_CONFIG
    ) -> Iterable[CURIE]:
        params = {"q": search_term, "include": ["prefLabel"]}
        if self.focus_ontology:
            # Ontology acronyms in BioPortal are always uppercase
            params["ontologies"] = self.focus_ontology.upper()
        obj = self._get_json("/search", params)
        logging.debug(f"Search obj={obj}")
        collection = obj["collection"]
        while len(collection) > 0:
            result = collection[0]
            curie = self.uri_to_curie(result["@id"], use_uri_fallback=True)
            label = result.get("prefLabel", None)
            self.label_cache[curie] = label
            logging.debug(f"M: {curie} => {label}")
            yield curie
            collection = collection[1:]
            if len(collection) == 0:
                next_page = obj["links"]["nextPage"]
                if next_page:
                    obj = self._get_json(next_page)
                    collection = obj["collection"]

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Implements: MappingProviderInterface
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_sssom_mappings_by_curie(self, id: Union[CURIE, URI]) -> Iterable[Mapping]:
        ontology, class_uri = self._get_ontology_and_uri_from_id(id)
        # This may return lots of duplicate mappings
        # See: https://github.com/ncbo/ontologies_linked_data/issues/117
        quoted_class_uri = quote(class_uri, safe="")
        req_url = f"/ontologies/{ontology}/classes/{quoted_class_uri}/mappings"
        logging.debug(req_url)
        response = self._get_response(
            req_url, params={"display_context": "false"}, raise_for_status=False
        )
        if response.status_code != requests.codes.ok:
            logging.warning(f"Could not fetch mappings for {id}")
            return []
        body = response.json()
        for result in body:
            yield self.result_to_mapping(result)

    def result_to_mapping(self, result: Dict[str, Any]) -> Mapping:
        subject = result["classes"][0]
        object = result["classes"][1]
        self.add_uri_to_ontology_mapping(subject)
        self.add_uri_to_ontology_mapping(object)
        mapping = Mapping(
            subject_id=subject["@id"],
            predicate_id=SOURCE_TO_PREDICATE[result["source"]],
            mapping_justification=SEMAPV.UnspecifiedMatching.value,
            object_id=object["@id"],
            mapping_provider=result["@type"],
            mapping_tool=result["source"],
        )
        return mapping

    def add_uri_to_ontology_mapping(self, ont_class: Dict[str, Any]) -> None:
        ontology_url = ont_class["links"]["ontology"]
        acronym = ontology_url.rsplit("/", 1)[-1]
        self.ontology_cache[ont_class["@id"]] = acronym

    def ancestors(self, uri: URI) -> Iterable[URI]:
        ontology, uri = self._get_ontology_and_uri_from_id(uri)
        quoted_uri = quote(uri, safe="")
        request_url = f"/ontologies/{ontology}/classes/{quoted_uri}/ancestors"
        logging.debug(request_url)
        response = self._get_response(request_url, params={"display_context": "false"})
        if response.status_code != requests.codes.ok:
            logging.warning(f"Could not fetch ancestors for {uri}")
            return []
        body = response.json()
        for ancestor in body:
            self.add_uri_to_ontology_mapping(ancestor)
            yield self.uri_to_curie(ancestor["@id"], strict=False, use_uri_fallback=True)

    def _get_ontology_and_uri_from_id(self, id: Union[CURIE, URI]) -> Tuple[str, URI]:
        if id in self.ontology_cache:
            ontology = self.ontology_cache[id]
            uri = id
        else:
            ontology = id.split(":", 1)[0]
            uri = self.curie_to_uri(id)
        return ontology, uri
