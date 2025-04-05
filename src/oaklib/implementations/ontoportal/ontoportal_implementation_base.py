import collections
import itertools
import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Iterable, Iterator, List, Optional, Tuple, Union
from urllib.parse import quote

import requests
from ontoportal_client.api import PreconfiguredOntoPortalClient
from prefixmaps.io.parser import load_multi_context
from sssom_schema import Mapping

from oaklib.datamodels.obograph import DefinitionPropertyValue, Edge, Graph, Meta, Node, SynonymPropertyValue
from oaklib.datamodels.search import SearchConfiguration
from oaklib.datamodels.text_annotator import TextAnnotation, TextAnnotationConfiguration
from oaklib.datamodels.vocabulary import LABEL_PREDICATE, SEMAPV
from oaklib.interfaces import (
    MappingProviderInterface,
    SearchInterface,
    TextAnnotatorInterface,
)
from oaklib.interfaces.basic_ontology_interface import (
    ALIAS_MAP,
    LANGUAGE_TAG,
    METADATA_MAP,
    PREFIX_MAP,
    RELATIONSHIP,
)
from oaklib.interfaces.dumper_interface import DumperInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.types import CURIE, PRED_CURIE, URI
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
    DumperInterface,
    TextAnnotatorInterface,
    OboGraphInterface,
    SearchInterface,
    MappingProviderInterface,
    ABC,
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

    def ontology_metadata_map(self, ontology: CURIE) -> METADATA_MAP:
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
            from requests import HTTPError

            try:
                results = self._get_json(f"{submission_url}/metrics")
                for k, v in results.items():
                    if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
                        if not k.startswith("@"):
                            m[k] = v
            except HTTPError as e:
                logging.error(
                    f"Could not fetch metrics for ontology {ontology} via {submission_url}\n"
                    f"Exception: {e}"
                )
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

    def label(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError("Language not supported")
        _obj = self._class(curie)
        return _obj.get("prefLabel", None)

    def _class(self, curie: CURIE) -> dict:
        ontology, class_uri = self._get_ontology_and_uri_from_id(curie)
        logging.debug(f"Fetching class for {ontology} class = {class_uri}")
        quoted_class_uri = quote(class_uri, safe="")
        req_url = f"/ontologies/{ontology}/classes/{quoted_class_uri}"
        logging.debug(req_url)
        response = self._get_response(
            req_url, params={"display_context": "false"}, raise_for_status=False
        )
        if response.status_code != requests.codes.ok:
            logging.warning(f"Could not fetch class for {curie}")
            return {}
        return response.json()

    def annotate_text(
        self, text: str, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        """
         Implements annotate_text from text_annotator_interface by calling the
         `annotate` endpoint using ontoportal client.

        :param text: Text to be annotated.
        :param configuration: Text annotation configuration.
        :return: A generator function that returns annotated results.
        """
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
        logging.debug(f"Annotate results: {results}")
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

    def sssom_mappings(
        self, curies: Optional[Union[CURIE, Iterable[CURIE]]] = None, source: Optional[str] = None
    ) -> Iterable[Mapping]:
        if not isinstance(curies, str):
            if isinstance(curies, collections.Iterable):
                curies = list(curies)
            if not isinstance(curies, list):
                raise ValueError(f"Invalid curies: {curies}")
            for curie in curies:
                yield from self.sssom_mappings(curie, source=source)
            return
        id = curies
        ontology, class_uri = self._get_ontology_and_uri_from_id(id)
        logging.debug(f"Fetching mappings for {ontology} class = {class_uri}")
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
        yielded = set()
        for result in body:
            m = self.result_to_mapping(result)
            if str(m) not in yielded:
                yield m
            yielded.add(str(m))

    def result_to_mapping(self, result: Dict[str, Any]) -> Mapping:
        subject = result["classes"][0]
        object = result["classes"][1]
        self.add_uri_to_ontology_mapping(subject)
        self.add_uri_to_ontology_mapping(object)
        mapping = Mapping(
            subject_id=self.uri_to_curie(subject["@id"]),
            predicate_id=SOURCE_TO_PREDICATE[result["source"]],
            mapping_justification=SEMAPV.UnspecifiedMatching.value,
            object_id=self.uri_to_curie(object["@id"], use_uri_fallback=True),
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

    def relationships(
        self,
        subjects: Iterable[CURIE] = None,
        predicates: Iterable[PRED_CURIE] = None,
        objects: Iterable[CURIE] = None,
        include_tbox: bool = True,
        include_abox: bool = True,
        include_entailed: bool = False,
        exclude_blank: bool = True,
        invert: bool = False,
    ) -> Iterator[RELATIONSHIP]:
        """
        Yields all relationships matching query constraints from Ontoportal.

        This implementation will fetch the class hierarchy and properties for the specified subjects.

        :param subjects: constrain search to these subjects (i.e outgoing edges)
        :param predicates: constrain search to these predicates
        :param objects: constrain search to these objects (i.e incoming edges)
        :param include_tbox: if true, include class-class relationships (default True)
        :param include_abox: if true, include instance-instance/class relationships (default True)
        :param include_entailed: include inferred relationships
        :param exclude_blank: do not include blank nodes/anonymous expressions
        :param invert: if true, invert the relationship
        :return: iterator over subject-predicate-object triples
        """
        if invert:
            for s, p, o in self.relationships(
                subjects=objects,
                predicates=predicates,
                objects=subjects,
                include_tbox=include_tbox,
                include_abox=include_abox,
                include_entailed=include_entailed,
                exclude_blank=exclude_blank,
            ):
                yield o, p, s
            return

        if subjects is None and objects is None:
            # We need at least subjects or objects
            if self.focus_ontology:
                # Get some entities to use as subjects if focus_ontology is set
                subjects = list(
                    itertools.islice(self.entities(), 100)
                )  # Limit to first 100 to avoid overwhelming the API
            else:
                logging.warning("No subjects or objects specified, and no focus_ontology set")
                return

        # If objects is specified but not subjects, we need to handle this specially
        if subjects is None and objects is not None:
            # For each object, look for subjects that have a relationship to it
            for obj in objects:
                ontology, uri = self._get_ontology_and_uri_from_id(obj)
                quoted_uri = quote(uri, safe="")
                req_url = f"/ontologies/{ontology}/classes/{quoted_uri}/children"

                response = self._get_response(req_url, params={"display_context": "false"})
                if response.status_code != requests.codes.ok:
                    logging.warning(f"Could not fetch children for {obj}")
                    continue

                results = response.json()
                for child in results:
                    child_id = self.uri_to_curie(child["@id"], strict=False)
                    if predicates is None or "rdfs:subClassOf" in predicates:
                        yield child_id, "rdfs:subClassOf", obj
            return

        # Process subjects
        if subjects is not None:
            for subject in subjects:
                ontology, uri = self._get_ontology_and_uri_from_id(subject)
                quoted_uri = quote(uri, safe="")

                # Get subClassOf relationships from parents
                req_url = f"/ontologies/{ontology}/classes/{quoted_uri}/parents"
                response = self._get_response(req_url, params={"display_context": "false"})

                if response.status_code == requests.codes.ok:
                    parents = response.json()
                    for parent in parents:
                        parent_id = self.uri_to_curie(parent["@id"], strict=False)
                        if objects is None or parent_id in objects:
                            if predicates is None or "rdfs:subClassOf" in predicates:
                                yield subject, "rdfs:subClassOf", parent_id

                # Get property relationships
                req_url = f"/ontologies/{ontology}/classes/{quoted_uri}"
                params = {"display_context": "false", "include": "properties,children"}
                response = self._get_response(req_url, params=params)

                if response.status_code == requests.codes.ok:
                    cls_data = response.json()

                    # Process properties if available
                    if "properties" in cls_data:
                        for prop in cls_data.get("properties", []):
                            if isinstance(prop, dict) and "property" in prop and "values" in prop:
                                prop_id = prop["property"]
                                if predicates is None or prop_id in predicates:
                                    for value in prop["values"]:
                                        if isinstance(value, str):
                                            try:
                                                obj_id = self.uri_to_curie(value, strict=False)
                                                if objects is None or obj_id in objects:
                                                    yield subject, prop_id, obj_id
                                            except Exception:
                                                # If we can't parse as a URI, treat as a literal
                                                if not exclude_blank:
                                                    yield subject, prop_id, value

    def _get_ontology_and_uri_from_id(self, id: Union[CURIE, URI]) -> Tuple[str, URI]:
        if id in self.ontology_cache:
            ontology = self.ontology_cache[id]
            uri = id
        else:
            ontology = id.split(":", 1)[0]
            uri = self.curie_to_uri(id)
            if ontology.lower() == "fbbt":
                ontology = "FB-BT"
            elif ontology.lower() == "wbbt":
                ontology = "WB-BT"
        return ontology, uri

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        """
        Yields all known entity CURIEs from the ontology.

        :param filter_obsoletes: if True, exclude any obsolete/deprecated element
        :param owl_type: CURIE for RDF metaclass for the object, e.g. owl:Class
        :return: iterator over CURIEs
        """
        if self.focus_ontology:
            ontology = self.focus_ontology.upper()
            params = {"include": "prefLabel", "display_context": "false", "display_links": "false"}
            req_url = f"/ontologies/{ontology}/classes"
            logging.debug(f"Fetching classes for ontology {ontology}")

            current_page_url = req_url

            while current_page_url:
                response = self._get_response(current_page_url, params=params)
                if response.status_code != requests.codes.ok:
                    logging.warning(f"Could not fetch classes for ontology {ontology}")
                    return

                results = response.json()
                collection = results.get("collection", [])

                for result in collection:
                    entity_id = self.uri_to_curie(result["@id"], strict=False)
                    if entity_id:
                        label = result.get("prefLabel", None)
                        if label:
                            self.label_cache[entity_id] = label
                        yield entity_id

                # Check for next page
                links = results.get("links", {})
                next_page = links.get("nextPage")

                if next_page:
                    current_page_url = next_page
                    # Clear params for subsequent requests as they're included in the nextPage URL
                    params = {}
                else:
                    current_page_url = None
        else:
            logging.warning("No focus_ontology specified; cannot list all entities")
            yield from []

    def as_obograph(self, expand_curies=False) -> Graph:
        """
        Convert entire resource to an OBO Graph object

        :param expand_curies: if True expand CURIEs to URIs
        :return: Graph object
        """
        if self.focus_ontology:
            # For OntoPortal, we consider the focus ontology as the graph to convert
            ontology = self.focus_ontology.upper()

            # Create a graph with the ontology ID
            g = Graph(id=ontology)

            # Collect nodes (limited to avoid overwhelming the API)
            entities = list(itertools.islice(self.entities(), 1000))

            # Get nodes with metadata
            nodes = []
            for entity in entities:
                node = self.node(entity, include_metadata=True, expand_curies=expand_curies)
                if node:
                    nodes.append(node)

            # Get edges for these entities
            edges = []
            for entity in entities:
                for rel in self.relationships([entity]):
                    s, p, o = rel
                    if p == "rdfs:subClassOf":
                        p = "is_a"  # OboGraph expects "is_a" for subClassOf
                    edges.append(Edge(sub=s, pred=p, obj=o))

            g.nodes = nodes
            g.edges = edges

            return g
        else:
            raise ValueError("No focus_ontology specified for as_obograph()")

    def entity_alias_map(self, curie: CURIE) -> ALIAS_MAP:
        meta = self.node(curie).meta
        m = collections.defaultdict(list)
        lbl = self.label(curie)
        if lbl:
            m[LABEL_PREDICATE] = [lbl]
        if meta is not None:
            for syn in meta.synonyms:
                from oaklib.converters.obo_graph_to_rdf_owl_converter import SCOPE_MAP
                pred = SCOPE_MAP.get(syn.pred, None)
                m[pred].append(syn.val)
        return m

    def definition(self, curie: CURIE, lang: Optional[LANGUAGE_TAG] = None) -> Optional[str]:
        if lang:
            raise NotImplementedError("Language tags not supported")
        m = self.node(curie).meta
        if m:
            return m.definition.val

    def dump(self, path: str = None, syntax: str = "obojson", **kwargs):
        """
        Exports current contents in the specified syntax.

        This is a simplified implementation that supports JSON-based formats.

        :param path: Path to file to write to. If None, then write to stdout.
        :param syntax: Syntax to use (default: obojson)
        :param kwargs: Additional arguments
        :return: None
        """
        if not self.focus_ontology:
            raise ValueError("No focus_ontology specified for dump()")

        if syntax in ["obo", "obojson", "json"]:
            return super().dump(path, syntax, **kwargs)
        else:
            raise ValueError(
                f"Unsupported syntax for Ontoportal dump: {syntax}. Try 'obojson' instead."
            )

    def node(
        self, curie: CURIE, strict=False, include_metadata=False, expand_curies=False
    ) -> Optional[Node]:
        """
        Look up a node object by CURIE in the ontoportal implementation

        :param curie: identifier of node
        :param strict: raise exception if node not found
        :param include_metadata: include detailed metadata
        :param expand_curies: if True expand CURIEs to URIs
        :return: Node object containing class information
        """
        ontology, class_uri = self._get_ontology_and_uri_from_id(curie)
        logging.debug(f"Fetching node for {ontology} class = {class_uri}")

        # Build the parameters for the API request
        params = {"display_context": "false"}
        if include_metadata:
            # Include additional information like synonyms, definitions, etc.
            params["include"] = "prefLabel,synonym,definition,obsolete,properties"

        if not class_uri:
            # If class_uri is empty, return None
            if strict:
                raise ValueError(f"Could not fetch node for {curie}")
            return None
        quoted_class_uri = quote(class_uri, safe="")
        req_url = f"/ontologies/{ontology}/classes/{quoted_class_uri}"

        logging.debug(req_url)
        response = self._get_response(req_url, params=params, raise_for_status=False)

        if response.status_code != requests.codes.ok:
            if strict:
                raise ValueError(f"Could not fetch node for {curie}")
            return None

        result = response.json()

        # Get node ID (either expanded URI or CURIE)
        node_id = result["@id"]
        if not expand_curies:
            node_id = self.uri_to_curie(node_id, strict=False)

        # Get the label
        label = result.get("prefLabel", None)
        if label:
            self.label_cache[curie] = label

        # Create the basic node with ID and label
        node = Node(id=node_id, lbl=label, type="CLASS")

        # Add metadata if requested
        if include_metadata:
            meta = {}

            # Add synonyms if available
            if "synonym" in result:
                synonyms = []
                for syn in result.get("synonym", []):
                    if isinstance(syn, str):
                        # Simple string synonym
                        synonyms.append(SynonymPropertyValue(pred="hasExactSynonym", val=syn))
                    elif isinstance(syn, dict) and "value" in syn:
                        # Dictionary with synonym value and possibly scope
                        scope = syn.get("scope", "EXACT")
                        pred = "hasExactSynonym"  # Use values that match ScopeEnum
                        if scope == "BROAD":
                            pred = "hasBroadSynonym"
                        elif scope == "NARROW":
                            pred = "hasNarrowSynonym"
                        elif scope == "RELATED":
                            pred = "hasRelatedSynonym"
                        synonyms.append(SynonymPropertyValue(pred=pred, val=syn["value"]))

                meta["synonyms"] = synonyms

            # Add definition if available
            if "definition" in result:
                definition = result.get("definition", [])
                if definition and len(definition) > 0:
                    if isinstance(definition[0], str):
                        meta["definition"] = DefinitionPropertyValue(val=definition[0])
                    elif isinstance(definition[0], dict) and "value" in definition[0]:
                        meta["definition"] = DefinitionPropertyValue(val=definition[0]["value"])

            # Add obsolete flag if available
            if "obsolete" in result:
                meta["deprecated"] = result.get("obsolete", False)

            # Add any additional properties
            # if "properties" in result:
            #     for prop in result.get("properties", []):
            #         if isinstance(prop, dict) and "property" in prop and "values" in prop:
            #             prop_id = prop["property"]
            #             prop_values = prop["values"]
            #             if expand_curies:
            #                 prop_id = self.curie_to_uri(prop_id)
            #             meta[prop_id] = prop_values

            node.meta = Meta(**meta)

        return node
